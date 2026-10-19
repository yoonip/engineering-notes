#!/usr/bin/env python3
"""표준 라이브러리만 사용하는 소프트웨어 모델/모의 전송 테스트.

Run: python -B tests/test_offline.py --report /existing/folder/report.json
No board, debugger, kernel module, VISA backend, or network is used.
"""
import sys

sys.dont_write_bytecode = True

import argparse
import ast
import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import platform
import subprocess
import tempfile
import types
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


def load_source(relative):
    """Import only the named local module; do not discover installed backends."""
    spec = importlib.util.spec_from_file_location(
        "offline_" + Path(relative).stem, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_python(relative, *args):
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    return subprocess.run(
        [sys.executable, "-B", str(ROOT / relative), *map(str, args)],
        cwd=ROOT, env=environment, capture_output=True, text=True,
        encoding="utf-8", timeout=30, check=False)


class SourceTests(unittest.TestCase):
    def test_all_python_sources_parse(self):
        files = sorted(ROOT.rglob("*.py"))
        self.assertTrue(files)
        for path in files:
            ast.parse(path.read_text(encoding="utf-8"),
                      filename=path.relative_to(ROOT).as_posix())


class TapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tap = load_source("jtag/tap_walk.py")

    def walk(self, bits, state):
        with contextlib.redirect_stdout(io.StringIO()):
            return self.tap.walk(bits, state)

    def test_all_16_states_reset_with_five_ones(self):
        self.assertEqual(len(self.tap.NEXT), 16)
        for state, successors in self.tap.NEXT.items():
            self.assertEqual(len(successors), 2)
            self.assertTrue(set(successors).issubset(self.tap.NEXT))
            self.assertEqual(self.walk("11111", state), "Test-Logic-Reset",
                             state)

    def test_ir_dr_shift_pause_update_paths(self):
        for path, target in [("0100", "Shift-DR"), ("01100", "Shift-IR")]:
            self.assertEqual(self.walk(path, "Test-Logic-Reset"), target)
        for register in ("DR", "IR"):
            shift = "Shift-" + register
            self.assertEqual(self.walk("10", shift), "Pause-" + register)
            self.assertEqual(self.walk("1010", shift), shift)
            self.assertEqual(self.walk("11", shift), "Update-" + register)
            self.assertEqual(self.walk("110", shift), "Run-Test/Idle")

    def test_invalid_tms_is_rejected(self):
        with self.assertRaises(ValueError):
            self.walk("0102", "Test-Logic-Reset")


class ModelCliTests(unittest.TestCase):
    def test_existing_bench_checks(self):
        run = run_python("validation/check_examples.py")
        self.assertEqual(run.returncode, 0, "bench checks failed")
        self.assertIn("PASS: 5 harness outcomes", run.stdout)

    def test_npu_cli_reference_faults_and_input_hash(self):
        # Independent hand-computed scalar results for the documented input.
        expected = [[185, -39], [83, 123]]
        hashes = []
        with tempfile.TemporaryDirectory(prefix="offline-npu-") as temp:
            for fault in ("none", "layout", "stale", "overflow"):
                out = Path(temp) / fault
                run = run_python("validation/npu.py", "--fault", fault,
                                 "--out", out)
                self.assertEqual(run.returncode, 0 if fault == "none" else 1,
                                 fault)
                result = json.loads((out / "result.json").read_text())
                self.assertEqual(result, json.loads(run.stdout))
                self.assertIs(result["simulation_only"], True)
                self.assertEqual(result["expected"], expected)
                self.assertEqual(result["status"],
                                 "PASS" if fault == "none" else "FAIL")
                actual_hash = hashlib.sha256((out / "input.json").read_bytes()).hexdigest()
                self.assertEqual(result["input_sha256"], actual_hash)
                hashes.append(actual_hash)
                self.assertEqual(bool(result["errors"]), fault != "none")
                if fault == "none":
                    self.assertEqual(result["actual"], expected)
                if fault == "overflow":
                    self.assertEqual(result["actual"][0][0], -71)
        self.assertEqual(len(set(hashes)), 1)

    def test_coverage_example_distinguishes_attempts_from_valid_results(self):
        run = run_python("validation/coverage_account.py")
        self.assertEqual(run.returncode, 0)
        self.assertIn("planned=12, executed=10, valid=8", run.stdout)
        self.assertIn("conditional pass=7/8", run.stdout)


class TrainingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.training = load_source("validation/training_ber.py")

    def test_window_empty_singleton_duplicates_tie_and_split(self):
        self.assertEqual(self.training.longest_window([]),
                         {"pass": False, "reason": "NO_PASS_TAP"})
        one = self.training.longest_window([7, 7])
        self.assertEqual((one["chosen_tap"], one["margin_steps"],
                          one["passing_tap_count"]), (7, 0, 1))
        tied = self.training.longest_window([11, 2, 1, 10, 2])
        self.assertEqual(tied["all_windows"], [(1, 2), (10, 11)])
        self.assertEqual(tied["chosen_tap"], 1)
        split = self.training.longest_window([1, 2, 3, 9, 10])
        self.assertEqual((split["left_tap"], split["right_tap"],
                          split["chosen_tap"], split["margin_steps"]),
                         (1, 3, 2, 1))

    def test_ber_exact_bound_and_invalid_arguments(self):
        upper = self.training.zero_error_upper
        self.assertAlmostEqual(upper(1, 0.95), 0.95)
        self.assertAlmostEqual(upper(10, 0.95), 1 - 0.05 ** 0.1)
        self.assertTrue(9.98e-13 < upper(3e12) < 1e-12)
        self.assertLess(upper(100), upper(10))
        for bits, confidence in [(0, .95), (-1, .95), (10, 0), (10, 1)]:
            with self.assertRaises(ValueError):
                upper(bits, confidence)


class CorrelationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.correlation = load_source("validation/correlation.py")

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="offline-correlation-")
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.correlation.make_dataset(self.folder)

    def rewrite(self, name, rows):
        self.correlation.write_csv(self.folder / name, rows)

    def rows(self, name):
        return list(self.correlation.load_unique(self.folder / name).values())

    def test_synthetic_matrix_and_distinct_false_accept_denominators(self):
        report = self.correlation.analyse(self.folder, True)
        self.assertEqual(report["matrix_ate_slt"],
                         {"PASS/PASS": 900, "PASS/FAIL": 60,
                          "FAIL/PASS": 20, "FAIL/FAIL": 20})
        self.assertAlmostEqual(report["agreement"], .92)
        metrics = report["independent_truth_metrics"]
        self.assertEqual((metrics["good_parts"], metrics["bad_parts"],
                          metrics["passed_parts"], metrics["false_accept_parts"],
                          metrics["false_reject_parts"]), (940, 60, 920, 10, 30))
        self.assertAlmostEqual(metrics["false_accept_per_bad"], 10 / 60)
        self.assertAlmostEqual(metrics["shipped_defective_fraction"], 10 / 920)
        self.assertAlmostEqual(metrics["false_reject_per_good"], 30 / 940)
        no_truth = self.correlation.analyse(self.folder, False)
        self.assertNotIn("independent_truth_metrics", no_truth)

    def test_invalid_truth_classification_is_rejected(self):
        rows = self.rows("truth.csv")
        rows[0]["classification"] = "UNKNOWN"
        self.rewrite("truth.csv", rows)
        with self.assertRaisesRegex(ValueError, "Invalid truth"):
            self.correlation.analyse(self.folder, True)

    def test_unmatched_and_duplicate_serials_are_rejected(self):
        slt = self.rows("slt.csv")
        self.rewrite("slt.csv", slt[:-1])
        with self.assertRaisesRegex(ValueError, "Unmatched"):
            self.correlation.analyse(self.folder, False)
        self.rewrite("slt.csv", slt + [dict(slt[0])])
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.correlation.analyse(self.folder, False)

    def test_zero_denominators_are_unavailable_not_zero(self):
        common = {"serial": "SIM-ONE", "lot": "L0", "temperature_c": "25",
                  "voltage_v": "0.80"}
        for classification, outcome, unavailable in [
                ("GOOD", "FAIL", {"false_accept_per_bad",
                                  "shipped_defective_fraction", "shipped_dppm"}),
                ("BAD", "PASS", {"false_reject_per_good"})]:
            self.rewrite("ate.csv", [dict(common, result=outcome)])
            self.rewrite("slt.csv", [dict(common, result=outcome)])
            self.rewrite("truth.csv", [{"serial": "SIM-ONE",
                                        "classification": classification}])
            metrics = self.correlation.analyse(self.folder, True)["independent_truth_metrics"]
            self.assertEqual(set(metrics["undefined_metrics"]), unavailable)
            for name in unavailable:
                self.assertIsNone(metrics[name])


class VisaMockTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.visa = load_source("validation/visa_readonly.py")

    def make_backend(self):
        manager, device = mock.MagicMock(), mock.MagicMock()
        manager.open_resource.return_value = device
        backend = types.SimpleNamespace(ResourceManager=mock.Mock(return_value=manager))
        return backend, manager, device

    def test_mock_query_configuration_and_normal_close(self):
        backend, manager, device = self.make_backend()
        device.query.return_value = "MOCK,MODEL,0,1\n"
        with mock.patch.dict(sys.modules, {"pyvisa": backend}):
            transport = self.visa.VisaTransport("MOCK::INSTR", backend="@mock")
            try:
                self.assertEqual(transport.query("*IDN?"), "MOCK,MODEL,0,1")
                self.assertEqual(device.timeout, 2000)
                self.assertEqual(device.read_termination, "\n")
                self.assertEqual(device.write_termination, "\n")
                device.query.assert_called_once_with("*IDN?")
                self.assertEqual(transport.log[0]["command"], "*IDN?")
                self.assertGreaterEqual(transport.log[0]["host_elapsed_s"], 0)
            finally:
                transport.close()
        backend.ResourceManager.assert_called_once_with("@mock")
        manager.open_resource.assert_called_once_with("MOCK::INSTR")
        device.close.assert_called_once()
        manager.close.assert_called_once()

    def test_open_failure_closes_manager(self):
        backend, manager, device = self.make_backend()
        manager.open_resource.side_effect = OSError("mock open failure")
        with mock.patch.dict(sys.modules, {"pyvisa": backend}):
            with self.assertRaises(OSError):
                self.visa.VisaTransport("MOCK::INSTR")
        manager.close.assert_called_once()
        device.close.assert_not_called()

    def test_query_failure_is_cleaned_up_by_caller_finally(self):
        backend, manager, device = self.make_backend()
        device.query.side_effect = TimeoutError("mock query timeout")
        with mock.patch.dict(sys.modules, {"pyvisa": backend}):
            transport = self.visa.VisaTransport("MOCK::INSTR")
            with self.assertRaises(TimeoutError):
                try:
                    transport.query("*IDN?")
                finally:
                    transport.close()
        self.assertEqual(transport.log, [])
        device.close.assert_called_once()
        manager.close.assert_called_once()


class LinuxClientMockTests(unittest.TestCase):
    def run_client(self, written, response, expected_error=None):
        # Compile before patching. Every client device operation is mocked.
        source = (ROOT / "linux/client.py").read_text(encoding="utf-8")
        code = compile(source, "linux/client.py", "exec")
        reader = io.BytesIO(response)
        output = io.StringIO()
        with mock.patch("os.open", return_value=17) as opened, \
                mock.patch("os.write", return_value=written) as write, \
                mock.patch("os.close") as close, \
                mock.patch("builtins.open", return_value=reader) as read_open, \
                contextlib.redirect_stdout(output):
            if expected_error:
                with self.assertRaises(expected_error):
                    exec(code, {"__name__": "__main__"})
            else:
                exec(code, {"__name__": "__main__"})
        opened.assert_called_once_with("/dev/valdemo", os.O_WRONLY)
        write.assert_called_once_with(17, bytes([1, 2, 3, 250]))
        close.assert_called_once_with(17)
        if written != 4:
            read_open.assert_not_called()
        else:
            read_open.assert_called_once_with("/dev/valdemo", "rb", buffering=0)
        return output.getvalue()

    def test_normal_device_response(self):
        self.assertIn("PASS length=4 sum=256",
                      self.run_client(4, b"length=4 sum=256\n"))

    def test_short_write_closes_descriptor_before_raising(self):
        self.run_client(2, b"", RuntimeError)

    def test_bad_checksum_is_rejected(self):
        self.run_client(4, b"length=4 sum=255\n", AssertionError)


class JsonResult(unittest.TextTestResult):
    """Public report contains stable test IDs and statuses, not local paths."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.records.append({"name": test.id().split(".", 1)[-1], "status": "PASS"})

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.records.append({"name": test.id().split(".", 1)[-1], "status": "FAIL",
                             "exception_type": err[0].__name__})

    def addError(self, test, err):
        super().addError(test, err)
        self.records.append({"name": test.id().split(".", 1)[-1], "status": "ERROR",
                             "exception_type": err[0].__name__})

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.records.append({"name": test.id().split(".", 1)[-1], "status": "SKIP"})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if args.report is not None and not args.report.parent.is_dir():
        parser.error("report parent directory must already exist")
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2, resultclass=JsonResult).run(suite)
    report = {
        "schema_version": 1,
        "scope": "offline software models and mocked transports only",
        "status": "PASS" if result.wasSuccessful() else "FAIL",
        "runtime": {"python_version": platform.python_version(),
                    "implementation": platform.python_implementation(),
                    "os_family": platform.system()},
        "counts": {"total": result.testsRun,
                   "passed": sum(r["status"] == "PASS" for r in result.records),
                   "failed": len(result.failures), "errors": len(result.errors),
                   "skipped": len(result.skipped)},
        "tests": result.records,
        "limits": {
            "physical_hardware": "NOT_RUN",
            "firmware_and_kernel_module_compilation": "NOT_RUN",
            "qemu_or_other_external_simulator": "NOT_RUN",
            "actual_visa_transport_and_linux_device_io": "NOT_RUN; mocked only",
            "openocd_gdb_daemon_and_external_services": "NOT_RUN",
            "power_timing_signal_integrity_and_silicon_coverage": "NOT_MEASURED"}}
    if args.report is not None:
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                               encoding="utf-8")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
