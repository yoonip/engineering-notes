"""날짜별 뉴스 보관의 경계·링크·실패 처리 계약을 검사합니다."""
from datetime import datetime, timezone
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

import archive_news as archive

FIRST = datetime(2026, 10, 28, 14, 59, tzinfo=timezone.utc)
SECOND = datetime(2026, 10, 28, 15, 0, tzinfo=timezone.utc)


class NewsArchiveTests(unittest.TestCase):
    def test_kst_midnight_starts_a_new_daily_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / '최신뉴스_latest.md'
            first = archive.publish_bundle(output, 'Previous day\n', FIRST)
            second = archive.publish_bundle(output, 'Next day\n', SECOND)
            self.assertEqual(first['daily'], '날짜별/2026/2026-10-28.md')
            self.assertEqual(second['daily'], '날짜별/2026/2026-10-29.md')
            self.assertEqual((root / first['daily']).read_bytes(), b'Previous day\n')
            self.assertEqual((root / second['daily']).read_bytes(), b'Next day\n')
            self.assertEqual(output.read_bytes(), b'Next day\n')

    def test_same_day_refresh_has_one_index_entry(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / '최신뉴스_latest.md'
            archive.publish_bundle(output, 'First\n', SECOND)
            result = archive.publish_bundle(output, 'Refreshed\n', SECOND)
            index = (root / result['index']).read_text(encoding='utf-8')
            self.assertEqual(index.count('[2026-10-29]'), 1)
            self.assertEqual((root / result['daily']).read_text(encoding='utf-8'), 'Refreshed\n')

    def test_known_internal_links_resolve_from_both_views(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ('README.md', '매체와수집기준_sources.md', '운영안내_operations.md'):
                (root / name).write_text('# Reference\n', encoding='utf-8')
            output = root / '최신뉴스_latest.md'
            text = ('[안내](README.md#guide) [출처](<매체와수집기준_sources.md>) '
                    '[운영](운영안내_operations.md) [최신](최신뉴스_latest.md) '
                    '[날짜별](날짜별/README.md)\n')
            result = archive.publish_bundle(output, text, SECOND)
            for document in (output, root / result['daily'], root / result['index']):
                for target in re.findall(r'\]\(<?([^\s>)]+)>?\)', document.read_text(encoding='utf-8')):
                    target = target.split('#', 1)[0]
                    self.assertTrue((document.parent / target).resolve().is_file(),
                                    str(document) + ' -> ' + target)

    def test_external_urls_and_visible_headlines_are_unchanged(self):
        text = ('[README.md is a headline](<https://news.example.org/README.md?a=1&b=2>)\n'
                '[News](https://news.example.org/날짜별/README.md#latest)\n')
        self.assertEqual(archive.archive_text(text), text)

    def test_index_lists_only_existing_valid_dates_in_reverse_order(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = ('2025/2025-12-31.md', '2026/2026-01-01.md', '2026/2026-02-30.md',
                     '2025/2026-01-02.md', '2026/random.md')
            for name in paths:
                path = root / '날짜별' / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b'Historical body\n')
            result = archive.publish_bundle(root / '최신뉴스_latest.md', 'Today\n', SECOND)
            index = (root / result['index']).read_text(encoding='utf-8')
            self.assertLess(index.index('[2026-10-29]'), index.index('[2026-01-01]'))
            self.assertLess(index.index('[2026-01-01]'), index.index('[2025-12-31]'))
            for absent in ('2026-02-30', '2026-01-02', 'random'):
                self.assertNotIn(absent, index)
            for name in paths:
                self.assertEqual((root / '날짜별' / name).read_bytes(), b'Historical body\n')

    def test_naive_time_is_rejected_without_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaises(ValueError):
                archive.publish_bundle(root / '최신뉴스_latest.md', 'News\n', datetime(2026, 10, 29))
            self.assertEqual(list(root.iterdir()), [])

    def test_category_readme_is_supported_as_latest_view(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / 'README.md'
            result = archive.publish_bundle(output, '[Latest](README.md)\n', SECOND)
            index = (root / result['index']).read_text(encoding='utf-8')
            daily = (root / result['daily']).read_text(encoding='utf-8')
            self.assertEqual(result['latest'], 'README.md')
            self.assertIn('[최신 뉴스](../README.md)', index)
            self.assertNotIn('최신뉴스_latest.md', index)
            self.assertIn('[Latest](../../README.md)', daily)

    def test_parent_traversal_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                archive.publish_bundle(Path(directory) / '..' / 'outside.md', 'News\n', SECOND)

    def test_stage_failure_keeps_previous_documents_and_removes_temporaries(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / '최신뉴스_latest.md'
            archive.publish_bundle(output, 'Original\n', SECOND)
            before = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob('*.md')}
            real_stage = archive._stage
            calls = 0
            def fail_last(target, text):
                nonlocal calls
                calls += 1
                if calls == 3:
                    raise OSError('simulated full disk')
                return real_stage(target, text)
            with patch.object(archive, '_stage', side_effect=fail_last), self.assertRaises(OSError):
                archive.publish_bundle(output, 'Replacement\n', SECOND)
            after = {str(p.relative_to(root)): p.read_bytes() for p in root.rglob('*.md')}
            self.assertEqual(before, after)
            self.assertEqual(list(root.rglob('*.tmp')), [])

    def test_symlink_output_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            real = root / 'real.md'
            real.write_text('Keep\n', encoding='utf-8')
            link = root / 'latest.md'
            try:
                link.symlink_to(real)
            except OSError as exc:
                self.skipTest('Symbolic links are unavailable: ' + str(exc))
            with self.assertRaises(ValueError):
                archive.publish_bundle(link, 'Replace\n', SECOND)
            self.assertEqual(real.read_bytes(), b'Keep\n')

    def test_archive_directory_cannot_redirect_outside_root(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root = Path(directory)
            try:
                (root / '날짜별').symlink_to(Path(outside), target_is_directory=True)
            except OSError as exc:
                self.skipTest('Symbolic links are unavailable: ' + str(exc))
            with self.assertRaises(ValueError):
                archive.publish_bundle(root / '최신뉴스_latest.md', 'Replace\n', SECOND)
            self.assertEqual(list(Path(outside).iterdir()), [])
            self.assertFalse((root / '최신뉴스_latest.md').exists())


if __name__ == '__main__':
    unittest.main()
