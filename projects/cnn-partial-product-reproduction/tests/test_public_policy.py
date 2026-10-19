"""Offline source-tree guards. They do not certify legal rights or anonymity.

Generated experiment output is intentionally outside this source inventory.
Use a clean checkout and review staged files before publishing anything.
"""
from pathlib import Path
import ast
import json
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIRECTORIES = {".git", ".venv", "__pycache__", "results", "data", "user_runs"}
FORBIDDEN_DIRECTORIES = {"vendor", "node_modules", "site-packages", "checkpoints", "sources"}
FORBIDDEN_SUFFIXES = {
    ".pdf", ".ppt", ".pptx", ".doc", ".docx", ".xls", ".xlsx",
    ".pt", ".pth", ".npz", ".npy", ".pkl", ".pickle", ".dat", ".raw",
    ".exe", ".dll", ".so", ".dylib", ".bin", ".zip", ".tar", ".tgz", ".gz",
}
PRIVATE_PATH_PATTERNS = {
    "absolute drive path": re.compile(r"(?i)\b[a-z]:[\\/]"),
    "personal home directory": re.compile(r"/(?:home|Users)/[^\s/]+/"),
    "personal UNC share": re.compile(r"\\\\[\w.-]+\\[\w$.-]+"),
    "email address": re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"),
}


def source_files():
    return [p for p in ROOT.rglob("*") if p.is_file()
            and not RUNTIME_DIRECTORIES.intersection(p.relative_to(ROOT).parts)]


class PublicSourcePolicyTests(unittest.TestCase):
    def test_no_document_checkpoint_dataset_or_vendor_payload(self):
        problems = []
        for path in source_files():
            relative = path.relative_to(ROOT)
            if path.suffix.lower() in FORBIDDEN_SUFFIXES:
                problems.append(str(relative))
            if FORBIDDEN_DIRECTORIES.intersection(relative.parts):
                problems.append(str(relative))
            # Names of original device-model files are referenceable in source
            # code, but their actual third-party payload is not part of this tree.
            if path.name.startswith("sky130_fd_pr__"):
                problems.append(str(relative))
        self.assertEqual(problems, [], "Excluded payload in public source inventory")

    def test_source_text_has_no_machine_or_contact_identifiers(self):
        problems = []
        for path in source_files():
            if path.suffix.lower() in FORBIDDEN_SUFFIXES:
                continue
            try:
                text = path.read_text(encoding="utf-8-sig")
            except UnicodeDecodeError:
                problems.append((str(path.relative_to(ROOT)), "non-text payload"))
                continue
            for label, pattern in PRIVATE_PATH_PATTERNS.items():
                if pattern.search(text):
                    problems.append((str(path.relative_to(ROOT)), label))
        self.assertEqual(problems, [], "Review locally; do not paste sensitive matches into public logs")

    def test_python_sources_parse_without_importing_training_modules(self):
        for path in source_files():
            if path.suffix == ".py":
                with self.subTest(path=str(path.relative_to(ROOT))):
                    ast.parse(path.read_text(encoding="utf-8-sig"), filename=path.name)

    def test_optional_json_metadata_is_well_formed(self):
        for path in source_files():
            if path.suffix == ".json":
                with self.subTest(path=str(path.relative_to(ROOT))):
                    value = json.loads(path.read_text(encoding="utf-8-sig"))
                    self.assertIsInstance(value, (dict, list))

    def test_licensing_status_and_independent_provenance_are_explicit(self):
        license_path = ROOT / "LICENSE"
        self.assertTrue(license_path.is_file(), "Record the project's licensing status explicitly")
        self.assertGreater(len(license_path.read_text(encoding="utf-8-sig").strip()), 200)
        readme = ROOT / "README.md"
        self.assertTrue(readme.is_file())
        text = readme.read_text(encoding="utf-8-sig")
        self.assertRegex(text, r"(?i)\bAI(?:[- ](?:assisted|generated))?\b")
        self.assertRegex(text, r"(?i)independent|독립")


if __name__ == "__main__":
    unittest.main()
