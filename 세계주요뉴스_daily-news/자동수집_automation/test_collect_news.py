"""실제 네트워크 없이 뉴스 수집기의 날짜·표시·실패 처리 계약을 검사합니다."""
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from http.client import IncompleteRead
from io import BytesIO
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError
from xml.sax.saxutils import escape

import collect_news as news


NOW = datetime(2026, 10, 29, 0, 0, tzinfo=timezone.utc)


def source(identifier='world-a', group='world'):
    return {
        'id': identifier, 'name': identifier, 'group': group,
        'homepage': 'https://news.example.org/',
        'feed_url': 'https://news.example.org/feed.xml',
        'feed_hosts': ['news.example.org'], 'article_hosts': ['news.example.org'],
    }


def article(title='Example headline', url='https://news.example.org/story', published=None):
    timestamp = published if published is not None else format_datetime(NOW - timedelta(hours=1))
    return ('<item><title>' + escape(title) + '</title><link>' + escape(url) + '</link>'
            '<pubDate>' + escape(timestamp) + '</pubDate>'
            '<description>BODY_MUST_NOT_APPEAR</description></item>')


def feed(*items):
    return ('<rss version="2.0"><channel>' + ''.join(items) + '</channel></rss>').encode()


def report(src, items=None, state='ok'):
    return {'source': src, 'items': items or [], 'state': state, 'stats': {}}


def parsed_item(identifier):
    return {'title': 'Example ' + identifier, 'url': 'https://news.example.org/' + identifier,
            'published_at': (NOW - timedelta(hours=1)).isoformat()}


class FeedDateTests(unittest.TestCase):
    def test_rfc822_edt_converts_to_known_utc_time(self):
        self.assertEqual(news.date_value('Wed, 28 Oct 2026 17:15:56 EDT'),
                         datetime(2026, 10, 28, 21, 15, 56, tzinfo=timezone.utc))

    def test_iso8601_kst_and_z_refer_to_same_instant(self):
        self.assertEqual(news.date_value('2026-10-29T08:30:00+09:00'),
                         news.date_value('2026-10-28T23:30:00Z'))

    def test_missing_invalid_and_naive_dates_are_not_replaced_with_now(self):
        for value in (None, '', 'not a date', '2026-10-29T08:30:00'):
            with self.subTest(value=value):
                self.assertIsNone(news.date_value(value))

    def test_timezone_conversion_outside_datetime_range_is_discarded(self):
        for value in ('0001-01-01T00:00:00+09:00', '9999-12-31T23:59:59-09:00'):
            with self.subTest(value=value):
                self.assertIsNone(news.date_value(value))

    def test_cutoff_is_inclusive_and_future_old_items_are_excluded(self):
        items, stats = news.parse_feed(feed(
            article('At cutoff', 'https://news.example.org/cutoff',
                    format_datetime(NOW - timedelta(hours=24))),
            article('Too old', 'https://news.example.org/old',
                    format_datetime(NOW - timedelta(hours=24, seconds=1))),
            article('Future', 'https://news.example.org/future',
                    format_datetime(NOW + timedelta(seconds=1)))), source(), NOW)
        self.assertEqual([i['title'] for i in items], ['At cutoff'])
        self.assertEqual((stats['old'], stats['future']), (1, 1))

    def test_channel_build_date_does_not_supply_missing_article_date(self):
        data = ('<rss><channel><lastBuildDate>Thu, 29 Oct 2026 00:00:00 GMT</lastBuildDate>'
                '<item><title>No date</title><link>https://news.example.org/story</link>'
                '</item></channel></rss>').encode()
        items, stats = news.parse_feed(data, source(), NOW)
        self.assertEqual(items, [])
        self.assertEqual(stats['invalid'], 1)


class FeedFormatTests(unittest.TestCase):
    def test_rss_publishes_title_and_original_link_without_article_body(self):
        url = 'https://news.example.org/story?utm_source=rss&ref=homepage'
        items, _ = news.parse_feed(feed(article('A & B', url)), source(), NOW)
        self.assertEqual(items[0]['title'], 'A & B')
        self.assertEqual(items[0]['url'], url)
        self.assertEqual(set(items[0]), {'title', 'url', 'published_at'})

    def test_npr_provider_credit_is_preserved_and_displayed_as_escaped_text(self):
        provider = 'Associated Press <b>desk</b>'
        data = ('<rss xmlns:dc="http://purl.org/dc/elements/1.1/"><channel>'
                + article(url='https://www.npr.org/example').replace(
                    '</item>', '<dc:creator>' + escape(provider) + '</dc:creator></item>')
                + '</channel></rss>').encode()
        npr = source('npr')
        npr.update(name='NPR', homepage='https://www.npr.org/', article_hosts=['npr.org'])
        items, _ = news.parse_feed(data, npr, NOW)
        self.assertEqual(items[0]['credit'], provider)
        text = news.render([report(npr, items)], {'npr': items}, NOW)
        self.assertIn('[NPR](https://www.npr.org/)', text)
        self.assertIn('Associated Press &lt;b&gt;desk&lt;/b&gt;', text)
        self.assertNotIn('<b>', text)
        self.assertNotIn('BODY_MUST_NOT_APPEAR', text)

    def test_atom_uses_alternate_article_link_instead_of_feed_self_link(self):
        data = b'''<feed xmlns="http://www.w3.org/2005/Atom"><entry>
          <title>Atom article</title><published>2026-10-28T23:00:00Z</published>
          <link rel="self" href="https://news.example.org/feed/entry.xml"/>
          <link rel="alternate" href="https://news.example.org/article"/>
          </entry></feed>'''
        items, _ = news.parse_feed(data, source(), NOW)
        self.assertEqual(items[0]['url'], 'https://news.example.org/article')

    def test_rdf_dublin_core_date_is_supported(self):
        data = b'''<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
          xmlns="http://purl.org/rss/1.0/" xmlns:dc="http://purl.org/dc/elements/1.1/">
          <item rdf:about="https://news.example.org/rdf-story"><title>RDF article</title>
          <link>https://news.example.org/rdf-story</link>
          <dc:date>2026-10-28T23:00:00Z</dc:date></item></rdf:RDF>'''
        items, _ = news.parse_feed(data, source(), NOW)
        self.assertEqual(items[0]['title'], 'RDF article')
        self.assertEqual(items[0]['published_at'], '2026-10-28T23:00:00+00:00')

    def test_malformed_html_dtd_and_oversized_input_are_rejected(self):
        for data in (b'<rss>', b'<html><body>Not RSS</body></html>',
                     b'<!DOCTYPE rss [<!ENTITY x "test">]><rss/>',
                     b'<?xml version="1.0" encoding="garbage"?><rss/>',
                     b'<?xml version="1.0" encoding="utf-32"?><rss/>',
                     b'\x00<rss/>', b'x' * (news.MAX_BYTES + 1)):
            with self.subTest(prefix=data[:25]):
                with self.assertRaises(news.FeedError):
                    news.parse_feed(data, source(), NOW)

    def test_duplicate_tracking_links_keep_one_original_entry(self):
        first = 'https://news.example.org/story?utm_source=a&id=9'
        second = 'https://news.example.org/story?utm_source=b&id=9'
        items, stats = news.parse_feed(feed(article('First', first), article('Second', second)),
                                       source(), NOW)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]['url'], first)
        self.assertEqual(stats['duplicates'], 1)

    def test_feed_order_is_retained_rather_than_fabricating_priority(self):
        data = feed(article('First in feed', 'https://news.example.org/first',
                            format_datetime(NOW - timedelta(hours=5))),
                    article('Newer but second', 'https://news.example.org/second'))
        items, _ = news.parse_feed(data, source(), NOW)
        self.assertEqual([i['title'] for i in items], ['First in feed', 'Newer but second'])


class AddressAndRenderingTests(unittest.TestCase):
    def test_only_approved_https_domains_and_subdomains_are_allowed(self):
        self.assertTrue(news.safe_url('https://news.example.org/a', ['example.org']))
        self.assertTrue(news.safe_url('https://www.news.example.org/a', ['news.example.org']))
        for address in ('http://news.example.org/a', 'javascript:alert(1)',
                        'https://news.example.org.attacker.invalid/a',
                        'https://news.example.org@attacker.invalid/a',
                        'https://user:password@news.example.org/a',
                        'https://127.0.0.1/a', 'https://[::1]/a',
                        'https://news.example.org:8080/a',
                        'https://news.example.org/a\nInjected',
                        'https://news.example.org\\@attacker.invalid/a'):
            with self.subTest(address=address):
                self.assertFalse(news.safe_url(address, ['news.example.org']))

    def test_redirect_is_rejected_before_following_unapproved_host(self):
        redirect = news.RestrictedRedirect(['news.example.org'])
        with self.assertRaises(news.FeedError):
            redirect.redirect_request(None, None, 302, 'Found', {}, 'https://127.0.0.1/')

    def test_markdown_and_html_in_title_are_visible_text_not_markup(self):
        item = parsed_item('markup')
        item['title'] = '**Bold** [fake](javascript:evil) <script>alert(1)</script> | row'
        reports = [report(source(), [item])]
        text = news.render(reports, {'world-a': [item]}, NOW)
        self.assertNotIn('<script>', text)
        self.assertNotIn('**Bold**', text)
        self.assertNotIn('[fake](javascript:', text)
        self.assertIn('&lt;script&gt;', text)
        self.assertIn('\\| row', text)

    def test_rendered_time_is_known_kst_and_has_source_credit(self):
        item = parsed_item('time')
        reports = [report(source(), [item])]
        text = news.render(reports, {'world-a': [item]}, NOW)
        self.assertIn('2026-10-29 09:00 KST', text)
        self.assertIn('10-29 08:00 KST', text)
        self.assertIn('[world-a](https://news.example.org/)', text)


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.sources = [source('world-a'), source('world-b'), source('korea-a', 'korea')]
        self.config = {'sources': self.sources, 'items_per_source': 4}

    def test_total_failure_preserves_previous_file_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'latest.md'
            original = b'Previously verified list\n'
            output.write_bytes(original)
            code, summary = news.run(self.config, output, NOW,
                fetcher=lambda src, now: report(src, state='network_error'))
            self.assertEqual(code, 1)
            self.assertFalse(summary['published'])
            self.assertEqual(output.read_bytes(), original)

    def test_missing_korean_coverage_does_not_replace_latest(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'latest.md'
            output.write_text('Previous', encoding='utf-8')
            def fake(src, now):
                return report(src, [parsed_item(src['id'])]) if src['group'] == 'world' else report(src, state='network_error')
            code, _ = news.run(self.config, output, NOW, fetcher=fake)
            self.assertEqual(code, 1)
            self.assertEqual(output.read_text(encoding='utf-8'), 'Previous')

    def test_partial_failure_publishes_remaining_sources_and_records_outage(self):
        failed = source('world-failed')
        config = {'sources': self.sources + [failed], 'items_per_source': 4}
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'latest.md'
            def fake(src, now):
                if src['id'] == 'world-failed':
                    return report(src, state='network_error')
                return report(src, [parsed_item(src['id'])])
            code, summary = news.run(config, output, NOW, fetcher=fake)
            self.assertEqual(code, 0)
            self.assertIn('연결 오류', output.read_text(encoding='utf-8'))
            self.assertEqual(summary['sources'][-1]['state'], 'network_error')
            self.assertTrue(all('items' not in r for r in summary['sources']))
            self.assertFalse(output.with_suffix('.md.tmp').exists())

    def test_same_article_across_sources_is_not_counted_as_two_sources(self):
        shared = parsed_item('shared')
        reports = [report(self.sources[0], [shared]), report(self.sources[1], [shared]),
                   report(self.sources[2], [parsed_item('domestic')])]
        selected = news.choose_items(reports, 4)
        self.assertFalse(news.publishable(reports, selected))

    def test_per_source_limit_does_not_publish_entire_feed(self):
        items = [parsed_item(str(i)) for i in range(20)]
        chosen = news.choose_items([report(self.sources[0], items)], 4)
        self.assertEqual([i['title'] for i in chosen['world-a']],
                         ['Example 0', 'Example 1', 'Example 2', 'Example 3'])


class NetworkResponseTests(unittest.TestCase):
    class Response(BytesIO):
        url = 'https://news.example.org/feed.xml'

    def test_http_retry_success_does_not_keep_previous_error_status(self):
        first = HTTPError('https://news.example.org/feed.xml', 503, 'Unavailable', {}, None)
        with patch.object(news, 'build_opener') as build, patch.object(news.time, 'sleep'):
            build.return_value.open.side_effect = [first, self.Response(feed(article()))]
            result = news.fetch_source(source(), NOW)
        self.assertEqual(result['state'], 'ok')
        self.assertIsNone(result.get('http_status'))

    def test_truncated_response_is_retried_without_aborting_other_sources(self):
        class BrokenResponse(self.Response):
            def read(self, *args):
                raise IncompleteRead(b'<rss>')
        with patch.object(news, 'build_opener') as build, patch.object(news.time, 'sleep'):
            build.return_value.open.side_effect = [BrokenResponse(), self.Response(feed(article()))]
            result = news.fetch_source(source(), NOW)
        self.assertEqual(result['state'], 'ok')
        self.assertEqual(len(result['items']), 1)

    def test_permanent_http_403_is_not_bypassed_or_retried(self):
        error = HTTPError('https://news.example.org/feed.xml', 403, 'Forbidden', {}, None)
        with patch.object(news, 'build_opener') as build, patch.object(news.time, 'sleep'):
            build.return_value.open.side_effect = error
            result = news.fetch_source(source(), NOW)
            self.assertEqual(build.return_value.open.call_count, 1)
        self.assertEqual(result['state'], 'http_error')
        self.assertEqual(result['http_status'], 403)

    def test_persistent_network_error_is_reported_after_bounded_attempts(self):
        with patch.object(news, 'build_opener') as build, patch.object(news.time, 'sleep'):
            build.return_value.open.side_effect = URLError('offline')
            result = news.fetch_source(source(), NOW)
            self.assertEqual(build.return_value.open.call_count, 2)
        self.assertEqual(result['state'], 'network_error')


if __name__ == '__main__':
    unittest.main()
