"""출처 확인은 원문 존재 검사이며 명령이나 모델을 실행하지 않습니다."""
import base64
import json
from unittest import TestCase
from unittest.mock import Mock
from urllib.error import HTTPError

import source_checks

COMMIT = 'a' * 40
ROOT = 'https://github.com/example/project/blob/' + COMMIT + '/'
README = '# Demo\n## 1. Install and set up\n``` bash\n# Prepare first\ninstall-tool\nstart-tool\n```\n## Usage\nRun `tool --help` or `tool --name a &amp; b`.\n<a id="custom-anchor"></a>\n'


def document(text=README, path='README.md'):
    return {'status': 'ok', 'text': text, 'sha': source_checks._blob_sha(text.encode()),
            'source_url': ROOT + path, 'commit': COMMIT, 'path': path}


def response(text):
    raw = text.encode()
    return json.dumps({'encoding': 'base64', 'content': base64.b64encode(raw).decode(),
                       'sha': source_checks._blob_sha(raw)}).encode(), 'application/json'


class SourceChecksTests(TestCase):
    def test_automatic_contiguous_fence_and_numbered_anchor(self):
        guide = {'method': source_checks.AUTOMATIC, 'sources': [{'url': ROOT + 'README.md'}],
                 'install_code': {'code': 'install-tool\nstart-tool',
                                  'source_url': ROOT + 'README.md#1-install-and-set-up'}}
        get = Mock(side_effect=AssertionError('Unexpected request'))
        report = source_checks.verify(guide, document(), get, '')
        self.assertEqual(report['documents_checked'], 1)
        self.assertEqual(report['commands_checked'], 1)
        self.assertEqual(report['command_checks'][0]['mode'], 'contiguous_fenced_excerpt')
        get.assert_not_called()

    def test_manual_inline_and_html_unescape(self):
        guide = {'method': '공식 문서 한국어 해설', 'example_code':
                 {'code': 'tool --help\ntool --name a & b', 'source_url': ROOT + 'README.md#custom-anchor'}}
        report = source_checks.verify(guide, document(), Mock(), '')
        self.assertEqual(report['command_checks'][0]['mode'], 'manual_line_presence_inline_table_or_fence')

    def test_manual_table_and_unquoted_html_anchor(self):
        text = '## Commands\n| Name | Command |\n| --- | --- |\n| Help | `tool --help` |\n<a name=help></a>\n'
        guide = {'example_code': {'code': 'tool --help', 'source_url': ROOT + 'README.md#help'}}
        self.assertEqual(source_checks.verify(guide, document(text), Mock(), '')['commands_checked'], 1)

    def test_modified_command_fails(self):
        for method in (source_checks.AUTOMATIC, '공식 문서 한국어 해설'):
            guide = {'method': method, 'install_code': {'code': 'install-evil', 'source_url': ROOT + 'README.md'}}
            with self.assertRaisesRegex(ValueError, 'Command does not match'):
                source_checks.verify(guide, document(), Mock(), '')

    def test_automatic_cannot_join_noncontiguous_lines(self):
        guide = {'method': source_checks.AUTOMATIC, 'install_code':
                 {'code': '# Prepare first\nstart-tool', 'source_url': ROOT + 'README.md'}}
        with self.assertRaises(ValueError):
            source_checks.verify(guide, document(), Mock(), '')

    def test_invalid_anchor_fails(self):
        with self.assertRaisesRegex(ValueError, 'anchor'):
            source_checks.verify({'sources': [{'url': ROOT + 'README.md#absent'}]}, document(), Mock(), '')

    def test_numbered_heading_collision_keeps_the_unique_github_slug(self):
        readme = document('## Install\n## Install-1\n## Install\n')
        report = source_checks.verify({'sources':[{'url':ROOT+'README.md#install-2'}]}, readme, Mock(), '')
        self.assertEqual(report['documents_checked'],1)

    def test_404_fails(self):
        get = Mock(side_effect=HTTPError('url', 404, 'Not found', None, None))
        with self.assertRaisesRegex(ValueError, 'Cannot verify'):
            source_checks.verify({'sources': [{'url': ROOT + 'missing.md'}]}, document(), get, '')

    def test_floating_ref_fails(self):
        with self.assertRaisesRegex(ValueError, 'fixed commit'):
            source_checks.verify({'sources': [{'url': ROOT.replace(COMMIT, 'main') + 'README.md'}]}, document(), Mock(), '')

    def test_fetch_once_and_reuse_cached_documents(self):
        extra = '## Setup\n```sh\nprepare-tool\n```\n'
        get = Mock(return_value=response(extra))
        guide = {'sources': [{'url': ROOT + 'docs/install.md#setup'}],
                 'install_code': {'code': 'prepare-tool', 'source_url': ROOT + 'docs/install.md#setup'},
                 'assessment': {'advantages_ko': [{'source_urls': [ROOT + 'docs/install.md']} ]}}
        report = source_checks.verify(guide, document(), get, 'test-token')
        get.assert_called_once_with('https://api.github.com/repos/example/project/contents/docs/install.md?ref=' + COMMIT, 'test-token')
        self.assertEqual(report['documents_checked'], 1)
        cached = document()
        cached['documents'] = [document(extra, 'docs/install.md')]
        get.reset_mock()
        source_checks.verify(guide, cached, get, '')
        get.assert_not_called()

    def test_hash_tampering_fails(self):
        broken = document()
        broken['text'] += 'tampered'
        with self.assertRaisesRegex(ValueError, 'SHA mismatch'):
            source_checks.verify({}, broken, Mock(), '')

    def test_unchecked_links_are_not_reported_as_reachable(self):
        guide = {'assessment': {'advantages_ko': [{'source_urls':
                 ['https://github.com/example/project#readme', 'https://example.org/docs']} ]}}
        report = source_checks.verify(guide, document(), Mock(), '')
        self.assertEqual(len(report['unchecked_urls']), 2)
        self.assertEqual(report['documents_checked'], 0)
        with self.assertRaises(ValueError):
            source_checks.verify({'sources': [{'url': 'javascript:alert(1)'}]}, document(), Mock(), '')

    def test_automatic_item_source_is_checked(self):
        guide = {'method': source_checks.AUTOMATIC, 'features':
                 [{'source_url': ROOT + 'README.md#missing', 'original': 'A tool'}]}
        with self.assertRaisesRegex(ValueError, 'anchor'):
            source_checks.verify(guide, document(), Mock(), '')

    def test_original_paragraph_and_section_must_match(self):
        text = '## Features\nA tool with two useful modes.\n## Usage\nRun the tool.\n'
        item = {'source_url': ROOT + 'README.md#features', 'heading': 'Features',
                'original': 'A tool with two useful modes.'}
        guide = {'method': source_checks.AUTOMATIC, 'features': [item]}
        self.assertEqual(source_checks.verify(guide, document(text), Mock(), '')['excerpts_checked'], 1)
        item['original'] = 'A tool with fake capabilities.'
        with self.assertRaisesRegex(ValueError, 'Original excerpt'):
            source_checks.verify(guide, document(text), Mock(), '')
        item['original'] = 'A tool with two useful modes.'
        item['heading'] = 'Usage'
        with self.assertRaisesRegex(ValueError, 'Original excerpt'):
            source_checks.verify(guide, document(text), Mock(), '')
