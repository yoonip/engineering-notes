"""Regression cases for links next to code and punctuation in Markdown."""
import unittest

from check_documents import destinations, heading_ids, without_fences


class MarkdownDestinations(unittest.TestCase):
    def test_array_formula_is_code_while_adjacent_link_is_real(self):
        text = '`new[j]=old[j](1-p)+old[j-1]p` [DP](dp.md#transition)'
        self.assertEqual(list(destinations(text)), ['dp.md#transition'])

    def test_code_can_contain_shorter_backticks_and_newlines(self):
        text = '``a ` [fake](missing.md)\ntext``\n[real](notes.md)'
        self.assertEqual(list(destinations(text)), ['notes.md'])

    def test_code_in_link_label_does_not_hide_the_destination(self):
        text = '[`array[j]`](arrays.md) ![plot](<figures/plot (2).svg>)'
        self.assertEqual(list(destinations(text)), ['arrays.md', 'figures/plot (2).svg'])

    def test_escaped_and_unclosed_backticks_are_literal(self):
        self.assertEqual(list(destinations(r'\` [real](notes.md) \`')), ['notes.md'])
        self.assertEqual(list(destinations('`unclosed [real](notes.md)')), ['notes.md'])

    def test_unclosed_code_does_not_hide_links_in_later_paragraphs(self):
        text = '`unclosed\n\n[real](notes.md)\n\n`later code`'
        self.assertEqual(list(destinations(text)), ['notes.md'])

    def test_balanced_parentheses_and_heading_links_still_work(self):
        text = '[body](notes/example(1).md#part) [section](#arrayj)'
        self.assertEqual(list(destinations(text)), ['notes/example(1).md#part', '#arrayj'])
        self.assertIn('arrayj', heading_ids('# `array[j]`'))

    def test_fenced_examples_are_not_link_sources(self):
        text = '```python\nvalue[j](missing.md)\n```\n[real](notes.md)'
        self.assertEqual(list(destinations(without_fences(text))), ['notes.md'])


if __name__ == '__main__':
    unittest.main()
