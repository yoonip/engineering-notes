from pathlib import Path
import copy
import importlib.util
import json
import unittest

HERE = Path(__file__).resolve().parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.solution


class SolutionTests(unittest.TestCase):
    def test_examples_and_comparisons(self):
        main, alternative = load("solution"), load("alternative")
        cases = json.loads((HERE / "test_cases.json").read_text(encoding="utf-8"))
        for case in cases:
            with self.subTest(source=case["source"], args=case["args"]):
                actual = main(*copy.deepcopy(case["args"]))
                self.assertEqual(actual, case["expected"])
                if case.get("alternative", True):
                    self.assertEqual(alternative(*copy.deepcopy(case["args"])), actual)


    def test_large_boundary(self):
        main=load("solution")
        self.assertEqual(main(1,1000000,999999),1)

if __name__ == "__main__":
    unittest.main()
