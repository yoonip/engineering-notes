"""공식 뉴스 피드의 변경 판별·당일 누적·이전 날짜 보존을 검사합니다."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
from urllib.error import HTTPError

import news_pipeline as pipeline

NOW = datetime(2026, 10, 29, 0, 17, tzinfo=timezone.utc)


def source(identifier='world', group='world', mode='native_feed'):
    return {'id': identifier, 'name': identifier, 'group': group, 'summary_mode': mode,
            'homepage': 'https://news.example.org/', 'priority': 20}


def article(title='Central bank keeps interest rate at 3 percent',
            url='https://news.example.org/central-bank',
            excerpt='The central bank kept its interest rate at 3 percent.', published=None):
    return {'title': title, 'url': url, 'excerpt': excerpt,
            'published_at': (published or NOW - timedelta(minutes=5)).isoformat()}


def fetcher_for(items_by_source, state_by_source=None):
    states = state_by_source or {}
    def fetcher(src, now):
        entries = deepcopy(items_by_source.get(src['id'], []))
        state = states.get(src['id'], 'ok' if entries else 'no_recent_items')
        return {'source': src, 'items': entries, 'state': state, 'stats': {}}
    return fetcher


def snapshots(root):
    return {str(path.relative_to(root)): (path.read_bytes(), path.stat().st_mtime_ns)
            for path in root.rglob('*') if path.is_file()}


class PipelineChangeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.state = self.root / 'engine' / 'state.json'
        self.news = self.root / '뉴스_news'
        self.world = source()
        self.korea = source('korea', 'korea', 'native_feed')
        self.config = {'sources': [self.world, self.korea], 'new_items_per_group': 10}
        self.translator = Mock()
        self.translator.translate.side_effect = AssertionError('Production must not translate news')

    def run_items(self, items, now=NOW, states=None):
        return pipeline.run(self.config, self.state, self.news, now,
                            translator=self.translator, fetcher=fetcher_for(items, states))

    def test_unchanged_articles_do_not_translate_or_write_reader_files(self):
        items = {'world': [article()]}
        self.run_items(items)
        self.translator.reset_mock()
        before = snapshots(self.news)
        before_articles = deepcopy(pipeline.load_state(self.state)['articles'])
        result = self.run_items(items, NOW + timedelta(hours=1))
        self.assertFalse(result['changed'])
        self.translator.translate.assert_not_called()
        self.assertEqual(snapshots(self.news), before)
        self.assertEqual(pipeline.load_state(self.state)['articles'], before_articles)

    def test_title_decoration_and_publication_time_alone_are_not_updates(self):
        first = article('[속보] 기준금리 3% 동결', excerpt='기준금리를 3%로 유지했습니다.')
        later = article('기준금리 3% 동결(종합)', excerpt=first['excerpt'],
                        published=NOW + timedelta(minutes=50))
        self.run_items({'korea': [first]})
        before = snapshots(self.news)
        before_articles = deepcopy(pipeline.load_state(self.state)['articles'])
        self.translator.reset_mock()
        result = self.run_items({'korea': [later]}, NOW + timedelta(hours=1))
        self.assertFalse(result['changed'])
        self.assertEqual(snapshots(self.news), before)
        self.assertEqual(pipeline.load_state(self.state)['articles'], before_articles)
        self.translator.translate.assert_not_called()

    def test_temporary_missing_excerpt_does_not_delete_or_retranslate_known_news(self):
        first = article()
        self.run_items({'world': [first]})
        self.translator.reset_mock()
        before = snapshots(self.news)
        result = self.run_items({'world': [dict(first, excerpt='')]}, NOW + timedelta(hours=1))
        self.assertFalse(result['changed'])
        self.translator.translate.assert_not_called()
        self.assertEqual(snapshots(self.news), before)
        saved = next(iter(pipeline.load_state(self.state)['articles'].values()))
        self.assertEqual(saved['excerpt'], first['excerpt'])

    def test_same_story_at_another_url_is_not_republished(self):
        first = article()
        duplicate = dict(first, url='https://news.example.org/retransmitted')
        self.run_items({'world': [first]})
        self.translator.reset_mock()
        before = snapshots(self.news)
        before_articles = deepcopy(pipeline.load_state(self.state)['articles'])
        result = self.run_items({'world': [duplicate]}, NOW + timedelta(hours=1))
        self.assertFalse(result['changed'])
        self.assertEqual(snapshots(self.news), before)
        self.assertEqual(pipeline.load_state(self.state)['articles'], before_articles)
        self.translator.translate.assert_not_called()

    def test_nearly_identical_resend_is_not_a_new_story(self):
        first = article(title='Central bank keeps its key interest rate unchanged at 3 percent')
        resend = dict(first, title='Central bank keeps the key interest rate unchanged at 3 percent',
                      url='https://news.example.org/reissued')
        self.assertTrue(pipeline.near_duplicate(
            dict(first, group='world'), dict(resend, group='world')))
        self.run_items({'world': [first]})
        self.translator.reset_mock()
        before = snapshots(self.news)
        before_articles = deepcopy(pipeline.load_state(self.state)['articles'])
        result = self.run_items({'world': [resend]}, NOW + timedelta(hours=1))
        self.assertFalse(result['changed'])
        self.assertEqual(snapshots(self.news), before)
        self.assertEqual(pipeline.load_state(self.state)['articles'], before_articles)
        self.translator.translate.assert_not_called()

    def test_previously_observed_unselected_story_does_not_drip_into_next_run(self):
        self.config['new_items_per_group'] = 1
        first = article()
        unselected = article('Hurricane approaches a coastal town',
            url='https://news.example.org/unselected', excerpt='A hurricane approached the coastal town.')
        inputs = {'world': [first, unselected]}
        self.run_items(inputs)
        stored = pipeline.load_state(self.state)
        self.assertEqual(len(stored['articles']), 1)
        self.assertEqual(len(stored['observed']), 2)
        # 미선정 항목의 원문 텍스트를 별도 공개 캐시에 쌓지 않습니다.
        for hashed_url, observation in stored['observed'].items():
            self.assertRegex(hashed_url, r'^[a-f0-9]{64}$')
            self.assertEqual(set(observation), {'fingerprint', 'at'})
            self.assertRegex(observation['fingerprint'], r'^[a-f0-9]{64}$')
        before = snapshots(self.news)
        self.translator.reset_mock()
        result = self.run_items(inputs, NOW + timedelta(hours=1))
        self.assertFalse(result['changed'])
        self.assertEqual(result['new_articles'], 0)
        self.assertEqual(snapshots(self.news), before)
        self.translator.translate.assert_not_called()
        self.assertEqual(len(pipeline.load_state(self.state)['articles']), 1)

    def test_observed_unselected_url_can_enter_when_important_facts_change(self):
        self.config['new_items_per_group'] = 1
        first = article()
        unselected = article('Hurricane kills 3 people',
            url='https://news.example.org/unselected', excerpt='The hurricane killed 3 people.')
        self.run_items({'world': [first, unselected]})
        followup = dict(unselected, title='Hurricane kills 4 people', excerpt='The hurricane killed 4 people.')
        self.translator.reset_mock()
        result = self.run_items({'world': [first, followup]}, NOW + timedelta(hours=1))
        self.assertTrue(result['changed'])
        self.assertEqual(result['new_articles'], 1)
        self.translator.translate.assert_not_called()
        self.assertIn(followup['url'],
            (self.news / pipeline.GROUP_PATHS['world'] / 'README.md').read_text(encoding='utf-8'))

    def test_http_304_preserves_news_and_does_not_initialize_translation_model(self):
        self.run_items({'world': [article()]})
        state = pipeline.load_state(self.state)
        conditional = {'ETag': '"edition-7"', 'Last-Modified': 'Thu, 29 Oct 2026 00:00:00 GMT'}
        state['feeds']['world'] = conditional
        pipeline.save_state(self.state, state)
        before = snapshots(self.news)
        seen_requests = []
        def conditional_fetcher(src, now):
            feed_source = dict(src, feed_url='https://news.example.org/feed.xml',
                               feed_hosts=['news.example.org'], article_hosts=['news.example.org'])
            if src['id'] == 'korea':
                return {'source': src, 'items': [], 'state': 'no_recent_items', 'stats': {}}
            def not_modified(request, **kwargs):
                seen_requests.append(request)
                raise HTTPError(request.full_url, 304, 'Not Modified', {}, None)
            with patch.object(pipeline.core, 'build_opener') as build:
                build.return_value.open.side_effect = not_modified
                return pipeline.core.fetch_source(feed_source, now)
        result = pipeline.run(self.config, self.state, self.news, NOW + timedelta(hours=1),
                              translator=self.translator, fetcher=conditional_fetcher)
        self.translator.translate.assert_not_called()
        self.assertFalse(result['changed'])
        self.assertEqual(snapshots(self.news), before)
        self.assertEqual(len(seen_requests), 1)
        headers = {name.lower(): value for name, value in seen_requests[0].header_items()}
        self.assertEqual(headers['if-none-match'], conditional['ETag'])
        self.assertEqual(headers['if-modified-since'], conditional['Last-Modified'])
        self.assertEqual(result['sources'][0]['state'], 'unchanged')

    def test_changed_casualty_number_at_a_different_url_is_new_information(self):
        first = article('Earthquake kills 3 people', excerpt='The earthquake killed 3 people.')
        followup = article('Earthquake kills 4 people', url='https://news.example.org/follow-up',
                           excerpt='The earthquake killed 4 people.')
        self.run_items({'world': [first]})
        self.translator.reset_mock()
        result = self.run_items({'world': [followup]}, NOW + timedelta(hours=1))
        self.assertTrue(result['changed'])
        self.assertEqual(result['new_articles'], 1)
        self.translator.translate.assert_not_called()
        state = pipeline.load_state(self.state)
        self.assertEqual(len(state['articles']), 2)

    def test_same_url_substantive_update_replaces_entry_and_keeps_previous_title(self):
        first = article('Earthquake kills 3 people', excerpt='The earthquake killed 3 people.')
        followup = dict(first, title='Earthquake kills 4 people', excerpt='The earthquake killed 4 people.')
        self.run_items({'world': [first]})
        result = self.run_items({'world': [followup]}, NOW + timedelta(hours=1))
        state = pipeline.load_state(self.state)
        self.assertEqual(result['updated_articles'], 1)
        self.assertEqual(result['new_articles'], 0)
        self.assertEqual(len(state['articles']), 1)
        saved = next(iter(state['articles'].values()))
        self.assertEqual(saved['title'], followup['title'])
        self.assertEqual(saved['history'][-1]['title'], first['title'])

    def test_new_world_story_does_not_rewrite_unchanged_korean_view(self):
        domestic = article('국내 기준금리 동결', url='https://news.example.org/korea', excerpt='기준금리를 유지했습니다.')
        self.run_items({'korea': [domestic]})
        category = self.news / pipeline.GROUP_PATHS['korea']
        before = snapshots(category)
        self.run_items({'world': [article()], 'korea': [domestic]}, NOW + timedelta(hours=1))
        self.assertEqual(snapshots(category), before)

    def test_same_day_accumulates_new_urls_without_removing_earlier_news(self):
        first = article(url='https://news.example.org/first')
        second = article('Hurricane approaches coast', url='https://news.example.org/second',
                         excerpt='A hurricane approached the coast.')
        self.run_items({'world': [first]})
        self.run_items({'world': [second]}, NOW + timedelta(hours=1))
        category = self.news / pipeline.GROUP_PATHS['world']
        latest = (category / 'README.md').read_text(encoding='utf-8')
        daily = (category / '날짜별' / '2026' / '2026-10-29.md').read_text(encoding='utf-8')
        for address in (first['url'], second['url']):
            self.assertIn(address, latest)
            self.assertIn(address, daily)

    def test_next_day_leaves_yesterdays_archive_bytes_and_mtime_unchanged(self):
        first = article()
        self.run_items({'world': [first]})
        category = self.news / pipeline.GROUP_PATHS['world']
        yesterday = category / '날짜별' / '2026' / '2026-10-29.md'
        before = yesterday.read_bytes(), yesterday.stat().st_mtime_ns
        tomorrow = NOW + timedelta(days=1)
        second = article('Election results announced', url='https://news.example.org/election',
                         excerpt='Election results were announced.', published=tomorrow - timedelta(minutes=5))
        self.run_items({'world': [second]}, tomorrow)
        self.assertEqual((yesterday.read_bytes(), yesterday.stat().st_mtime_ns), before)
        self.assertTrue((category / '날짜별' / '2026' / '2026-10-30.md').is_file())

    def test_partial_source_failure_still_publishes_available_new_story(self):
        result = self.run_items({'world': [article()]}, states={'korea': 'network_error'})
        self.assertTrue(result['changed'])
        self.assertTrue((self.news / pipeline.GROUP_PATHS['world'] / 'README.md').is_file())
        self.assertEqual(result['sources'][1]['state'], 'network_error')

    def test_total_failure_preserves_all_previous_files(self):
        self.run_items({'world': [article()]})
        self.translator.reset_mock()
        before = snapshots(self.root)
        with self.assertRaises(RuntimeError):
            self.run_items({}, NOW + timedelta(hours=1),
                           states={'world': 'network_error', 'korea': 'http_error'})
        self.assertEqual(snapshots(self.root), before)
        self.translator.translate.assert_not_called()

    def test_english_link_only_source_keeps_original_title_and_link_only(self):
        config = {'sources': [source('links', mode='link_only')], 'new_items_per_group': 10}
        item = article()
        result = pipeline.run(config, self.state, self.news, NOW,
            translator=self.translator, fetcher=fetcher_for({'links': [item]}))
        self.assertTrue(result['changed'])
        self.translator.translate.assert_not_called()
        text = (self.news / pipeline.GROUP_PATHS['world'] / 'README.md').read_text(encoding='utf-8')
        self.assertIn(item['title'], text)
        self.assertIn(item['url'], text)
        self.assertNotIn(item['excerpt'], text)
        self.assertNotIn('자동번역', text)
        self.assertNotIn('한국어 번역', text)

    def test_native_korean_feed_preserves_short_excerpt_and_original_attribution(self):
        item = article('중앙은행, 기준금리 3% 동결',
            excerpt='중앙은행은 기준금리를 3%로 유지했습니다.')
        item['credit'] = '공식 작성자'
        result = self.run_items({'world': [item]})
        self.assertTrue(result['changed'])
        self.translator.translate.assert_not_called()
        text = (self.news / pipeline.GROUP_PATHS['world'] / 'README.md').read_text(encoding='utf-8')
        self.assertIn(item['title'], text)
        self.assertIn(item['excerpt'], text)
        self.assertIn(item['url'], text)
        self.assertIn('출처:', text)
        self.assertIn('공식 작성자', text)
        self.assertNotIn('자동번역', text)
        saved = next(iter(pipeline.load_state(self.state)['articles'].values()))
        self.assertEqual(saved['title'], item['title'])
        self.assertEqual(saved['excerpt'], item['excerpt'])
        self.assertNotIn('title_ko', saved)
        self.assertNotIn('summary_ko', saved)


if __name__ == '__main__':
    unittest.main()
