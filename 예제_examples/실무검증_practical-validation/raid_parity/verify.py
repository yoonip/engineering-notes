"""Fresh-process, fixed-oracle checks for one educational host-file stripe."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import struct
import subprocess
import sys

HERE = Path(__file__).resolve().parent
MUTATIONS = ("none", "trust-dirty", "replay-incomplete", "accept-two-missing", "skip-generation")


class Checks:
    def __init__(self, output, mutation):
        self.output = output
        self.mutation = mutation
        self.calls = []
        self.checks = []
        self.case_count = 0
        self.fixture = json.loads((HERE / "fixtures.json").read_text("utf-8"))

    def check(self, name, actual, expected):
        self.checks.append({"name": name, "actual": actual, "expected": expected, "pass": actual == expected})
        if actual != expected:
            raise RuntimeError(f"{name}: {actual!r} != {expected!r}")

    def child(self, operation, source, *options, expected=0):
        command = [sys.executable, "-X", "utf8", "-B"]
        if sys.flags.optimize:
            command.append("-O")
        command += [str(HERE / "model.py"), operation, "--directory", str(source)]
        command += [str(value) for value in options]
        if operation == "recover":
            command += ["--mutation", self.mutation]
        process = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=10)
        self.calls.append({"command": command, "exit": process.returncode, "stdout": process.stdout, "stderr": process.stderr})
        self.check(f"child_{len(self.calls)}_exit", process.returncode, expected)
        value = json.loads(process.stdout)
        return value

    def folder(self, label, original):
        self.case_count += 1
        case = self.output / f"{self.case_count:03d}_{label}"
        case.mkdir()
        source = case / "source"
        shutil.copytree(original, source)
        return source

    def recover(self, source, expected_values=None, generation=None, reason=None):
        before = hashes(source)
        output = source.parent / "recovered"
        result = self.child("recover", source, "--output", output, expected=3 if reason else 0)
        self.check(f"case_{self.case_count}_source_preserved", hashes(source), before)
        if reason:
            self.check(f"case_{self.case_count}_reason", result["reason"], reason)
            self.check(f"case_{self.case_count}_no_output", output.exists(), False)
        else:
            self.check(f"case_{self.case_count}_generation", result["generation"], generation)
            self.check(f"case_{self.case_count}_reported_members", result["members"], expected_values)
            actual = [(output / name).read_bytes().hex() for name in ("D0.bin", "D1.bin", "P.bin")]
            self.check(f"case_{self.case_count}_reopened_bytes", actual, expected_values)
        return result, output


def hashes(directory):
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(directory.iterdir())}


def literal_redo(generation, values, stripe=0):
    # Verifier packing is separate; expected data are fixture literals, never model output.
    header = struct.pack("<4sII12s", b"RDL1", stripe, generation, bytes.fromhex("".join(values)))
    return header + hashlib.sha256(header).digest()


def exercise(checks):
    f = checks.fixture
    original = checks.output / "original"
    checks.child("seed", original)
    original_hash = hashes(original)
    checks.check("original_member_literals", [(original / name).read_bytes().hex() for name in ("D0.bin", "D1.bin", "P.bin")], f["old"])
    for missing in (None, "D0.bin", "D1.bin", "P.bin"):
        source = checks.folder("clean_single_rebuild", original)
        if missing:
            (source / missing).unlink()
        _, recovered = checks.recover(source, f["old"], f["old_generation"])
        second = source.parent / "replayed"
        checks.child("recover", recovered, "--output", second)
        checks.check("clean_idempotent_contents", hashes(second), hashes(recovered))
    for order in f["orders"]:
        for journal in f["journals"]:
            for stop in f["stops"]:
                for missing in (False, True):
                    source = checks.folder(f"{order}_{journal}_{stop}_{missing}", original)
                    observed = checks.child("interrupt", source, "--order", order, "--journal", journal, "--stop", stop)
                    if stop == "member1":
                        key = "mixed_data_first" if order == "data-first" else "mixed_parity_first"
                        checks.check("mixed_literal_members", observed["members"], f[key])
                        checks.check("mixed_parity_mismatch", observed["parity_matches"], False)
                        unsafe = checks.child("unsafe-d1", source)
                        checks.check("wrong_rebuild_literal", unsafe["computed_d1"], f["incorrect_d1"])
                        checks.check("wrong_rebuild_is_not_original", unsafe["computed_d1"] == f["old"][1], False)
                    if missing:
                        (source / "D1.bin").unlink()
                    if stop == "clean":
                        if journal == "incomplete":
                            checks.recover(source, reason="REDO_LENGTH")
                        else:
                            _, recovered = checks.recover(source, f["new"], f["new_generation"])
                    elif stop == "dirty" or journal == "none":
                        checks.recover(source, reason="NEEDS_RECOVERY_DATA")
                    elif journal == "incomplete":
                        checks.recover(source, reason="REDO_LENGTH")
                    else:
                        _, recovered = checks.recover(source, f["new"], f["new_generation"])
                        second = source.parent / "replayed"
                        checks.child("recover", recovered, "--output", second)
                        checks.check("redo_idempotent_contents", hashes(second), hashes(recovered))
    # Every proper prefix of the 56-byte record is insufficient, including the complete 24-byte payload header.
    complete = literal_redo(8, f["new"])
    checks.check("redo_fixed_length", len(complete), f["redo_bytes"])
    for cut in range(56):
        source = checks.folder(f"redo_prefix_{cut}", original)
        checks.child("interrupt", source, "--stop", "member1", "--journal", "none")
        (source / "D1.bin").unlink()
        (source / "redo.bin").write_bytes(complete[:cut])
        checks.recover(source, reason="REDO_LENGTH")
    invalid_logs = [
        ("changed_payload", complete[:15] + bytes([complete[15] ^ 1]) + complete[16:], "REDO_DIGEST"),
        ("stale_generation", literal_redo(6, f["old"]), "REDO_GENERATION"),
        ("wrong_stripe", literal_redo(8, f["new"], stripe=1), "REDO_IDENTITY"),
        ("bad_parity", literal_redo(8, [f["new"][0], f["new"][1], "00000000"]), "REDO_PARITY"),
        ("trailing_byte", complete + b"\x00", "REDO_LENGTH"),
    ]
    for label, raw, reason in invalid_logs:
        source = checks.folder(label, original)
        checks.child("interrupt", source, "--stop", "member1", "--journal", "none")
        (source / "redo.bin").write_bytes(raw)
        checks.recover(source, reason=reason)
    for absent in (("D0.bin", "D1.bin"), ("D0.bin", "P.bin"), ("D1.bin", "P.bin"), ("D0.bin", "D1.bin", "P.bin")):
        source = checks.folder("multiple_missing", original)
        for name in absent:
            (source / name).unlink()
        checks.recover(source, reason="TOO_MANY_MISSING")
    source = checks.folder("dirty_full_redo_two_missing", original)
    checks.child("interrupt", source, "--stop", "member1", "--journal", "full")
    (source / "D0.bin").unlink()
    (source / "D1.bin").unlink()
    checks.recover(source, reason="TOO_MANY_MISSING")
    for length in (0, 3, 5):
        source = checks.folder(f"member_length_{length}", original)
        (source / "D0.bin").write_bytes(b"x" * length)
        checks.recover(source, reason="MEMBER_LENGTH")
    source = checks.folder("parity_corruption", original)
    (source / "P.bin").write_bytes(b"\x00" * 4)
    checks.recover(source, reason="PARITY_MISMATCH")
    source = checks.folder("consistent_corruption", original)
    for name, value in zip(("D0.bin", "D1.bin", "P.bin"), f["consistent_corruption"]):
        (source / name).write_bytes(bytes.fromhex(value))
    observed = checks.child("inspect", source)
    checks.check("consistent_corruption_parity_matches", observed["parity_matches"], True)
    checks.check("consistent_corruption_not_original", observed["members"] == f["old"], False)
    checks.recover(source, f["consistent_corruption"], 7)
    for field, bad, reason in (("generation", True, "META_GENERATION"), ("pending", 8, "META_PENDING"),
                               ("generation", 0, "META_GENERATION"), ("generation", 65535, "META_GENERATION"),
                               ("dirty", 1, "META_DIRTY"), ("stripe", True, "META_IDENTITY")):
        source = checks.folder(f"bad_meta_{field}", original)
        meta = json.loads((source / "meta.json").read_text("ascii"))
        meta[field] = bad
        (source / "meta.json").write_text(json.dumps(meta), encoding="ascii")
        checks.recover(source, reason=reason)
    for generation, dirty, pending, reason in ((65534, False, None, None), (65533, True, 65534, None), (65534, True, 65535, "META_PENDING")):
        source = checks.folder("generation_upper_boundary", original)
        meta = json.loads((source / "meta.json").read_text("ascii"))
        meta.update(generation=generation, dirty=dirty, pending=pending)
        (source / "meta.json").write_text(json.dumps(meta), encoding="ascii")
        if dirty and not reason:
            (source / "redo.bin").write_bytes(literal_redo(65534, f["new"]))
        if reason:
            checks.recover(source, reason=reason)
        else:
            checks.recover(source, f["new"] if dirty else f["old"], 65534)
    source = checks.folder("duplicate_metadata", original)
    (source / "meta.json").write_bytes(b'{"generation":7,"generation":8}')
    checks.recover(source, reason="DUPLICATE_META_KEY")
    source = checks.folder("existing_recovery_output", original)
    destination = source.parent / "existing"
    destination.mkdir()
    (destination / "keep").write_bytes(b"KEEP")
    before = hashes(destination)
    refused = checks.child("recover", source, "--output", destination, expected=3)
    checks.check("existing_output_reason", refused["reason"], "OUTPUT_EXISTS")
    checks.check("existing_output_preserved", hashes(destination), before)
    checks.check("original_preserved", hashes(original), original_hash)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mutation", choices=MUTATIONS, default="none")
    args = parser.parse_args()
    if args.output.exists() or args.output.is_symlink():
        print(json.dumps({"status": "REFUSED", "reason": "OUTPUT_EXISTS"}))
        return 2
    args.output.mkdir(parents=True)
    checks = Checks(args.output, args.mutation)
    sources = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE / "model.py", HERE / "verify.py", HERE / "fixtures.json"]}
    error = None
    try:
        exercise(checks)
        current = {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest() for name in sources}
        checks.check("source_freeze_preserved", current, sources)
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError, KeyError) as caught:
        error = str(caught)
    result = {"status": "ERROR" if error else "PASS", "error": error, "mutation": args.mutation,
              "python": sys.version, "platform": platform.platform(), "optimized": bool(sys.flags.optimize),
              "source_sha256": sources, "checks_count": len(checks.checks), "cases": checks.case_count,
              "child_calls": len(checks.calls), "checks": checks.checks, "calls": checks.calls}
    (args.output / "results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({key: result[key] for key in ("status", "error", "mutation", "checks_count", "cases", "child_calls")}, ensure_ascii=False))
    return 1 if error else 0


if __name__ == "__main__":
    sys.exit(main())
