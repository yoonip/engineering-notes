import contextlib
import io
import json
from pathlib import Path
import re
import runpy
import unittest


ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'practice.html').read_text(encoding='utf-8')
BANK = json.loads(re.search(
    r'<script type="application/json" id="pp-bank">(.*?)</script>',
    HTML, re.S).group(1))


class PracticeTests(unittest.TestCase):
    def test_console_example(self):
        solution = runpy.run_path(str(ROOT / 'python_essential_practice.py'))['solution']
        values = [3, 1, 2, 1]
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            result = solution(values)
        self.assertEqual(result, 0)
        self.assertEqual(values, [3, 2, 1, 1])
        lines = stream.getvalue().splitlines()
        for expected in ['append: [3, 1, 2, 1, 5]', 'pop: 5 [3, 1, 2, 1]',
                         'min/max: 1 3', 'same count: True', 'str: -1 3',
                         'Counter[1]: 2', 'Counter values: [2, 1, 1]']:
            self.assertIn(expected, lines)

    def test_catalog_structure(self):
        self.assertEqual([q['id'] for q in BANK], list(range(1, 51)))
        self.assertEqual({q['stage'] for q in BANK}, {1, 2, 3, 4, 5})
        self.assertTrue(all(q['code'].count('____') == 1 for q in BANK))

    def test_each_accepted_answer_executes_to_expected_value(self):
        for question in BANK:
            for answer in question['answers']:
                with self.subTest(question=question['id'], answer=answer):
                    code = question['code'].replace('____', answer)
                    namespace = {}
                    exec(compile(code, '<practice>', 'exec'), namespace)
                    self.assertEqual(namespace['result'], question['expected'])

    def test_all_referenced_dom_elements_exist(self):
        element_ids = set(re.findall(r'\bid="([^"]+)"', HTML))
        referenced = set(re.findall(r"\$\('([^']+)'\)", HTML))
        self.assertEqual(referenced - element_ids, set())

    def test_standalone_document(self):
        self.assertIn('<!doctype html>', HTML.lower())
        self.assertIn('<meta charset="utf-8">', HTML)
        self.assertNotIn('window.openai', HTML)
        self.assertNotIn('privateContent', HTML)
        self.assertNotIn('fetch(', HTML)


if __name__ == '__main__':
    unittest.main()
