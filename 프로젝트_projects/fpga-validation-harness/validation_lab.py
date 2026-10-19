#!/usr/bin/env python3
"""PC-only synthetic validation lab; Python standard library, no hardware access.

The instrument, ADC readings, faults, and expected values are all simulated.
No driver, JTAG, network, serial port, or external instrument is accessed.

Examples:
    python validation_lab.py --scenario healthy --seed 42 --samples 128
    python validation_lab.py --scenario offset
    python validation_lab.py --scenario timeout --timeout-ms 50
    python validation_lab.py --scenario data-loss
    python validation_lab.py --scenario healthy --decode unsigned

Exit codes: PASS=0, FAIL=1, TIMEOUT=2, ERROR=3.
Each run creates a new directory under --output (default: ./results beside this file).
"""

import argparse
import csv
import json
import math
import platform
import random
import sys
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ADC_BITS = 12
ADC_SCALE = 1.0 / (1 << (ADC_BITS - 1))
SAMPLE_RATE_HZ = 1000.0  # Logical sample time only; no physical clock is used.
AMPLITUDE_V = 0.60
OFFSET_FAULT_V = 0.05
NOISE_BOUND_V = 0.0012
ERROR_TOLERANCE_V = 0.01
EXIT_CODES = {"PASS": 0, "FAIL": 1, "TIMEOUT": 2, "ERROR": 3}


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def save_json(path, data):
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )


def expected_voltage(sequence, total_samples):
    """Known test stimulus: four complete sine cycles in one acquisition."""
    return AMPLITUDE_V * math.sin(2.0 * math.pi * 4 * sequence / total_samples)


def encode_adc(voltage):
    """Quantize to a signed 12-bit code and transport the lower 12 bits."""
    signed_code = round(voltage / ADC_SCALE)
    signed_code = max(-(1 << 11), min((1 << 11) - 1, signed_code))
    return signed_code & ((1 << ADC_BITS) - 1)


def decode_adc(raw_code, mode):
    """unsigned intentionally injects a host-side two's-complement decode bug."""
    code = raw_code & ((1 << ADC_BITS) - 1)
    if mode == "signed" and code & (1 << (ADC_BITS - 1)):
        code -= 1 << ADC_BITS
    return code, code * ADC_SCALE


@dataclass(frozen=True)
class Sample:
    sequence: int
    raw_code: int


class EndOfStream(Exception):
    pass


class AcquisitionTimeout(Exception):
    pass


class MockInstrument:
    """Deterministic data model with a small poll interface for learning."""

    def __init__(self, scenario, seed, samples):
        self.scenario = scenario
        self.samples = samples
        self.rng = random.Random(seed)
        self.next_sequence = 0
        self.connected = False
        self.closed = False
        self.reset_done = False
        self.poll_count = 0
        self.last_raw_code = None

    def open(self):
        self.connected = True

    def poll(self):
        if not self.connected:
            raise RuntimeError("Instrument is not open")
        self.poll_count += 1
        if self.next_sequence >= self.samples:
            raise EndOfStream()
        # Simulate one stalled transaction; the caller owns the deadline.
        if self.scenario == "timeout" and self.next_sequence == self.samples // 2:
            return None

        while self.next_sequence < self.samples:
            sequence = self.next_sequence
            self.next_sequence += 1
            noise = self.rng.uniform(-NOISE_BOUND_V, NOISE_BOUND_V)
            reference = expected_voltage(sequence, self.samples)
            fault = OFFSET_FAULT_V if self.scenario == "offset" else 0.0
            raw = encode_adc(reference + noise + fault)
            # Generate then drop: retained values match a healthy run with this seed.
            if self.scenario == "data-loss" and sequence % 11 == 10:
                continue
            self.last_raw_code = raw
            return Sample(sequence, raw)
        raise EndOfStream()

    def snapshot(self):
        return {
            "synthetic_only": True,
            "scenario": self.scenario,
            "connected": self.connected,
            "next_sequence": self.next_sequence,
            "last_raw_code": self.last_raw_code,
            "poll_count": self.poll_count,
            "reset_done": self.reset_done,
            "closed": self.closed,
        }

    def reset(self):
        # Intentionally destroys volatile state: capture evidence before this call.
        self.next_sequence = 0
        self.last_raw_code = None
        self.reset_done = True

    def close(self):
        self.connected = False
        self.closed = True


def read_with_deadline(instrument, per_sample_timeout_s, run_deadline):
    deadline = min(time.monotonic() + per_sample_timeout_s, run_deadline)
    while True:
        if time.monotonic() >= deadline:
            raise AcquisitionTimeout("No sample arrived before the configured deadline")
        sample = instrument.poll()
        if sample is not None:
            return sample
        remaining = deadline - time.monotonic()
        if remaining > 0:
            time.sleep(min(0.001, remaining))


def evaluate(rows, expected_count):
    sequences = [row["sequence"] for row in rows]
    expected_set = set(range(expected_count))
    observed_set = set(sequences)
    missing = sorted(expected_set - observed_set)
    unexpected = sorted(observed_set - expected_set)
    duplicates = len(sequences) - len(observed_set)
    errors = [row["error_v"] for row in rows]
    mean_error = sum(errors) / len(errors) if errors else None
    max_error = max(abs(value) for value in errors) if errors else None
    checks = [
        {"name": "sample_count", "measured": len(rows), "expected": expected_count,
         "tolerance": 0, "pass": len(rows) == expected_count},
        {"name": "missing_sequences", "measured": len(missing), "expected": 0,
         "tolerance": 0, "pass": not missing},
        {"name": "duplicate_sequences", "measured": duplicates, "expected": 0,
         "tolerance": 0, "pass": duplicates == 0},
        {"name": "unexpected_sequences", "measured": len(unexpected), "expected": 0,
         "tolerance": 0, "pass": not unexpected},
        {"name": "absolute_mean_error_v", "measured": abs(mean_error) if errors else None,
         "expected": 0.0, "tolerance": ERROR_TOLERANCE_V,
         "pass": bool(errors) and abs(mean_error) <= ERROR_TOLERANCE_V},
        {"name": "max_absolute_error_v", "measured": max_error, "expected": 0.0,
         "tolerance": ERROR_TOLERANCE_V,
         "pass": bool(errors) and max_error <= ERROR_TOLERANCE_V},
    ]
    return {
        "observed_samples": len(rows),
        "expected_samples": expected_count,
        "mean_error_v": mean_error,
        "max_absolute_error_v": max_error,
        "missing_sequences": missing,
        "unexpected_sequences": unexpected,
        "checks": checks,
        "all_checks_passed": all(check["pass"] for check in checks),
    }


def bounded_integer(minimum, maximum):
    def parse(value):
        try:
            number = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError("Must be an integer")
        if not minimum <= number <= maximum:
            raise argparse.ArgumentTypeError("Must be between %d and %d" % (minimum, maximum))
        return number
    return parse


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--scenario", choices=["healthy", "offset", "timeout", "data-loss"], default="healthy")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--samples", type=bounded_integer(16, 10000), default=128)
    parser.add_argument("--decode", choices=["signed", "unsigned"], default="signed",
                        help="unsigned deliberately injects a host-side decoding bug")
    parser.add_argument("--timeout-ms", type=bounded_integer(1, 5000), default=50,
                        help="Deadline for each simulated sample transaction")
    parser.add_argument("--run-timeout-ms", type=bounded_integer(1, 30000), default=5000,
                        help="Overall acquisition deadline, not including file output")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "results",
                        help="Parent directory for a fresh run directory; existing runs are kept")
    return parser.parse_args()


def run(args):
    started = time.monotonic()
    run_name = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + args.scenario + "_" + uuid.uuid4().hex[:8]
    run_dir = args.output.expanduser().resolve() / run_name
    run_dir.mkdir(parents=True, exist_ok=False)
    config = {
        "synthetic_only": True,
        "purpose": "New self-study exercise; not evidence of past professional experience",
        "started_utc": utc_now(),
        "scenario": args.scenario,
        "seed": args.seed,
        "samples": args.samples,
        "decode": args.decode,
        "per_sample_timeout_ms": args.timeout_ms,
        "acquisition_timeout_ms": args.run_timeout_ms,
        "adc_bits": ADC_BITS,
        "adc_lsb_v": ADC_SCALE,
        "stimulus_amplitude_v": AMPLITUDE_V,
        "logical_sample_rate_hz": SAMPLE_RATE_HZ,
        "error_tolerance_v": ERROR_TOLERANCE_V,
        "noise_bound_v": NOISE_BOUND_V,
        "offset_fault_v": OFFSET_FAULT_V if args.scenario == "offset" else 0.0,
        "python": sys.version,
        "platform": platform.platform(),
    }
    save_json(run_dir / "config.json", config)
    events = []

    def log(event, **fields):
        events.append({"utc": utc_now(), "elapsed_ms": round((time.monotonic() - started) * 1000, 3),
                       "event": event, **fields})

    rows = []
    status = "ERROR"
    reason = "Acquisition did not finish"
    instrument = MockInstrument(args.scenario, args.seed, args.samples)
    fieldnames = ["sequence", "sample_time_s", "expected_v", "raw_code",
                  "decoded_code", "measured_v", "error_v"]
    print("SYNTHETIC ONLY: PC simulation; no hardware, driver, or JTAG access.")
    print("scenario=%s seed=%d samples=%d decode=%s" % (args.scenario, args.seed, args.samples, args.decode))

    with (run_dir / "samples.csv").open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        try:
            instrument.open()
            log("instrument_opened")
            deadline = time.monotonic() + args.run_timeout_ms / 1000.0
            while True:
                try:
                    sample = read_with_deadline(instrument, args.timeout_ms / 1000.0, deadline)
                except EndOfStream:
                    break
                decoded, measured = decode_adc(sample.raw_code, args.decode)
                expected = expected_voltage(sample.sequence, args.samples)
                row = {
                    "sequence": sample.sequence,
                    "sample_time_s": sample.sequence / SAMPLE_RATE_HZ,
                    "expected_v": expected,
                    "raw_code": sample.raw_code,
                    "decoded_code": decoded,
                    "measured_v": measured,
                    "error_v": measured - expected,
                }
                rows.append(row)
                writer.writerow(row)
            result = evaluate(rows, args.samples)
            status = "PASS" if result["all_checks_passed"] else "FAIL"
            failed_names = [check["name"] for check in result["checks"] if not check["pass"]]
            reason = "All configured checks passed" if status == "PASS" else "Failed checks: " + ", ".join(failed_names)
            log("checks_completed", status=status, reason=reason)
        except AcquisitionTimeout as exc:
            status = "TIMEOUT"
            reason = str(exc)
            log("acquisition_timeout", received=len(rows), reason=reason)
        except Exception as exc:
            status = "ERROR"
            reason = type(exc).__name__ + ": " + str(exc)
            log("unexpected_error", reason=reason)
        finally:
            try:
                # Persist acquired data and device state before reset destroys evidence.
                csv_file.flush()
                result = evaluate(rows, args.samples)
                if status != "PASS":
                    save_json(run_dir / "failure_snapshot.json", {
                        "synthetic_only": True,
                        "captured_utc": utc_now(),
                        "captured_before_reset": not instrument.reset_done,
                        "status": status,
                        "reason": reason,
                        "instrument": instrument.snapshot(),
                        "last_sample": rows[-1] if rows else None,
                        "evaluation": result,
                    })
                    log("failure_snapshot_saved", filename="failure_snapshot.json")
                else:
                    log("acquisition_complete", received=len(rows))
            finally:
                # Cleanup still runs if saving the failure snapshot raises a disk error.
                try:
                    instrument.reset()
                    log("instrument_reset")
                finally:
                    instrument.close()
                    log("instrument_closed")

    summary = {
        "synthetic_only": True,
        "status": status,
        "exit_code": EXIT_CODES[status],
        "reason": reason,
        "scenario": args.scenario,
        "decode": args.decode,
        "evaluation": result,
        "cleanup": {"reset_done": instrument.reset_done, "closed": instrument.closed},
        "finished_utc": utc_now(),
        "run_directory": str(run_dir),
    }
    save_json(run_dir / "events.json", events)
    save_json(run_dir / "summary.json", summary)
    print("RESULT=%s received=%d/%d" % (status, len(rows), args.samples))
    for check in result["checks"]:
        print("  %s: %s measured=%s expected=%s tolerance=%s" % (
            check["name"], "PASS" if check["pass"] else "FAIL",
            check["measured"], check["expected"], check["tolerance"]))
    print("Cleanup: reset=%s closed=%s" % (instrument.reset_done, instrument.closed))
    print("Evidence: " + str(run_dir))
    return EXIT_CODES[status]


def main():
    args = parse_args()
    try:
        return run(args)
    except KeyboardInterrupt:
        print("Interrupted by user. Inspect the latest run directory for saved evidence.", file=sys.stderr)
        return EXIT_CODES["ERROR"]
    except Exception as exc:
        print("ERROR: %s: %s" % (type(exc).__name__, str(exc)), file=sys.stderr)
        return EXIT_CODES["ERROR"]


if __name__ == "__main__":
    sys.exit(main())
