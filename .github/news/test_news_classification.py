"""공식 분야 분류와 분류 정정 뒤 재게시 방지를 검사합니다."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

import collect_news as core
import news_pipeline as pipeline


NOW = datetime(2026, 11, 2, 8, tzinfo=timezone.utc)
SBS = {
    'id': 'sbs', 'name': 'SBS 뉴스', 'group': 'korea',
    'homepage': 'https://news.sbs.co.kr/', 'article_hosts': ['news.sbs.co.kr'],
    'news_mode': True, 'summary_mode': 'feed',
    'category_groups': {'국제': 'world', '사회': 'korea'},
}


class ClassificationTests(unittest.TestCase):
    def test_first_category_is_official_section_not_later_keywords(self):
        item = ET.fromstring('<item><category>사회</category><category>국제</category></item>')
        self.assertEqual(core.article_classification(item, SBS, 'https://news.sbs.co.kr/a'),
                         {'group': 'korea', 'classification_basis': 'rss_category:사회'})

    def test_unknown_first_category_does_not_promote_a_later_keyword(self):
        item = ET.fromstring('<item><category>특집</category><category>국제</category></item>')
        self.assertEqual(core.article_classification(item, SBS, 'https://news.sbs.co.kr/a'), {})

    def test_rss_international_item_overrides_domestic_source(self):
        data = b'''<rss><channel><item><title>Foreign election result</title>
        <link>https://news.sbs.co.kr/a</link><pubDate>Mon, 02 Nov 2026 07:00:00 GMT</pubDate>
        <category>&#44397;&#51228;</category></item></channel></rss>'''
        items, _ = core.parse_feed(data, SBS, NOW)
        self.assertEqual(items[0]['group'], 'world')
        report = {'source': SBS, 'items': items}
        selected = pipeline.pick_candidates([report], {'articles': {}}, NOW)
        self.assertEqual(selected[0]['group'], 'world')

    def test_atom_category_term_is_read(self):
        item = ET.fromstring('<entry xmlns="http://www.w3.org/2005/Atom"><category term="국제"/></entry>')
        self.assertEqual(core.article_classification(item, SBS, 'https://news.sbs.co.kr/a')['group'], 'world')

    def test_only_official_url_path_is_used(self):
        source = {'article_path_groups': {'/news/Inter/': 'world'}}
        node = ET.fromstring('<item/>')
        self.assertEqual(core.article_classification(node, source, 'https://www.donga.com/news/Inter/article/a')['group'], 'world')
        self.assertEqual(core.article_classification(node, source, 'https://www.donga.com/news/Economy/a?section=/news/Inter/'), {})
        self.assertEqual(core.article_classification(node, source, 'https://www.donga.com/news/Interesting/a'), {})

    def test_official_category_takes_precedence_over_path(self):
        source = dict(SBS, article_path_groups={'/news/Inter/': 'world'})
        node = ET.fromstring('<item><category>사회</category></item>')
        self.assertEqual(core.article_classification(node, source, 'https://news.sbs.co.kr/news/Inter/a')['group'], 'korea')

    def test_voa_uses_primary_section_with_cross_listed_peninsula_articles(self):
        config = core.load_config(Path(__file__).with_name('sources.json'))
        source = next(item for item in config['sources'] if item['id'] == 'voa-ko-peninsula')
        world = ET.fromstring('<item><category>미국</category><category>한반도</category></item>')
        korea = ET.fromstring('<item><category>한반도</category><category>미국</category></item>')
        self.assertEqual(core.article_classification(world, source, 'https://www.voakorea.com/a/1')['group'], 'world')
        self.assertEqual(core.article_classification(korea, source, 'https://www.voakorea.com/a/2')['group'], 'korea')

    def test_legacy_renderer_uses_the_same_item_classification(self):
        item = {'title': '분류 확인용 제목', 'url': 'https://news.sbs.co.kr/a',
                'published_at': NOW.isoformat(), 'group': 'world'}
        text = core.render([{'source': SBS, 'state': 'ok'}], {'sbs': [item]}, NOW)
        self.assertIn('분류 확인용 제목', text.split('## 한국 뉴스')[0])
        self.assertNotIn('분류 확인용 제목', text.split('## 한국 뉴스')[1])

    def test_legacy_publishability_counts_distinct_sources_in_item_group(self):
        other = dict(SBS, id='other', group='world')
        reports = [{'source': SBS}, {'source': other}]
        selected = {'sbs': [{'group': 'world'}, {'group': 'world'}, {'group': 'korea'}],
                    'other': []}
        self.assertFalse(core.publishable(reports, selected))
        selected['other'] = [{'group': 'world'}]
        self.assertTrue(core.publishable(reports, selected))

    def test_only_classification_change_does_not_republish_old_article(self):
        old = {'title': '기사 원제', 'url': 'https://news.sbs.co.kr/a', 'published_at': NOW.isoformat(),
               'seen_at': NOW.isoformat(), 'day': '2026-11-01', 'group': 'korea'}
        state = {'articles': {old['url']: deepcopy(old)}}
        before = deepcopy(state)
        item = dict(old, group='world', classification_basis='rss_category:국제')
        self.assertEqual(pipeline.pick_candidates([{'source': SBS, 'items': [item]}], state, NOW), [])
        self.assertEqual(state, before)

    def test_classification_change_does_not_change_observed_fingerprint(self):
        item = {'title': '기사 원제', 'url': 'https://news.sbs.co.kr/a', 'group': 'korea'}
        self.assertEqual(pipeline.fingerprint(item), pipeline.fingerprint(dict(item, group='world')))

    def test_published_source_groups_and_retired_ambiguous_feed(self):
        config = core.load_config(Path(__file__).with_name('sources.json'))
        sources = {source['id']: source for source in config['sources']}
        self.assertEqual(sources['voa-ko-peninsula']['group'], 'korea')
        self.assertEqual(sources['voa-ko-world']['group'], 'world')
        self.assertNotIn('yonhap', sources)
        self.assertIn('yonhap-world', sources)
        self.assertIn('yonhap-society', sources)

    def test_bad_classification_mapping_is_rejected(self):
        config = json.loads(Path(__file__).with_name('sources.json').read_text(encoding='utf-8'))
        config['sources'][0]['category_groups'] = {'국제': 'unlisted-group'}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'sources.json'
            path.write_text(json.dumps(config), encoding='utf-8')
            with self.assertRaises(ValueError):
                core.load_config(path)


class PublishedClassificationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.state = self.root / 'state.json'
        self.news = self.root / 'news'
        self.item = {'title': '해외 사고 구조 현황', 'url': 'https://news.sbs.co.kr/a',
                     'published_at': NOW.isoformat(), 'excerpt': '구조된 인원은 10명입니다.',
                     'group': 'korea', 'classification_basis': 'rss_category:사회'}

    def run_item(self, item, now=NOW, source=SBS):
        def fetcher(src, _now):
            return {'source': src, 'state': 'ok', 'items': [deepcopy(item)], 'stats': {}}
        return pipeline.run({'sources': [source]}, self.state, self.news, now, fetcher=fetcher)

    def views(self, group):
        root = self.news / pipeline.GROUP_PATHS[group]
        return [root / 'README.md', root / '날짜별' / '2026' / '2026-11-02.md']

    def test_substantive_update_moves_same_day_item_and_clears_old_group(self):
        self.run_item(self.item)
        updated = dict(self.item, group='world', classification_basis='rss_category:국제',
                       excerpt='구조된 인원은 12명입니다.')
        result = self.run_item(updated, NOW + timedelta(hours=1))
        self.assertEqual((result['new_articles'], result['updated_articles']), (0, 1))
        for path in self.views('korea'):
            text = path.read_text(encoding='utf-8')
            self.assertNotIn(self.item['url'], text)
            self.assertIn('기사 목록이 비어 있습니다.', text)
        for path in self.views('world'):
            text = path.read_text(encoding='utf-8')
            self.assertEqual(text.count(self.item['url']), 1)
            self.assertIn('12명', text)

    def test_classification_only_moves_item_without_new_content_or_history(self):
        self.run_item(self.item)
        original = deepcopy(pipeline.load_state(self.state)['articles'][self.item['url']])
        classified = dict(self.item, group='world', classification_basis='rss_category:국제')
        result = self.run_item(classified, NOW + timedelta(hours=1))
        self.assertTrue(result['changed'])
        self.assertEqual((result['new_articles'], result['updated_articles'], result['reclassified_articles']), (0, 0, 1))
        saved = pipeline.load_state(self.state)['articles'][self.item['url']]
        expected = dict(original, group='world', classification_basis='rss_category:국제')
        self.assertEqual(saved, expected)
        for path in self.views('korea'):
            self.assertNotIn(self.item['url'], path.read_text(encoding='utf-8'))
        for path in self.views('world'):
            self.assertIn(self.item['url'], path.read_text(encoding='utf-8'))
        before = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in self.news.rglob('*.md')}
        again = self.run_item(classified, NOW + timedelta(hours=2))
        self.assertFalse(again['changed'])
        self.assertEqual(before, {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in self.news.rglob('*.md')})

    def test_classification_only_does_not_rewrite_previous_day_archives(self):
        self.run_item(self.item)
        before = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in self.news.rglob('*.md')}
        classified = dict(self.item, group='world', classification_basis='rss_category:국제')
        result = self.run_item(classified, NOW + timedelta(days=1))
        self.assertFalse(result['changed'])
        self.assertEqual(result['reclassified_articles'], 0)
        self.assertEqual(before, {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in self.news.rglob('*.md')})
        updated = dict(classified, excerpt='구조된 인원은 12명입니다.')
        result = self.run_item(updated, NOW + timedelta(days=1, hours=1))
        self.assertEqual(result['updated_articles'], 1)
        for path, snapshot in before.items():
            self.assertEqual((path.read_bytes(), path.stat().st_mtime_ns), snapshot)

    def test_another_source_cannot_move_an_unchanged_item(self):
        self.run_item(self.item)
        classified = dict(self.item, group='world', classification_basis='rss_category:국제')
        result = self.run_item(classified, NOW + timedelta(hours=1), dict(SBS, id='another-feed'))
        self.assertFalse(result['changed'])
        self.assertEqual(pipeline.load_state(self.state)['articles'][self.item['url']]['group'], 'korea')


if __name__ == '__main__':
    unittest.main()
