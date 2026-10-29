from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import update_pipeline as p
from test_update_pipeline import NOW, SOURCE, item as source_item, feed


class ReviewedItemsTests(unittest.TestCase):
    def test_collection_applies_review_and_never_reposts_an_excluded_item(self):
        row = source_item()
        key = p.publication_key('reports', row['url'])
        for action, expected in [('keep', 1), ('exclude', 0)]:
            with self.subTest(action=action), tempfile.TemporaryDirectory() as temporary:
                repo = Path(temporary)
                state_path = repo / 'state.json'
                config = {'sources': [dict(SOURCE)], 'initial_days': 45, 'initial_per_source': 3,
                          'reviews': {key: {'action': action, 'fingerprint': p.fingerprint(row),
                                           'fields': {'summary_ko': '대조한 소개입니다.', 'summary_mode': '공식 원문을 대조한 한국어 소개'}}}}
                with patch.dict(p.ADAPTERS, {'reports': SimpleNamespace()}):
                    result = p.run(config, state_path, repo, NOW, lambda url, hosts: (feed([row]), url))
                    self.assertEqual(result['new_or_updated'], expected)
                    again = p.run(config, state_path, repo, NOW, lambda url, hosts: (feed([row]), url))
                    self.assertEqual(again['new_or_updated'], 0)
                if action == 'keep':
                    body = (repo / p.GROUPS['reports'][0] / '새소식_updates/README.md').read_text(encoding='utf-8')
                    self.assertIn('대조한 소개입니다.', body)
                else:
                    self.assertFalse((repo / p.GROUPS['reports'][0]).exists())

    def test_source_change_does_not_inherit_a_stale_review(self):
        item = {'url': 'https://example.org/article', 'title': 'Updated source', 'summary_ko': 'Automatic guide'}
        review = {'action': 'keep', 'fingerprint': 'reviewed-content',
                  'fields': {'summary_ko': 'Checked introduction'}}
        self.assertEqual(p.reviewed_item(item, review, 'reviewed-content')['summary_ko'], 'Checked introduction')
        self.assertEqual(p.reviewed_item(item, review, 'changed-content')['summary_ko'], 'Automatic guide')
        self.assertEqual(item['summary_ko'], 'Automatic guide')

    def test_review_cannot_replace_an_original_link_with_another_page(self):
        with self.assertRaises(ValueError):
            p.reviewed_item({'url': 'https://example.org/a'},
                            {'action': 'keep', 'fingerprint': 'x', 'fields': {'url': 'https://example.org/b'}}, 'x')

    def test_ministry_name_in_description_is_not_an_energy_technology_match(self):
        source = next(s for s in p.load_config()['sources'] if s['id'] == 'mcee-energy')
        adapter = SimpleNamespace()
        for title in ('도시 침수 예방을 위한 하수도정비 중점관리지역 11곳 지정', '원전 공론화평가단 구성'):
            self.assertFalse(p.eligible(source, {'title': title, 'description': '기후에너지환경부 보도자료입니다.'}, adapter))
        self.assertTrue(p.eligible(source, {'title': '산업용 히트펌프 기술개발·실증 지원', 'description': ''}, adapter))

    def test_feed_metadata_is_labelled_as_feed_metadata(self):
        text = '<rss><channel><item><title>A</title><link>https://example.org/a</link><author>Feed editor</author></item></channel></rss>'
        self.assertEqual(p.parse_feed(text)[0]['author_label'], 'RSS·Atom 표기 작성자')

    def test_page_date_and_feed_time_are_displayed_separately(self):
        item = {'key': 'tools:x', 'title': 'Checked title', 'url': 'https://example.org/a',
                'date': '2026-10-27', 'date_label': '원문 게시일', 'feed_date': '2026-10-27T22:00:00Z',
                'summary_ko': '원문을 읽고 작성한 소개입니다.', 'summary_mode': '공식 원문을 대조한 한국어 소개',
                'source_name': 'Official site', 'homepage': 'https://example.org/',
                'author': 'Article writer', 'author_label': '원문 작성자'}
        output = p.render([item], 'tools', '2026-10-29 16:00', '')
        self.assertIn('원문 게시일: 2026-10-27', output)
        self.assertIn('RSS·Atom 발행 시각: 2026-10-28 07:00 KST', output)
        self.assertNotIn('> 원문을 읽고', output)

    def test_rebuilding_todays_page_keeps_earlier_reviewed_introduction(self):
        now = datetime(2026, 10, 29, 7, tzinfo=timezone.utc)
        def item(key, intro):
            return {'key': key, 'group': 'tools', 'title': key, 'url': 'https://example.org/' + key,
                    'date': '2026-10-29', 'summary_ko': intro, 'summary_mode': '공식 원문을 대조한 한국어 소개',
                    'source_name': 'Official site', 'homepage': 'https://example.org/'}
        checked = item('checked', '본문을 대조한 설명입니다.')
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            state = {'days': {'tools': {'2026-10-29': [checked]}}}
            analysis = repo / p.GROUPS['tools'][0] / 'existing.md'
            analysis.parent.mkdir(parents=True)
            analysis.write_bytes(b'Existing explanation\n')
            p.publish(repo, state, [item('new', '새 자료 소개입니다.')], now)
            body = (analysis.parent / '새자료_inbox/README.md').read_text(encoding='utf-8')
            self.assertIn(checked['summary_ko'], body)
            self.assertEqual(analysis.read_bytes(), b'Existing explanation\n')


if __name__ == '__main__':
    unittest.main()
