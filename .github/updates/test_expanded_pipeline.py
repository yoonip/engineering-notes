from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import update_pipeline as p
from test_update_pipeline import NOW, SOURCE, item, feed


class ExpandedTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name) / 'repo'
        self.repo.mkdir()
        self.state = self.repo.parent / 'state.json'

    def run_sources(self, sources, body, now=NOW):
        fake = SimpleNamespace()
        with patch.dict(p.ADAPTERS, {source['group']: fake for source in sources}):
            return p.run({'sources': sources, 'initial_days': 45, 'initial_per_source': 3},
                         self.state, self.repo, now, lambda url, hosts: (body, url))

    def test_topic_words_do_not_match_inside_unrelated_english_words(self):
        source = {'group': 'products', 'name': '공식 자료'}
        for title, unwanted in [('Reagent quality in DNA sequencing', '에이전트·도구 사용'),
                                ('Decoding retinal signals for visual prostheses', '코딩'),
                                ('Neural encoding of speech sounds', '코딩'),
                                ('Firmware revision 2.1 release notes', '이미지·영상 처리')]:
            with self.subTest(title=title):
                summary, _ = p.overview({'title': title}, source)
                self.assertNotIn(unwanted, summary)
        for title, expected in [('Agents and tool calling', '에이전트·도구 사용'),
                                ('Coding assistants for software engineering', '코딩'),
                                ('Code generation with static checks', '코딩'),
                                ('Agentic systems', '에이전트·도구 사용'),
                                ('Computer vision and videos', '이미지·영상 처리')]:
            with self.subTest(title=title):
                summary, _ = p.overview({'title': title}, source)
                self.assertIn(expected, summary)

    def test_general_context_and_memory_do_not_imply_ai_context_or_chip_memory(self):
        source = {'group': 'papers', 'name': '공식 논문 초록'}
        examples = [
            ('Neuroscience of Improvisation Across Music and Other Domains',
             'Memory and creative behavior depend on context.', '긴 문맥·장기 작업'),
            ('Near-Field Multipath MIMO Channels',
             'We evaluate channel models in the context of wireless communications.', '긴 문맥·장기 작업'),
            ('xCHEM: SDR-Based Multi-Link Channel Emulator',
             'The implementation uses FPGA memory for wireless channel responses.', '메모리·캐시'),
        ]
        for title, description, unwanted in examples:
            with self.subTest(title=title):
                summary, _ = p.overview({'title': title, 'description': description}, source)
                self.assertNotIn(unwanted, summary)
        for title, expected in [('Long-context models and context windows', '긴 문맥·장기 작업'),
                                ('HBM memory bandwidth and SRAM cache', '메모리·캐시')]:
            summary, _ = p.overview({'title': title}, source)
            self.assertIn(expected, summary)

    def test_six_inboxes_preserve_all_existing_analysis_bytes_and_record_provenance(self):
        for group in ('technology', 'tools', 'industry', 'products', 'papers', 'learning'):
            root = self.repo / p.GROUPS[group][0]
            root.mkdir()
            analysis = root / '기존해설.md'
            analysis.write_bytes(b'original analysis\n')
            original_time = analysis.stat().st_mtime_ns
            source = dict(SOURCE, id=group, group=group, acquisition_method='공식 RSS의 소개문')
            row = item()
            row['url'] += '&group=' + group
            self.run_sources([source], feed([row]))
            output = root / '새자료_inbox/README.md'
            text = output.read_text(encoding='utf-8')
            for expected in ('가져온 시각: 2026-10-29 10:00:00 KST', '수집 경로:', '공식 RSS의 소개문', 'https://example.org/rss'):
                self.assertIn(expected, text)
            self.assertEqual(analysis.read_bytes(), b'original analysis\n')
            self.assertEqual(analysis.stat().st_mtime_ns, original_time)
            self.assertFalse((root / '새소식_updates').exists())

    def test_same_original_in_two_categories_is_published_once(self):
        sources = [dict(SOURCE, id='technology', group='technology'), dict(SOURCE, id='products', group='products')]
        result = self.run_sources(sources, feed([item()]))
        self.assertEqual(result['new_or_updated'], 1)
        self.assertEqual(result['sources'][1]['other_category'], 1)
        self.assertFalse((self.repo / p.GROUPS['products'][0] / '새자료_inbox').exists())

    def test_existing_analysis_in_another_category_is_not_reposted(self):
        root = self.repo / p.GROUPS['products'][0]
        root.mkdir()
        (root / 'analysis.md').write_text('[원문](https://example.org/report?id=1)', encoding='utf-8')
        result = self.run_sources([dict(SOURCE, group='technology')], feed([item()]))
        self.assertEqual(result['new_or_updated'], 0)

    def test_arxiv_version_pdf_and_abstract_identify_the_same_original(self):
        self.assertEqual(p.original_identity('https://arxiv.org/pdf/2610.12345v2.pdf'),
                         p.original_identity('https://arxiv.org/abs/2610.12345v1'))

    def test_atom_alternate_is_not_replaced_with_comments_or_self_link(self):
        body = '''<feed xmlns="http://www.w3.org/2005/Atom"><entry><title>Technical note</title>
        <link rel="alternate" href="https://example.org/note"/>
        <link rel="replies" href="https://example.org/note/feed"/>
        <link rel="self" href="https://example.org/atom"/><published>2026-10-28T00:00:00Z</published></entry></feed>'''
        self.assertEqual(p.parse_feed(body)[0]['url'], 'https://example.org/note')

    def test_wordpress_footer_is_not_a_korean_introduction(self):
        body = feed([item(description='공식 한국어 기술 소개입니다. The post Example appeared first on NVIDIA Blog Korea.')])
        self.assertEqual(p.parse_feed(body)[0]['description'], '공식 한국어 기술 소개입니다.')

    def test_empty_arxiv_weekend_is_not_a_parser_failure(self):
        source = dict(SOURCE, group='papers', allow_empty_feed=True)
        result = self.run_sources([source], '<rss><channel/></rss>')
        self.assertEqual(result['sources'][0]['status'], 'no_recent_items')
        self.assertFalse(result['changed_files'])

    def test_subject_filters_and_selection_limit_do_not_drip_old_material(self):
        source = dict(SOURCE, group='technology', include_patterns=['전력'], max_new_items=1)
        self.run_sources([source], feed([item(1)]))
        result = self.run_sources([source], feed([item(2, date='2026-10-29'), item(3, date='2026-10-29')]), NOW + timedelta(hours=1))
        self.assertEqual(result['new_or_updated'], 1)
        self.assertEqual(result['sources'][0]['not_selected'], 1)
        result = self.run_sources([source], feed([item(2, date='2026-10-29'), item(3, date='2026-10-29')]), NOW + timedelta(hours=2))
        self.assertEqual(result['new_or_updated'], 0)

    def test_bulletin_query_identity_excludes_search_and_page_state(self):
        one = 'https://www.boho.or.kr/kr/bbs/view.do?bbsId=B1&nttId=42&pageIndex=1'
        two = 'https://www.boho.or.kr/kr/bbs/view.do?nttId=42&bbsId=B1&searchWrd=&pageIndex=3'
        self.assertEqual(p.canonical(one), p.canonical(two))

    def test_arxiv_hosts_share_one_three_second_request_budget(self):
        client = p.Client({}, [{'hosts': ['rss.arxiv.org', 'arxiv.org'], 'min_interval_seconds': 3, 'rate_limit_group': 'arxiv'}])
        with patch.object(p.time, 'monotonic', side_effect=[0, 1, 3]), patch.object(p.time, 'sleep') as sleep:
            client.throttle('https://rss.arxiv.org/rss/cs.AI')
            client.throttle('https://arxiv.org/robots.txt')
        sleep.assert_called_once_with(2)

    def test_month_boundary_uses_korean_calendar(self):
        now = datetime(2026, 10, 31, 15, 37, tzinfo=timezone.utc)
        self.assertEqual(p.outside_window('2026-11', now - timedelta(days=45), now), (False, False))

    def test_publication_uses_completion_date_when_collection_crosses_midnight(self):
        started = datetime(2026, 10, 31, 14, 59, tzinfo=timezone.utc)
        fetched = started + timedelta(minutes=2)
        finished = started + timedelta(minutes=3)
        ticks = iter((fetched, finished))
        with patch.dict(p.ADAPTERS, {'reports': SimpleNamespace()}):
            result = p.run({'sources': [SOURCE]}, self.state, self.repo, started,
                           lambda url, hosts: (feed([item()]), url), clock=lambda: next(ticks))
        directory = self.repo / p.GROUPS['reports'][0] / p.OUTPUT_DIRS['reports']
        self.assertTrue((directory / '날짜별/2026-11-01.md').exists())
        self.assertFalse((directory / '날짜별/2026-10-31.md').exists())
        text = (directory / 'README.md').read_text(encoding='utf-8')
        self.assertIn('반영: 2026-11-01 00:02 KST', text)
        self.assertIn('가져온 시각: 2026-11-01 00:01:00 KST', text)
        self.assertEqual(result['started_at'], started.isoformat())
        self.assertEqual(result['checked_at'], finished.isoformat())


if __name__ == '__main__':
    unittest.main()
