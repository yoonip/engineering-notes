"""Small integrity checks for the portable source manifest."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / 'tools' / 'manifest.py'
SPEC = importlib.util.spec_from_file_location('export_manifest', MODULE)
manifest = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(manifest)


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root / 'sample.py').write_text('value = 1\n', encoding='utf-8')
        manifest.create(self.root)

    def test_clean_inventory(self):
        self.assertTrue(manifest.verify(self.root)['passed'])

    def test_content_change_is_detected(self):
        (self.root / 'sample.py').write_text('value = 2\n', encoding='utf-8')
        self.assertFalse(manifest.verify(self.root)['passed'])

    def test_unrecorded_source_is_detected(self):
        (self.root / 'extra.py').write_text('x = 0\n', encoding='utf-8')
        self.assertFalse(manifest.verify(self.root)['passed'])

    def test_parent_path_is_rejected(self):
        path = self.root / 'MANIFEST_SHA256.json'
        value = json.loads(path.read_text(encoding='utf-8'))
        value['files'][0]['path'] = '../sample.py'
        path.write_text(json.dumps(value), encoding='utf-8')
        self.assertFalse(manifest.verify(self.root)['passed'])

    def test_duplicate_path_is_rejected(self):
        path = self.root / 'MANIFEST_SHA256.json'
        value = json.loads(path.read_text(encoding='utf-8'))
        value['files'].append(value['files'][0].copy())
        path.write_text(json.dumps(value), encoding='utf-8')
        self.assertFalse(manifest.verify(self.root)['passed'])


if __name__ == '__main__':
    unittest.main()
