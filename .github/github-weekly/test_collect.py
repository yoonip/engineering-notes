"""주간 수집의 경계·실패·중복·출처 보존을 네트워크 없이 검사합니다."""
from __future__ import annotations

import builtins
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request

import collect as weekly


def trending_html(slugs=None, missing_metric=None):
    slugs = slugs or [f'owner/project-{number}' for number in range(1, 11)]
    rows = []
    for number, slug in enumerate(slugs, 1):
        metric = '123 stars today' if number == missing_metric else f'{number:,} stars this week'
        rows.append(f'''<article class="Box-row"><h2 class="h3">
            <a href="/{slug}"><span>{slug.split('/')[0]} /</span> {slug.split('/')[-1]}</a>
            </h2><p>A project description.</p><div><span>{metric}</span></div></article>''')
    return ('<html><body>' + ''.join(rows) + '</body></html>').encode()


def metadata(number, slug=None):
    slug = slug or f'owner/project-{number}'
    return {'id': number, 'full_name': slug, 'html_url': 'https://github.com/' + slug,
            'description': '공식 한국어 프로젝트 소개입니다.', 'language': 'Python',
            'stargazers_count': 1000 + number, 'forks_count': number, 'topics': [],
            'archived': False, 'disabled': False, 'license': {'spdx_id': 'MIT'},
            'default_branch': 'main', 'metadata_url': 'https://api.github.com/repos/' + slug}


class TrendingParserTests(unittest.TestCase):
    def test_preserves_display_order_and_weekly_metric(self):
        rows = weekly.parse_trending(trending_html())
        self.assertEqual([row['rank'] for row in rows], list(range(1, 11)))
        self.assertEqual(rows[0]['requested_full_name'], 'owner/project-1')
        self.assertEqual(rows[-1]['weekly_stars'], 10)

    def test_comma_metric_and_singular_star(self):
        raw = trending_html().replace(b'1 stars this week', b'1,234 stars this week', 1)
        raw = raw.replace(b'2 stars this week', b'1 star this week', 1)
        rows = weekly.parse_trending(raw)
        self.assertEqual(rows[0]['weekly_stars'], 1234)
        self.assertEqual(rows[1]['weekly_stars'], 1)

    def test_case_insensitive_duplicate_is_rejected(self):
        slugs = [f'owner/project-{number}' for number in range(1, 11)]
        slugs[-1] = 'OWNER/PROJECT-1'
        with self.assertRaises(ValueError):
            weekly.parse_trending(trending_html(slugs))

    def test_missing_weekly_metric_is_rejected(self):
        with self.assertRaises(ValueError):
            weekly.parse_trending(trending_html(missing_metric=10))

    def test_malformed_slug_is_rejected(self):
        for slug in ('owner/project/extra', 'https://evil.example/x', 'owner/project?x=1'):
            with self.subTest(slug=slug):
                raw = trending_html().replace(b'/owner/project-1"', ('/' + slug + '"').encode(), 1)
                with self.assertRaises(ValueError):
                    weekly.parse_trending(raw)

    def test_layout_change_and_short_results_fail_closed(self):
        for raw in (b'<html><p>Sign in</p></html>', trending_html(['owner/one'])):
            with self.subTest(raw=raw[:40]):
                with self.assertRaises(ValueError):
                    weekly.parse_trending(raw)


class CalendarTests(unittest.TestCase):
    def test_sunday_at_month_start_belongs_to_previous_monday(self):
        now = datetime(2026, 11, 1, 23, 59, tzinfo=weekly.KST)
        start = weekly.week_start(now)
        self.assertEqual(start.date().isoformat(), '2026-10-26')
        self.assertEqual(weekly.label(start), '2026년 10월 4주차')

    def test_new_year_does_not_relabel_the_same_calendar_week(self):
        now = datetime(2027, 1, 1, 12, tzinfo=weekly.KST)
        start = weekly.week_start(now)
        self.assertEqual(start.date().isoformat(), '2026-12-28')
        self.assertEqual(weekly.label(start), '2026년 12월 4주차')
        self.assertEqual(weekly.label(weekly.week_start(datetime(2027, 1, 4, tzinfo=weekly.KST))),
                         '2027년 1월 1주차')

    def test_utc_to_korea_monday_boundary(self):
        before = datetime(2026, 11, 1, 14, 59, tzinfo=timezone.utc)
        after = before + timedelta(minutes=1)
        self.assertEqual(weekly.week_start(before).date().isoformat(), '2026-10-26')
        self.assertEqual(weekly.week_start(after).date().isoformat(), '2026-11-02')


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='weekly-tests-', dir=weekly.HERE)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.output = self.root / 'projects'
        self.cache = self.root / 'translations.json'
        self.now = datetime(2026, 11, 2, 9, 23, tzinfo=weekly.KST)

    def publish(self):
        with patch.object(weekly, 'get', return_value=(trending_html(), weekly.TRENDING)), \
             patch.object(weekly, 'repository', side_effect=lambda slug, token: metadata(int(slug.rsplit('-', 1)[1]))):
            return weekly.collect(self.output, self.now, '', {}, self.cache)

    def test_records_source_metrics_and_resolvable_archive_links(self):
        result = self.publish()
        self.assertEqual(result['status'], 'published')
        archive = self.output / '주간기록/2026/11/2026-11-02.json'
        data = json.loads(archive.read_text(encoding='utf-8'))
        self.assertEqual(data['source_url'], weekly.TRENDING)
        self.assertEqual(data['source_sha256'], weekly.hashlib.sha256(trending_html()).hexdigest())
        self.assertEqual(data['items'][0]['weekly_stars'], 1)
        self.assertEqual(data['items'][0]['repository']['stargazers_count'], 1001)
        md = archive.with_suffix('.md').read_text(encoding='utf-8')
        self.assertIn('[주간 기록 목록](../../README.md)', md)
        self.assertTrue((archive.parent / '../../README.md').resolve().is_file())

    def test_same_week_is_immutable_and_performs_no_fetch(self):
        self.publish()
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        with patch.object(weekly, 'get', side_effect=AssertionError('already published must not fetch')):
            result = weekly.collect(self.output, self.now + timedelta(days=6), '', {}, self.cache)
        self.assertEqual(result['status'], 'already_published')
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_last_repository_failure_writes_no_archive_or_cache(self):
        def failing_repository(slug, token):
            number = int(slug.rsplit('-', 1)[1])
            if number == 10:
                raise HTTPError('https://api.github.com/repos/' + slug, 503, 'Unavailable', {}, None)
            return metadata(number)
        with patch.object(weekly, 'get', return_value=(trending_html(), weekly.TRENDING)), \
             patch.object(weekly, 'repository', side_effect=failing_repository):
            with self.assertRaises(HTTPError):
                weekly.collect(self.output, self.now, '', {}, self.cache)
        self.assertFalse(self.output.exists())
        self.assertFalse(self.cache.exists())

    def test_trending_failure_writes_no_files(self):
        with patch.object(weekly, 'get', side_effect=TimeoutError('network unavailable')):
            with self.assertRaises(TimeoutError):
                weekly.collect(self.output, self.now, '', {}, self.cache)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_redirected_duplicate_id_is_not_published(self):
        with patch.object(weekly, 'get', return_value=(trending_html(), weekly.TRENDING)), \
             patch.object(weekly, 'repository', return_value=metadata(1, 'canonical/project')):
            with self.assertRaisesRegex(ValueError, 'duplicate'):
                weekly.collect(self.output, self.now, '', {}, self.cache)
        self.assertFalse(self.output.exists())
        self.assertFalse(self.cache.exists())

    def test_missing_markdown_is_rebuilt_from_saved_snapshot(self):
        self.publish()
        path = self.output / '주간기록/2026/11/2026-11-02.md'
        expected = path.read_bytes()
        json_path = path.with_suffix('.json')
        original_json = json_path.read_bytes()
        path.unlink()
        with patch.object(weekly, 'get', side_effect=AssertionError('recovery must use saved snapshot')):
            weekly.collect(self.output, self.now + timedelta(hours=4), '', {}, self.cache)
        self.assertEqual(path.read_bytes(), expected)
        self.assertEqual(json_path.read_bytes(), original_json)

    def test_detailed_publication_fetches_and_preserves_pinned_readme_sources(self):
        def readme_for(repo, token, getter):
            return {'status': 'ok', 'text': '## 기능\n공식 기능을 설명하는 한국어 문서입니다.\n## 설치\nPython을 준비합니다.\n```sh\nrun-official-example\n```',
                    'sha': str(repo['id']) * 40, 'commit': 'a' * 40, 'path': 'README.md',
                    'source_url': repo['html_url'] + '/blob/' + 'a' * 40 + '/README.md',
                    'fetched_at': '2026-11-02T00:00:00+00:00'}
        with patch.object(weekly, 'get', return_value=(trending_html(), weekly.TRENDING)), \
             patch.object(weekly, 'repository', side_effect=lambda slug, token: metadata(int(slug.rsplit('-', 1)[1]))), \
             patch.object(weekly.guides, 'fetch_readme', side_effect=readme_for), \
             patch.object(weekly.guides, 'linked_documents', return_value=[]):
            weekly.collect(self.output, self.now, '', {}, self.cache, details={})
        data = json.loads((self.output / '주간기록/2026/11/2026-11-02.json').read_text(encoding='utf8'))
        self.assertTrue(all('guide' in item and 'readme' in item for item in data['items']))
        self.assertNotIn('text', data['items'][0]['readme'])
        self.assertEqual(data['items'][0]['guide']['install_code']['code'], 'run-official-example')

    def test_readme_failure_cannot_publish_a_partial_detailed_week(self):
        with patch.object(weekly, 'get', return_value=(trending_html(), weekly.TRENDING)), \
             patch.object(weekly, 'repository', return_value=metadata(1)), \
             patch.object(weekly.guides, 'fetch_readme', side_effect=TimeoutError('README unavailable')):
            with self.assertRaises(TimeoutError):
                weekly.collect(self.output, self.now, '', {}, self.cache, details={})
        self.assertFalse(self.output.exists())
        self.assertFalse(self.cache.exists())


class ContentTests(unittest.TestCase):
    def test_markdown_and_html_from_descriptions_are_displayed_as_text(self):
        value = weekly.clean('<script>alert(1)</script> [evil](javascript:alert(1)) **bold** | next\n# heading')
        self.assertNotIn('<script>', value)
        self.assertIn('&lt;script&gt;', value)
        self.assertIn(r'\[evil\]', value)
        self.assertIn(r'\*\*bold\*\*', value)
        self.assertIn(r'\|', value)
        self.assertNotIn('\n', value)

    def test_cached_translation_does_not_import_argos(self):
        source = 'A tool for generating videos from HTML.'
        entry = {'source': source, 'text': 'HTML로 영상을 만드는 도구입니다.',
                 'method': 'Argos Translate en→ko 1.1'}
        introductions = weekly.Introductions({}, {weekly.digest(source): entry})
        original_import = builtins.__import__

        def no_argos(name, *args, **kwargs):
            if name.startswith('argostranslate'):
                raise AssertionError('cached translation must not initialize the model')
            return original_import(name, *args, **kwargs)

        with patch('builtins.__import__', side_effect=no_argos):
            self.assertEqual(introductions.translate(source), entry)

    def test_missing_license_is_not_labeled_open_source(self):
        repo = metadata(1)
        repo['license'] = None
        item = {'rank': 1, 'weekly_stars': 2, 'repository': repo,
                'introduction': {'text': '소개입니다.', 'method': '공식 소개', 'source_url': repo['html_url']}}
        rendered = weekly.render_entry(item)
        self.assertIn('공식 라이선스 파일 확인', rendered)
        self.assertNotIn('라이선스: MIT', rendered)

    def test_reviewed_summary_requires_same_repository_and_description(self):
        repo = metadata(1)
        reviewed = {repo['full_name']: {'repository_id': 1,
                    'description_sha256': weekly.digest(repo['description']),
                    'reviewed_at': '2026-11-02', 'summary_ko': '확인한 한국어 해설입니다.'}}
        introductions = weekly.Introductions(reviewed, {})
        self.assertEqual(introductions.for_repo(repo)['text'], '확인한 한국어 해설입니다.')
        changed = dict(repo, description='새 용도의 공식 한국어 소개입니다.')
        self.assertEqual(introductions.for_repo(changed)['text'], changed['description'])
        recreated = dict(repo, id=99)
        self.assertEqual(introductions.for_repo(recreated)['text'], repo['description'])


class RedirectTests(unittest.TestCase):
    def test_cross_host_or_downgrade_is_rejected_before_new_request(self):
        handler = weekly.SafeRedirect()
        request = Request('https://api.github.com/repos/old/name', headers={'Authorization': 'Bearer test-only'})
        for target in ('https://evil.example/capture', 'https://github.com/new/name',
                       'http://api.github.com/repos/new/name'):
            with self.subTest(target=target):
                with self.assertRaises((ValueError, HTTPError)):
                    handler.redirect_request(request, None, 301, 'Moved', {}, target)

    def test_same_host_redirect_preserves_authenticated_api_lookup(self):
        handler = weekly.SafeRedirect()
        request = Request('https://api.github.com/repos/old/name', headers={'Authorization': 'Bearer test-only'})
        redirected = handler.redirect_request(request, None, 301, 'Moved', {},
                                              'https://api.github.com/repositories/123')
        self.assertEqual(redirected.full_url, 'https://api.github.com/repositories/123')
        self.assertEqual(redirected.get_header('Authorization'), 'Bearer test-only')


if __name__ == '__main__':
    unittest.main()
