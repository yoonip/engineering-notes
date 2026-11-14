"""Check real temporary Git commits and their reported article counts; no push."""
import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import pipeline as p
import publish


class PublicationReportingTests(unittest.TestCase):
    def test_state_commit_and_article_commit_have_distinct_counts(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)/'repo'; root.mkdir()
            output=Path(temporary)/'output'; output.mkdir()
            summary=Path(temporary)/'summary.md'
            def git(*args):
                return subprocess.run(['git','-C',str(root),*args],check=True,
                                      capture_output=True).stdout
            state_path=p.CONTROL+'/state.json'
            state=root/state_path; state.parent.mkdir(parents=True)
            state.write_text('{}\n',encoding='utf-8')
            git('init'); git('add','.')
            git('-c','user.name=Test','-c','user.email=test@example.invalid','commit','-m','Initial state')
            for article in (False,True):
                paths=[state_path]
                if article:
                    paths.append(p.CATEGORY+'/자동분석_auto-research/2026-11-15/검사_Test.md')
                hashes={name:p.digest((root/name).read_bytes()) if (root/name).exists() else None for name in paths}
                for name in paths:
                    target=output/name; target.parent.mkdir(parents=True,exist_ok=True)
                    target.write_text('{"checked":true}\n' if name==state_path else '# Test article\n',encoding='utf-8')
                (output/'manifest.json').write_text(json.dumps({'paths':paths,'base_sha256':hashes}),encoding='utf-8')
                log=io.StringIO()
                with patch.dict(os.environ,{'GITHUB_STEP_SUMMARY':str(summary)}),contextlib.redirect_stdout(log):
                    self.assertEqual(publish.main(['--root',str(root),'--output',str(output)]),0)
                result=json.loads(log.getvalue())
                self.assertEqual(result['analyses_published'],int(article))
                self.assertEqual(result['state_only'],not article)
                self.assertFalse(result['pushed'])
                self.assertEqual(git('status','--porcelain'),b'')
            self.assertIn('새 분석 글: 0개',summary.read_text(encoding='utf-8'))
            self.assertIn('새 분석 글: 1개',summary.read_text(encoding='utf-8'))


if __name__=='__main__':unittest.main()
