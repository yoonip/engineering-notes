"""README의 설치·예시 경계를 지키고 원문 명령을 바꾸지 않는지 검사합니다."""
import base64
import json
from unittest import TestCase
from unittest.mock import Mock
from urllib.error import HTTPError

import collect
import guides


README = '''# Project

A tool that converts office documents into Markdown files.

## Features

Read documents and preserve tables in generated Markdown output.

## Who is this for?

Developers who need to prepare documents for text processing.

## Installation

Use Python 3.12 or later in a fresh environment.

```sh
python -m pip install example-package
```

### Optional setup

```sh
example-package configure
```

## Usage

Convert a document and write the result into a file.

```sh
example-package input.docx --output result.md
```

## Uninstall

```sh
python -m pip uninstall example-package
```
'''


class ParserTests(TestCase):
    def test_install_and_usage_do_not_cross_into_each_other(self):
        parsed = guides.sections(README)
        install = guides.code_example(parsed, 'installation')
        usage = guides.code_example(parsed, 'examples')
        self.assertEqual(install['code'], 'python -m pip install example-package')
        self.assertEqual(usage['code'], 'example-package input.docx --output result.md')
        self.assertNotIn('Uninstall', [s['heading'] for s in guides.select_sections(parsed, 'installation')])

    def test_shell_comments_are_not_headings(self):
        parsed = guides.sections('## Install\n```bash\n# this is a shell comment\nrun-tool\n```\n## Usage\nUse it.\n')
        self.assertEqual([s['heading'] for s in parsed], ['Introduction', 'Install', 'Usage'])
        self.assertEqual(guides.code_example(parsed, 'installation')['code'], '# this is a shell comment\nrun-tool')

    def test_tilde_fences_and_setext_headings(self):
        parsed = guides.sections('Installation\n------------\n~~~bash\ninstall-tool\n~~~\n')
        self.assertEqual(guides.code_example(parsed, 'installation')['code'], 'install-tool')

    def test_spaced_fence_keeps_shell_comments_and_following_heading(self):
        parsed = guides.sections('## Build from source\n``` bash\n# Keep this exported\nexport ENGINE=nvidia\n./build.sh\n```\n### Offline inference\n``` bash\npython examples/offline_inference.py\n```')
        self.assertEqual([s['heading'] for s in parsed], ['Introduction','Build from source','Offline inference'])
        self.assertEqual(parsed[1]['codes'][0]['language'], 'bash')
        self.assertEqual(parsed[1]['codes'][0]['code'], '# Keep this exported\nexport ENGINE=nvidia\n./build.sh')
        self.assertEqual(parsed[2]['codes'][0]['code'], 'python examples/offline_inference.py')

    def test_numbered_heading_is_not_treated_as_a_list_item(self):
        parsed = guides.sections('## 1. Install and set up\nInstall the package.')
        self.assertEqual(parsed[1]['heading'], '1. Install and set up')

    def test_long_first_step_does_not_expose_only_a_later_step(self):
        text='## Installation\n```sh\n'+'\n'.join('prepare-environment' for _ in range(16))+'\n```\n```sh\nstart-server\n```'
        self.assertIsNone(guides.code_example(guides.sections(text),'installation'))

    def test_prerequisite_script_is_not_skipped_before_install(self):
        text='## Installation\n### Prerequisites\nPrepare the required certificate.\n```sh\n'+'\n'.join('prepare-certificate' for _ in range(16))+'\n```\n### Install package\n```sh\ninstall-tool\n```'
        self.assertIsNone(guides.code_example(guides.sections(text),'installation'))

    def test_usage_nested_under_installation_is_not_an_install_step(self):
        parsed=guides.sections('## Installation\n### Usage\n```sh\nstart-server\n```\n### Windows\n```powershell\ninstall-tool.ps1\n```')
        self.assertEqual(guides.code_example(parsed,'installation')['code'],'install-tool.ps1')
        self.assertEqual(guides.code_example(parsed,'examples')['code'],'start-server')

    def test_install_scope_stops_at_another_document(self):
        parsed=guides.sections('## Installation\nPrepare Python.')
        for s in parsed:s['source_url']='first'
        second=guides.sections('### Run\n```sh\nstart-server\n```')
        for s in second:s['source_url']='second'
        self.assertIsNone(guides.code_example(parsed+second,'installation'))

    def test_incomplete_or_long_script_is_not_truncated_into_a_command(self):
        self.assertIsNone(guides.code_example(guides.sections('## Install\n```sh\nincomplete'), 'installation'))
        text = '## Install\n```sh\n' + '\n'.join('run-tool' for _ in range(16)) + '\n```'
        self.assertIsNone(guides.code_example(guides.sections(text), 'installation'))

    def test_no_install_command_is_invented_from_package_names(self):
        parsed = guides.sections('# FancyProject\nA new Python package.\n## Features\nDoes useful work.')
        self.assertIsNone(guides.code_example(parsed, 'installation'))

    def test_nested_prerequisites_do_not_hide_sibling_platform_installation(self):
        parsed = guides.sections('## Install\n### Prerequisites\nRequires Python 3.12.\n### Windows\nUse PowerShell.\n```powershell\ninstall-tool.ps1\n```')
        self.assertEqual(guides.code_example(parsed, 'installation')['code'], 'install-tool.ps1')
        self.assertEqual(guides.excerpts(parsed, 'installation')[0]['original'], 'Requires Python 3.12.')

    def test_plain_keeps_version_numbers_and_3d_words(self):
        self.assertEqual(guides.plain('3D graphics and version 2.0'), '3D graphics and version 2.0')
        self.assertEqual(guides.plain('1. Requires Python 3.12'), 'Requires Python 3.12')


class SourceTests(TestCase):
    def setUp(self):
        self.repo = {'id': 12, 'full_name': 'owner/project', 'html_url': 'https://github.com/owner/project',
                     'default_branch': 'release/stable'}
        self.commit = 'a' * 40

    def test_readme_is_requested_at_a_fixed_commit_and_links_preserve_path(self):
        getter = Mock(side_effect=[(json.dumps({'object': {'sha': self.commit}}).encode(), ''),
                      (json.dumps({'encoding': 'base64', 'content': base64.b64encode(README.encode()).decode(),
                                   'path': 'docs/README.md', 'sha': 'b' * 40}).encode(), '')])
        readme = guides.fetch_readme(self.repo, 'test-token', getter)
        self.assertIn('heads/release%2Fstable', getter.call_args_list[0].args[0])
        self.assertIn('readme?ref=' + self.commit, getter.call_args_list[1].args[0])
        self.assertEqual(readme['text'], README)
        self.assertEqual(readme['source_url'], self.repo['html_url'] + '/blob/' + self.commit + '/docs/README.md')

    def test_missing_readme_records_missing_instead_of_a_network_failure(self):
        getter = Mock(side_effect=[(json.dumps({'object': {'sha': self.commit}}).encode(), ''),
                                  HTTPError('https://api.github.com/', 404, 'Not found', {}, None)])
        readme = guides.fetch_readme(self.repo, '', getter)
        self.assertEqual(readme['status'], 'not_found')
        self.assertEqual(readme['text'], '')

    def test_permission_or_server_error_is_not_misreported_as_no_readme(self):
        for status in (403, 503):
            getter = Mock(side_effect=[(json.dumps({'object': {'sha': self.commit}}).encode(), ''),
                                      HTTPError('https://api.github.com/', status, 'Failed', {}, None)])
            with self.assertRaises(HTTPError):
                guides.fetch_readme(self.repo, '', getter)

    def test_linked_install_document_stays_in_same_repository_and_commit(self):
        readme = {'text': '[Install](docs/install.md) [Unsafe](../../install.md) [External](https://other.example/install.md)',
                  'path': 'README.md', 'commit': self.commit}
        payload = {'encoding': 'base64', 'content': base64.b64encode(b'## Install\n```sh\nrun-install\n```').decode(), 'sha': 'c' * 40}
        getter = Mock(return_value=(json.dumps(payload).encode(), ''))
        docs = guides.linked_documents(self.repo, readme, '', getter)
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0]['path'], 'docs/install.md')
        self.assertIn('contents/docs/install.md?ref=' + self.commit, getter.call_args.args[0])
        self.assertEqual(getter.call_count, 1)


class GuideTests(TestCase):
    def setUp(self):
        self.repo = {'id': 12, 'full_name': 'owner/project', 'html_url': 'https://github.com/owner/project'}
        self.readme = {'text': README, 'sha': 'b' * 40, 'commit': 'a' * 40, 'fetched_at': '2026-11-02T00:00:00Z',
                       'source_url': self.repo['html_url'] + '/blob/' + 'a' * 40 + '/README.md'}
        self.translations = Mock()
        self.translations.translate.side_effect = lambda source: {'text': '공식 문서에서 가져온 설명입니다.', 'method': 'test CPU translator'}

    def test_new_project_gets_all_four_sections_and_unmodified_commands(self):
        guide = guides.make_guide(self.repo, self.readme, {}, self.translations)
        output = '\n'.join(guides.render_guide(guide, collect.clean))
        for heading in ('어떤 일을 하나요', '누구에게 유용한가요', '설치 방법', '사용 예시'):
            self.assertIn('### ' + heading, output)
        self.assertIn('python -m pip install example-package', output)
        self.assertIn('example-package input.docx --output result.md', output)
        self.assertNotIn('pip uninstall', output)
        # 번역기에는 명령이 아닌 자연어 구간만 전달합니다.
        inputs = [call.args[0] for call in self.translations.translate.call_args_list]
        self.assertFalse(any('pip install' in source or '--output' in source for source in inputs))

    def test_reviewed_guide_is_invalidated_when_readme_changes(self):
        reviewed = {'owner/project': {'repository_id': 12, 'readme_sha': self.readme['sha'],
                                     'features_ko': ['확인한 기능입니다.'], 'checked_at': '2026-11-02'}}
        valid = guides.make_guide(self.repo, self.readme, reviewed, self.translations)
        self.assertEqual(valid['features_ko'], ['확인한 기능입니다.'])
        changed = guides.make_guide(self.repo, dict(self.readme, sha='c' * 40), reviewed, self.translations)
        self.assertNotIn('features_ko', changed)
        self.assertIn('features', changed)

    def test_missing_sections_have_an_honest_official_link(self):
        guide = guides.make_guide(self.repo, dict(self.readme, text=''), {}, self.translations)
        output = '\n'.join(guides.render_guide(guide, collect.clean))
        self.assertIn('설치 절차가 없습니다', output)
        self.assertIn(self.readme['source_url'], output)
        self.assertNotIn('pip install', output)

    def test_source_code_fence_cannot_close_outer_block(self):
        guide = {'method': '공식 문서', 'readme_url': self.readme['source_url'], 'checked_at': '2026-11-02',
                 'install_code': {'language': 'text', 'code': 'echo "```"\n<script>alert(1)</script>'}}
        output = '\n'.join(guides.render_guide(guide, collect.clean))
        self.assertIn('````text\necho "```"\n<script>alert(1)</script>\n````', output)

    def test_platform_heading_and_command_context_remain_visible(self):
        readme = dict(self.readme, text='## Install\n### Windows\nUse PowerShell on Windows.\n```powershell\ninstall-tool.ps1\n```')
        guide = guides.make_guide(self.repo, readme, {}, self.translations)
        output = '\n'.join(guides.render_guide(guide, collect.clean))
        self.assertIn('공식 문서의 명령·예시 — Install → Windows:', output)
        self.assertEqual(guide['install_code']['context'], 'Use PowerShell on Windows.')

    def test_parent_install_condition_remains_with_a_platform_command(self):
        readme=dict(self.readme,text='## Install\nUse an isolated Python environment before installing this package.\n### Windows\nUse PowerShell on Windows.\n```powershell\ninstall-tool.ps1\n```')
        guide=guides.make_guide(self.repo,readme,{},self.translations)
        output='\n'.join(guides.render_guide(guide,collect.clean))
        self.assertIn('Use an isolated Python environment before installing this package. Use PowerShell on Windows.',output)
        self.assertIn('원문 조건:',output)

    def test_chinese_prose_is_not_sent_to_english_translator(self):
        result = guides.korean_text('这是中文说明文字。', self.translations)
        self.assertEqual(result['method'], '원문 병기')
        self.translations.translate.assert_not_called()

    def test_code_from_linked_document_retains_that_documents_source(self):
        readme = dict(self.readme, text='# Project\nA project with separate documentation.')
        url = 'https://github.com/owner/project/blob/' + 'a' * 40 + '/docs/install.md'
        readme['documents'] = [{'path': 'docs/install.md', 'sha': 'c' * 40, 'source_url': url,
                                'text': '## Install\nRequires Python 3.12.\n```sh\ninstall-tool\n```'}]
        guide = guides.make_guide(self.repo, readme, {}, self.translations)
        self.assertEqual(guide['install_code']['source_url'], url)
        self.assertIn(url, '\n'.join(guides.render_guide(guide, collect.clean)))
