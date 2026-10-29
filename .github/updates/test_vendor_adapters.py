"""Offline fixtures for tool release and KISA notice parsing."""
import json
import unittest
import vendor_adapters as v


class VendorAdapterTests(unittest.TestCase):
    def github(self):
        return {'adapter': 'github_releases', 'group': 'tools', 'repository': 'org/tool',
                'hosts': ['api.github.com', 'github.com']}

    def release(self, **changes):
        row = {'id': 10, 'name': 'Tool 4.5.0', 'tag_name': 'v4.5.0', 'draft': False,
               'prerelease': False, 'published_at': '2026-10-28T22:23:36Z',
               'created_at': '2026-10-01T00:00:00Z', 'updated_at': '2026-10-29T01:00:00Z',
               'html_url': 'https://github.com/org/tool/releases/tag/v4.5.0',
               'body': '# Tool 4.5\n\nThis release updates firmware support and corrects scheduling defects.\n\n## Changes\n- Full PR list'}
        row.update(changes)
        return row

    def test_github_uses_published_at_and_short_intro(self):
        item = v.discover(self.github(), json.dumps([self.release()]))[0]
        self.assertEqual(item['date'], '2026-10-28T22:23:36+00:00')
        self.assertEqual(item['source_item_id'], '10')
        self.assertNotIn('Full PR list', item['description'])

    def test_unpublished_and_preview_versions_are_excluded(self):
        rows = [self.release(draft=True), self.release(prerelease=True),
                self.release(name='Tool nightly', tag_name='nightly'),
                self.release(name='Tool candidate 1', tag_name='v5.0.0-rc1')]
        self.assertEqual(v.discover(self.github(), json.dumps(rows)), [])

    def test_wrong_repository_or_host_cannot_enter_release_list(self):
        rows = [self.release(html_url='https://github.com/other/tool/releases/tag/v4.5.0'),
                self.release(html_url='https://evil.invalid/org/tool/releases/tag/v4.5.0')]
        self.assertEqual(v.discover(self.github(), json.dumps(rows)), [])

    def test_creation_or_update_date_is_not_a_substitute_for_release(self):
        self.assertEqual(v.discover(self.github(), json.dumps([self.release(published_at=None)])), [])

    def test_invalid_response_and_adapter_fail_explicitly(self):
        with self.assertRaises(ValueError):
            v.discover(self.github(), '{}')
        with self.assertRaises(ValueError):
            v.discover({'adapter': 'unrecognized'}, '[]')

    def test_duplicate_release_urls_are_one_item(self):
        self.assertEqual(len(v.discover(self.github(), json.dumps([self.release(), self.release()]))), 1)

    def test_python_stable_release_vs_preview_and_meeting(self):
        source = {'adapter': 'python_releases', 'group': 'tools', 'hosts': ['blog.python.org']}
        base = {'url': 'https://blog.python.org/2026/10/release/', 'categories': ['releases']}
        self.assertTrue(v.eligible(source, dict(base, title='Python 3.15.2 and 3.14.10 are out')))
        self.assertFalse(v.eligible(source, dict(base, title='Python 3.16.0 alpha 1 is now available')))
        self.assertFalse(v.eligible(source, dict(base, title='Python 3.16.0a1 is now available')))
        self.assertFalse(v.eligible(source, dict(base, title='Python Language Summit 2026')))

    def test_publisher_technical_article_is_not_an_event_registration(self):
        source = {'adapter': 'vendor_feed', 'group': 'products', 'hosts': ['blog.st.com']}
        self.assertTrue(v.eligible(source, {'url': 'https://blog.st.com/touchgfx/', 'title': 'TouchGFX 4.27 hybrid double buffering'}))
        self.assertFalse(v.eligible(source, {'url': 'https://blog.st.com/register/', 'title': 'Register now for our webinar'}))

    def test_kisa_reads_only_the_overview_not_affected_version_table(self):
        source = {'adapter': 'kisa_notice'}
        doc = '''<section id="View"><div class="board"><header><div class="b_title">
        <h2>Example 제품 보안 업데이트 권고</h2><span>2026-10-29</span></div></header>
        <div class="content_html"><p>□ 개요<br>o 보안 업데이트를 발표하였습니다.</p>
        <p>□ 설명<br>CVE-2026-11111</p><table><tr><td>affected 1.0</td></tr></table>
        <script>steal()</script></div></div></section>'''
        item = v.detail(source, doc, 'https://www.boho.or.kr/kr/bbs/view.do?nttId=1')
        self.assertEqual(item['date'], '2026-10-29')
        self.assertEqual(item['description'], '보안 업데이트를 발표하였습니다.')
        self.assertNotIn('CVE', item['description'])
        self.assertNotIn('steal', item['description'])

    def test_kisa_missing_structure_is_not_reported_as_successful_empty_notice(self):
        with self.assertRaises(ValueError):
            v.detail({'adapter': 'kisa_notice'}, '<html>login page</html>', 'https://www.boho.or.kr/')

    def test_other_feeds_do_not_require_a_detail_page(self):
        self.assertEqual(v.detail({'adapter': 'vendor_feed'}, '<html/>', 'https://blog.st.com/'), {})


if __name__ == '__main__':
    unittest.main()
