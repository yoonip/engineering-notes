from pathlib import Path
import subprocess
import tempfile
import unittest

import publish_changes as writer


class WriterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.git('init', '-b', 'main')
        self.git('config', 'user.name', 'Test author')
        self.git('config', 'user.email', 'test@example.invalid')
        (self.repo / 'analysis.md').write_text('Existing explanation\n', encoding='utf-8')
        self.git('add', 'analysis.md')
        self.git('commit', '-m', 'Initial')

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.repo), *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout

    def test_only_inbox_is_committed_and_original_analysis_is_unchanged(self):
        path = self.repo / '기술동향_technology/새자료_inbox/README.md'
        path.parent.mkdir(parents=True)
        path.write_text('New source\n', encoding='utf-8')
        commits = writer.commit_changes(self.repo, '2026-10-29 13:00')
        self.assertEqual([commit['group'] for commit in commits], ['technology'])
        self.assertEqual((self.repo / 'analysis.md').read_text(), 'Existing explanation\n')
        self.assertEqual(writer.commit_changes(self.repo, '2026-10-29 14:00'), [])

    def test_changed_explanation_aborts_before_any_commit(self):
        (self.repo / 'analysis.md').write_text('Changed\n', encoding='utf-8')
        head = self.git('rev-parse', 'HEAD')
        with self.assertRaises(ValueError):
            writer.commit_changes(self.repo, '2026-10-29 13:00')
        self.assertEqual(head, self.git('rev-parse', 'HEAD'))

    def test_existing_staged_changes_are_not_taken_over(self):
        (self.repo / 'analysis.md').write_text('Changed\n', encoding='utf-8')
        self.git('add', 'analysis.md')
        with self.assertRaises(ValueError):
            writer.commit_changes(self.repo, '2026-10-29 13:00')
        self.assertIn(b'analysis.md', self.git('diff', '--cached', '--name-only'))


if __name__ == '__main__':
    unittest.main()
