"""Verify the two *executed* ngspice decks; optionally rerun the portable tool.

python verify_run.py             # verify existing logs/wrdata
python verify_run.py --run-spice # execute both decks and verify
"""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import re
import subprocess
import os
import shutil
from datetime import datetime, timezone
import time
import numpy as np
import export_circuit as ec

ROOT = Path(__file__).resolve().parent

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-spice", action="store_true")
    ap.add_argument("--ngspice", type=Path, default=None,
                    help="ngspice executable; alternatively set NGSPICE or use PATH")
    args = ap.parse_args()
    found = str(args.ngspice) if args.ngspice else (os.environ.get("NGSPICE") or shutil.which("ngspice") or shutil.which("ngspice_con"))
    exe = Path(found).resolve() if found else None
    if args.run_spice and (exe is None or not exe.is_file()):
        raise FileNotFoundError("Specify the installed ngspice executable with --ngspice or NGSPICE.")
    records = []
    for index in (8, 15):
        stem = f"{index:05d}"
        deck = ROOT / f"circuit_sample_{stem}.cir"
        log = ROOT / f"ngspice_sample_{stem}.log"
        wave = ROOT / f"ngspice_sample_{stem}_logits.txt"
        launch = None
        if args.run_spice:
            start = time.perf_counter()
            command = [str(exe), "-b", "-o", log.name, deck.name]
            result = subprocess.run(command, cwd=ROOT, capture_output=True, timeout=120)
            if result.returncode:
                raise RuntimeError(result.stderr.decode(errors="replace"))
            launch = {"command": command, "returncode": result.returncode,
                      "process_wall_seconds": time.perf_counter() - start,
                      "stdout": result.stdout.decode(errors="replace")}
        text = log.read_text(encoding="utf-8", errors="replace")
        if "Measurements for Transient Analysis" not in text or "No. of Data Rows" not in text:
            raise AssertionError("No transient run evidence in log")
        if re.search(r"(?im)^\s*(?:Error|Fatal):", text):
            raise AssertionError("Simulator error in log")
        expected = json.loads((ROOT / f"circuit_sample_{stem}_results.json").read_text(encoding="utf-8"))
        parsed_path = ROOT / f"ngspice_sample_{stem}_parsed.json"
        parsed = ec.parse_ngspice_export(wave, expected, parsed_path)
        assert parsed["max_absolute_error_vs_python_finite_gain"] < 1e-7
        assert parsed["prediction"] == expected["python_finite_gain_prediction"]
        assert parsed["prediction"] == (6 if index == 8 else 5)
        match = re.search(r"Total elapsed time \(seconds\)\s*=\s*([\d.]+)", text)
        records.append({"sample_index": index, "true_label": 5,
                        "prediction": parsed["prediction"], "sample_time_s": 8e-6,
                        "max_logit_error_vs_python_finite_gain": parsed["max_absolute_error_vs_python_finite_gain"],
                        "max_logit_error_vs_quantized_ideal": parsed["max_absolute_error_vs_quantized_ideal"],
                        "reported_elapsed_seconds": float(match.group(1)) if match else None,
                        "deck_sha256": digest(deck), "log_sha256": digest(log),
                        "waveform_sha256": digest(wave), "launch": launch})
    report = {"verification_passed": True, "execution_scope": "ngspice transient simulation of two full 64-50-10 fixed-resistor behavioral networks",
              "not_executed": ["Spectre", "transistor opamp", "dynamic memristor programming", "measured silicon", "all 10000 images in SPICE"],
              "checked_at_utc": datetime.now(timezone.utc).isoformat(), "os": platform.platform(),
              "simulator_executed_this_run": args.run_spice,
              "ngspice_executable_sha256": digest(exe) if exe and exe.is_file() else None,
              "reference": "Independent finite-gain TIA KCL equations with identical quantized weights and biases",
              "samples": records}
    (ROOT / "verified_execution.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))

if __name__ == "__main__":
    main()
