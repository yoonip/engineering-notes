"""Network-free checks for persistent deduplication and publication boundaries."""
from datetime import datetime, timedelta, timezone
import html
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import update_pipeline as p

NOW = datetime(2026, 10, 29, 1, 0, tzinfo=timezone.utc)
SOURCE = {'id': 'example', 'group': 'reports', 'name': '공식 연구기관',
          'url': 'https://example.org/rss', 'hosts': ['example.org'],
          'format': 'feed', 'detail': False, 'language': 'ko'}


def item(n=1, description='전력 공급과 설비 투자에 필요한 조건을 분석한 보고서입니다.', date='2026-10-28', **kw):
    return dict(title=f'기술·경제 보고서 {n}', url=f'https://example.org/report?id={n}',
                description=description, date=date, **kw)


def feed(items):
    return '<rss><channel>' + ''.join('<item>' + ''.join(
        f'<{tag}>{html.escape(value)}</{tag}>' for tag, value in (
            ('title', row['title']), ('link', row['url']), ('description', row['description']), ('pubDate', row['date'])))
        + '</item>' for row in items) + '</channel></rss>'


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / 'repo'
        self.repo.mkdir()
        self.state = self.base / 'state.json'
        self.sources = [dict(SOURCE)]
        self.calls = []
        self.body = feed([item()])

    def fetch(self, url, hosts):
        self.calls.append(url)
        return self.body, url

    def run_at(self, now=NOW, fetcher=None, limit=3):
        return p.run({'sources': self.sources, 'initial_days': 45, 'initial_per_source': limit},
                     self.state, self.repo, now, fetcher or self.fetch)

    def snapshot(self):
        return {f.relative_to(self.repo).as_posix(): (f.read_bytes(), f.stat().st_mtime_ns)
                for f in self.repo.rglob('*') if f.is_file()}

    def test_unchanged_same_next_day_and_next_year_preserve_public_bytes_and_mtime(self):
        self.assertEqual(self.run_at()['new_or_updated'], 1)
        before = self.snapshot()
        for delta in (timedelta(hours=1), timedelta(days=1), timedelta(days=400)):
            result = self.run_at(NOW + delta)
            self.assertEqual(result['new_or_updated'], 0)
            self.assertEqual(result['changed_files'], [])
            self.assertEqual(before, self.snapshot())

    def test_initial_limit_does_not_leak_old_material_on_next_runs(self):
        self.body = feed([item(n) for n in range(1, 6)])
        self.assertEqual(self.run_at(limit=2)['new_or_updated'], 2)
        self.assertEqual(self.run_at(NOW + timedelta(hours=1), limit=2)['new_or_updated'], 0)
        self.body = feed([item(6, date='2026-10-29')] + [item(n) for n in range(1, 6)])
        self.assertEqual(self.run_at(NOW + timedelta(hours=2), limit=2)['new_or_updated'], 1)

    def test_substantive_update_keeps_same_identity_and_preserves_previous_day(self):
        self.run_at()
        before = {k: v for k, v in self.snapshot().items() if '2026-10-29.md' in k}
        self.body = feed([item(description='설비 투자 전망이 바뀌어 공급 계획과 대응 전략을 다시 설명합니다.')])
        result = self.run_at(NOW + timedelta(days=1))
        self.assertEqual(result['new_or_updated'], 1)
        self.assertEqual(result['sources'][0]['updated'], 1)
        for key, content in before.items():
            self.assertEqual(self.snapshot()[key], content)

    def test_tracking_query_and_timestamp_only_do_not_repost(self):
        self.run_at()
        row = item(date='2026-10-29')
        row['url'] += '&utm_source=feed'
        self.body = feed([row])
        self.assertEqual(self.run_at(NOW + timedelta(hours=1))['new_or_updated'], 0)

    def test_query_publication_ids_and_section_fragments_remain_distinct(self):
        self.assertNotEqual(p.canonical(item(1)['url']), p.canonical(item(2)['url']))
        self.assertNotEqual(p.canonical('https://example.org/updates/#a', True),
                            p.canonical('https://example.org/updates/#b', True))

    def test_google_exact_localized_slug_is_one_announcement(self):
        ko = 'https://blog.google/intl/ko-kr/company-news/technology/genie-4-world-simulation-kr/'
        en = 'https://deepmind.google/blog/genie-4-world-simulation/'
        self.assertEqual(p.publication_key('models', ko), p.publication_key('models', en))
        self.assertNotEqual(p.publication_key('models', en), p.publication_key('models', en.replace('genie-4', 'genie-5')))

    def test_no_24_hour_expiry_when_resuming_after_weeks(self):
        self.run_at()
        self.body = feed([item(2, date='2026-11-01')])
        self.assertEqual(self.run_at(NOW + timedelta(days=50))['new_or_updated'], 1)

    def test_month_precision_is_preserved_and_not_replaced_with_collection_day(self):
        self.body = feed([item(date='2026-10')])
        self.run_at()
        text = next((self.repo / p.GROUPS['reports'][0] / '새소식_updates').glob('README.md')).read_text(encoding='utf-8')
        self.assertIn('공식 페이지 표기일: 2026-10\n', text)
        self.assertEqual(p.outside_window('2026-10', NOW - timedelta(days=45), NOW), (False, False))

    def test_first_unknown_date_is_not_invented_and_future_item_is_deferred(self):
        self.body = feed([item(date=''), item(2, date='2026-12-01')])
        self.assertEqual(self.run_at()['new_or_updated'], 0)
        self.assertEqual(self.snapshot(), {})

    def test_existing_analysis_source_is_not_reposted(self):
        directory = self.repo / p.GROUPS['reports'][0] / '해설'
        directory.mkdir(parents=True)
        (directory / 'existing.md').write_text('[공식 원문](https://example.org/report?id=1)', encoding='utf-8')
        self.assertEqual(self.run_at()['new_or_updated'], 0)

    def test_detail_failure_pending_recovers_after_source_304(self):
        self.sources[0]['detail'] = True
        attempt = [0]
        def fetch(url, hosts):
            if url == SOURCE['url']:
                return (self.body if attempt[0] == 0 else None), url
            if attempt[0] == 0:
                raise p.FetchFailure('network_error')
            return '<html><meta property="og:description" content="전력 수요와 경제 전망의 연결을 설명하는 공식 보고서입니다."></html>', url
        with patch.object(p.report_adapters, 'detail', return_value={}):
            self.assertEqual(self.run_at(fetcher=fetch)['new_or_updated'], 0)
            attempt[0] = 1
            result = self.run_at(NOW + timedelta(hours=1), fetcher=fetch)
        self.assertEqual(result['new_or_updated'], 1)

    def test_unchanged_does_not_fetch_detail_again(self):
        self.sources[0]['detail'] = True
        calls = []
        def fetch(url, hosts):
            calls.append(url)
            return (self.body if url == SOURCE['url'] else '<html></html>'), url
        with patch.object(p.report_adapters, 'detail', return_value={}):
            self.run_at(fetcher=fetch)
            self.run_at(NOW + timedelta(hours=1), fetcher=fetch)
        self.assertEqual(calls.count(item()['url']), 1)

    def test_processed_source_body_is_not_kept_in_retry_cache(self):
        self.run_at()
        state = json.loads(self.state.read_text(encoding='utf-8'))
        self.assertEqual(state['sources']['example']['candidates'], [])
        self.assertTrue(state['seen'])

    def test_optional_detail_403_uses_official_feed_introduction(self):
        self.sources[0]['detail_if_empty'] = True
        self.body = feed([item(description='전력 수요와 새로운 설비 도입의 조건을 설명합니다.')])
        def fetch(url, hosts):
            if url != SOURCE['url']:
                raise p.FetchFailure('http_403')
            return self.body, url
        result = self.run_at(fetcher=fetch)
        self.assertEqual(result['new_or_updated'], 1)
        self.assertEqual(result['sources'][0]['feed_only'], 1)

    def test_pending_bootstrap_unknown_date_is_not_replaced_with_retry_date(self):
        self.sources[0]['detail'] = True
        self.body = feed([item(description='', date='')])
        attempt = [0]
        def fetch(url, hosts):
            if url == SOURCE['url']:
                return self.body, url
            if attempt[0] == 0:
                raise p.FetchFailure('network_error')
            return '<html><meta property="og:description" content="소개만 있고 발행일을 확인할 수 없는 보고서입니다."></html>', url
        with patch.object(p.report_adapters, 'detail', return_value={}):
            self.run_at(fetcher=fetch)
            attempt[0] = 1
            self.assertEqual(self.run_at(NOW + timedelta(hours=1), fetcher=fetch)['new_or_updated'], 0)

    def test_verification_program_is_not_a_new_model(self):
        self.assertFalse(p.model_adapters.eligible({'hosts': ['www.anthropic.com']},
            {'title': 'Introducing the Life Sciences Verification Program',
             'url': 'https://www.anthropic.com/news/life-sciences-verification',
             'description': 'A new program for model access.'}))

    def test_304_without_list_cache_clears_validator_for_recovery(self):
        self.sources.append(dict(SOURCE, id='other', url='https://example.org/other'))
        data = {'schema': 1, 'requests': {p.canonical(SOURCE['url']): {'ETag': 'stuck'}},
                'sources': {}, 'seen': {}, 'aliases': {}, 'robots': {}}
        self.state.write_text(json.dumps(data), encoding='utf-8')
        def fetch(url, hosts):
            return (None if url == SOURCE['url'] else self.body), url
        self.run_at(fetcher=fetch)
        after = json.loads(self.state.read_text(encoding='utf-8'))
        self.assertNotIn(p.canonical(SOURCE['url']), after['requests'])

    def test_total_failure_preserves_everything(self):
        self.run_at()
        before, state = self.snapshot(), self.state.read_bytes()
        def fail(url, hosts):
            raise p.FetchFailure('network_error')
        with self.assertRaises(RuntimeError):
            self.run_at(NOW + timedelta(hours=1), fetcher=fail)
        self.assertEqual(before, self.snapshot())
        self.assertEqual(state, self.state.read_bytes())

    def test_partial_failure_keeps_healthy_source(self):
        self.sources.append(dict(SOURCE, id='other', url='https://example.org/other'))
        def fetch(url, hosts):
            if url.endswith('/other'):
                raise p.FetchFailure('http_403')
            return self.body, url
        result = self.run_at(fetcher=fetch)
        self.assertEqual(result['new_or_updated'], 1)
        self.assertEqual(result['sources'][1]['status'], 'http_403')

    def test_kst_midnight_and_prior_archive_stability(self):
        before_midnight = datetime(2026, 10, 29, 14, 59, tzinfo=timezone.utc)
        self.run_at(before_midnight)
        self.body = feed([item(2, date='2026-10-30')])
        self.run_at(before_midnight + timedelta(minutes=2))
        dates = sorted(f.name for f in self.repo.rglob('2026-*.md'))
        self.assertEqual(dates, ['2026-10-29.md', '2026-10-30.md'])

    def test_no_false_translation_of_denials_or_planned_availability(self):
        text, mode = p.overview(dict(title='New Model X', description='Not improved at coding. Weights are planned, not released.'),
                                dict(SOURCE, group='models'))
        self.assertIn('코딩', text)
        self.assertNotIn('성능이 향상', text)
        self.assertNotIn('가중치를 공개', text)
        self.assertIn('안내', mode)

    def test_public_quote_is_short_and_markup_is_escaped(self):
        text, mode = p.overview(item(description='전력 수요를 분석합니다. ' * 70), SOURCE)
        self.assertLessEqual(len(text), 231)
        self.assertEqual(mode, '공식 한국어 소개 발췌')
        self.assertNotIn('<script>', p.clean('<script>alert(1)</script>공식 문서'))
        self.assertNotIn('[bad]', p.md_text('[bad](javascript:alert)'))

    def test_external_api_and_unsafe_urls_are_not_permitted(self):
        for url in ('http://example.org/report', 'https://127.0.0.1/a', 'https://api.openai.com/v1/responses',
                    'https://evil.invalid/x', 'https://user:secret@example.org/x'):
            self.assertFalse(p.safe_url(url, SOURCE['hosts']))

    def test_xml_external_entity_is_rejected(self):
        with self.assertRaises(ValueError):
            p.parse_feed('<!DOCTYPE rss [<!ENTITY file SYSTEM "file:///secret">]><rss/>')

    def test_revision_only_change_is_not_a_new_model(self):
        first = dict(item(), revision='a', lastModified='2026-10-28')
        second = dict(item(), revision='b', lastModified='2026-10-29')
        self.assertEqual(p.fingerprint(first), p.fingerprint(second))


if __name__ == '__main__':
    unittest.main()
