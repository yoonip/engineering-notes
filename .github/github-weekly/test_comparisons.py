"""장단점·대안·선택의 출처와 제작자 주장 범위가 보존되는지 검사합니다."""
import unittest
from unittest.mock import Mock, patch
from urllib.error import HTTPError

import collect
import comparisons
import guides


README = '''# Example

## Features

Generate videos from HTML and CSS without a React application.

## Advantages

This project can reuse the HTML and CSS assets from a website.

## Limitations

The renderer requires a local browser and a supported video encoder.

## Comparison

The rendering model differs from [Other](https://github.com/other/video).

| Tool | Input | Server |
| --- | --- | --- |
| Example | HTML | Local |
| Other | React | Optional |

### Reproduce benchmark

Install [PyTorch](https://github.com/pytorch/pytorch) for the benchmark only.

## When to use

Choose this tool when your video scenes already exist as HTML pages.
'''


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.repo = {'id': 4, 'full_name': 'owner/example', 'html_url': 'https://github.com/owner/example',
                     'default_branch': 'main', 'stargazers_count': 999999999}
        self.readme = {'status': 'ok', 'text': README, 'sha': 'b' * 40, 'commit': 'a' * 40,
                       'source_url': self.repo['html_url'] + '/blob/' + 'a' * 40 + '/README.md',
                       'fetched_at': '2026-11-02T01:00:00Z'}
        self.translations = Mock()
        self.translations.translate.side_effect = lambda source: {'text': '공식 설명을 한국어로 옮깁니다.', 'method': 'test translator'}
        self.other = {'id': 5, 'full_name': 'other/video', 'html_url': 'https://github.com/other/video',
                      'default_branch': 'main', 'language': 'TypeScript', 'license': {'spdx_id': 'MIT'}}
        self.other_readme = dict(self.readme, source_url=self.other['html_url'] + '/blob/' + 'c' * 40 + '/README.md',
                                 commit='c' * 40, sha='d' * 40, text='## Features\nRender videos with React components.\n\n## Requirements\nRequires Node.js 22 or later.')

    def build(self, readme=None):
        loader, getter = Mock(return_value=self.other), Mock()
        with patch.object(guides, 'fetch_readme', return_value=self.other_readme):
            result = comparisons.build(self.repo, readme or self.readme, {}, self.translations, getter, loader, '')
        return result, loader

    def test_benchmark_dependency_is_not_selected_as_a_competitor(self):
        names = comparisons.competitor_names(comparisons.parsed_documents(self.readme), self.repo['full_name'])
        self.assertEqual(names, ['other/video'])

    def test_unrelated_feature_links_and_inspiration_are_not_alternatives(self):
        readme = dict(self.readme, text='## Features\nUses [Torch](https://github.com/pytorch/pytorch).\n## Inspired by\n[Other](https://github.com/other/video)')
        self.assertEqual(comparisons.competitor_names(comparisons.parsed_documents(readme), 'owner/example'), [])

    def test_disadvantages_are_not_advantages(self):
        parsed = comparisons.parsed_documents(dict(self.readme, text='## Disadvantages\nRequires a dedicated GPU with enough memory.'))
        self.assertEqual(comparisons.select(parsed, 'advantages'), [])
        self.assertEqual(len(comparisons.select(parsed, 'limitations')), 1)

    def test_opposite_subsection_does_not_inherit_advantage_scope(self):
        parsed = comparisons.parsed_documents(dict(self.readme, text='## Advantages\nReuse your existing design assets without rewriting them.\n### Limitations\nThis tool cannot process files larger than ten megabytes.\n### Reuse\nKeep your existing assets in the same project.'))
        advantages = comparisons.evidence(parsed, 'advantages', self.translations)
        self.assertEqual([item['original'] for item in advantages], [
            'Reuse your existing design assets without rewriting them.',
            'Keep your existing assets in the same project.'])
        limits = comparisons.evidence(parsed, 'limitations', self.translations)
        self.assertEqual([item['original'] for item in limits], ['This tool cannot process files larger than ten megabytes.'])

    def test_mixed_tradeoff_heading_does_not_assign_both_categories(self):
        parsed = comparisons.parsed_documents(dict(self.readme, text='## Advantages and disadvantages\nThe renderer reuses assets but requires a browser.'))
        self.assertEqual(comparisons.select(parsed, 'advantages'), [])
        self.assertEqual(comparisons.select(parsed, 'limitations'), [])

    def test_heading_scope_does_not_cross_document_boundaries(self):
        readme = dict(self.readme, text='## Advantages\nReuse your existing design assets without rewriting them.', documents=[
            {'text':'### Install\nThis tool requires a browser.', 'source_url':'https://github.com/owner/example/blob/commit/install.md'}])
        parsed = comparisons.parsed_documents(readme)
        self.assertEqual([item['heading'] for item in comparisons.select(parsed, 'advantages')], ['Advantages'])

    def test_integrations_below_alternatives_are_not_competitors(self):
        parsed = comparisons.parsed_documents(dict(self.readme, text='## Alternatives\n[Other](https://github.com/other/video)\n### Optional integrations\n[Python](https://github.com/python/cpython)'))
        self.assertEqual(comparisons.competitor_names(parsed, 'owner/example'), ['other/video'])

    def test_each_extracted_claim_keeps_its_source(self):
        result, loader = self.build()
        self.assertEqual(loader.call_args.args[0], 'other/video')
        for key in ('advantages','limitations','comparison','selection'):
            self.assertTrue(result[key])
            self.assertEqual(result[key][0]['source_url'], self.readme['source_url'])
        self.assertNotIn('score', result)

    def test_rival_information_comes_from_its_own_fixed_readme(self):
        result, _ = self.build()
        other = result['official_competitors'][0]
        self.assertEqual(other['readme_url'], self.other_readme['source_url'])
        self.assertEqual(other['commit'], 'c' * 40)
        self.assertEqual(other['features'][0]['original'], 'Render videos with React components.')

    def test_author_comparison_is_labeled_and_all_requested_sections_render(self):
        result, _ = self.build()
        text = '\n'.join(comparisons.render(result, collect.clean))
        for heading in ('장점', '제약과 확인할 점', '비슷한 도구와의 차이', '선택하기 좋은 상황'):
            self.assertIn('### ' + heading, text)
        self.assertIn('제작자가 공개한 설명', text)
        self.assertIn(self.readme['source_url'], text)
        self.assertIn(self.other_readme['source_url'], text)
        self.assertNotIn('999999999', text)

    def test_no_evidence_does_not_create_a_rival_or_ranking(self):
        result, loader = self.build(dict(self.readme, text='# Example\n'))
        loader.assert_not_called()
        self.assertEqual(result['official_competitors'], [])
        text = '\n'.join(comparisons.render(result, collect.clean))
        self.assertIn('구체적인 비교 근거가 없어', text)
        self.assertNotIn('더 빠릅니다', text)

    def test_reviewed_assessment_requires_same_repo_and_readme(self):
        manual = {'owner/example': {'repository_id':4, 'readme_sha':'b' * 40, 'checked_at':'2026-11-02',
                    'advantages_ko':[{'text':'기존 해설입니다.','source_urls':[self.readme['source_url']]}]}}
        getter, loader = Mock(), Mock()
        result = comparisons.build(self.repo,self.readme,manual,self.translations,getter,loader,'')
        self.assertEqual(result['origin'],'reviewed')
        loader.assert_not_called()
        changed = dict(self.readme, sha='f' * 40, text='# A changed project\n')
        result = comparisons.build(self.repo,changed,manual,self.translations,getter,loader,'')
        self.assertEqual(result['origin'],'extracted')
        self.assertNotIn('advantages_ko', result)

    def test_markdown_tables_stay_inside_their_own_boundaries(self):
        parsed = guides.sections('## Comparison\n| Tool | Value |\n| --- | --- |\n| One | 1 |\n\nSome prose.\n\n| Other | Value |\n| --- | --- |\n| Two | 2 |')
        tables = parsed[-1]['tables']
        self.assertEqual(len(tables),2)
        self.assertEqual(tables[0]['rows'],[['One','1']])
        self.assertEqual(tables[1]['rows'],[['Two','2']])

    def test_external_hosts_and_code_block_links_are_not_followed(self):
        text = '## Alternatives\n[Foreign](https://evil.example/other/video)\n```md\n[Do not fetch](https://github.com/fake/repo)\n```'
        self.assertEqual(comparisons.competitor_names(comparisons.parsed_documents(dict(self.readme,text=text)),'owner/example'),[])

    def test_missing_rival_is_not_fabricated(self):
        loader = Mock(side_effect=HTTPError('https://api.github.com',404,'Missing',{},None))
        result = comparisons.build(self.repo,self.readme,{},self.translations,Mock(),loader,'')
        self.assertEqual(result['official_competitors'],[])

    def test_generic_only_marketing_sentence_is_not_a_documented_limit(self):
        parsed = comparisons.parsed_documents(dict(self.readme,text='## Features\nOnly the best design is provided by this project.\n## Requirements\nNo API key required.'))
        self.assertEqual(comparisons.documented_conditions(parsed,self.translations),[])

    def test_selection_keeps_a_negative_heading_context(self):
        result,_ = self.build(dict(self.readme,text='## When not to use\nProduction traffic without an available model server.'))
        output='\n'.join(comparisons.render(result,collect.clean))
        self.assertIn('원문 (When not to use)',output)
