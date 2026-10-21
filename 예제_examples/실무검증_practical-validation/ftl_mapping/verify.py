"""FTL 파일·새 프로세스·리터럴 상태·중단 prefix·GC/주소 재사용을 검사합니다."""
import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import zlib

from models import (CRC, FtlError, MUTATIONS, NONE, physical_record, write, trim, payload,
                    decode_physical, decode_mapping)

BASE = Path(__file__).resolve().parent


def require(condition, reason):
    if not condition:  # 명시적 예외를 사용해 -O에서도 기대값 비교를 남깁니다.
        raise RuntimeError(reason)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Suite:
    def __init__(self, output, fixture, mutation):
        self.output, self.fixture, self.mutation = output, fixture, mutation
        self.checks, self.commands, self.cuts, self.controls, self.trace = [], [], [], [], []

    def check(self, name, actual, expected):
        require(actual == expected, f"{name}: {actual!r} != {expected!r}")
        self.checks.append({"name": name, "actual": actual, "expected": expected})

    def call(self, root, action, code=0, mutation=None, **options):
        command = [sys.executable, "-X", "utf8", "-B"] + (["-O"] if sys.flags.optimize else [])
        command += [str(BASE / "models.py"), "--root", str(root), "--fixture", str(BASE / "fixtures.json"),
                    "--action", action, "--mutation", self.mutation if mutation is None else mutation]
        for name, value in options.items():
            command += ["--" + name, str(value)]  # 사전의 옵션을 shell 없이 인수 목록으로 전달합니다.
        run = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=10)
        result = json.loads(run.stdout)
        self.commands.append({"command": command, "exit": run.returncode, "stdout": run.stdout,
                              "stderr": run.stderr, "result": result})
        require(run.returncode == code, f"{action}: expected exit {code}, got {run.returncode}: {result}")
        return result

    def case(self, name):
        folder = self.output / name
        folder.mkdir()
        root = folder / "store"
        self.call(root, "seed")
        return root

    def state(self, label, root, expected, mutation=None):
        result = self.call(root, "inspect", mutation=mutation)
        self.check(label, {key: result[key] for key in expected}, expected)
        return result

    def file_hashes(self, root):
        return {name: sha(root / name) for name in ("physical.log", "mapping.log")}

    def inject(self, path, raw):
        with path.open("wb") as stream:
            require(stream.write(raw) == len(raw), "injection short write")
            stream.flush()
            os.fsync(stream.fileno())

    def basics(self):
        e = self.fixture["expected"]
        self.check("CRC32 standard literal", zlib.crc32(b"123456789"), 0xCBF43926)
        root = self.case("happy")
        self.check("physical seed bytes", (root / "physical.log").read_bytes().hex(), e["seed_physical_hex"])
        self.check("mapping seed bytes", (root / "mapping.log").read_bytes().hex(), e["seed_mapping_hex"])
        self.check("seed hashes", self.file_hashes(root), {"physical.log": e["seed_physical_sha256"], "mapping.log": e["seed_mapping_sha256"]})
        self.state("seed mapping literal", root, e["seed"])
        self.call(root, "write", lpn=0, data="aaaa0001")
        self.check("physical update bytes", (root / "physical.log").read_bytes().hex(), e["seed_physical_hex"] + e["update_physical_hex"])
        self.check("mapping update bytes", (root / "mapping.log").read_bytes().hex(), e["seed_mapping_hex"] + e["update_mapping_hex"])
        self.state("published mapping literal", root, e["updated"])
        before = self.file_hashes(root)
        self.state("repeat reconstruction", root, e["updated"])
        self.check("readonly reconstruction", self.file_hashes(root), before)

        root = self.case("trim")
        self.call(root, "trim", lpn=0)
        self.state("durable tombstone returns None", root, e["trimmed"])
        self.check("trim leaves physical history", (root / "physical.log").read_bytes().hex(), e["seed_physical_hex"])

        root = self.case("gc")
        job = root.parent / "job.json"
        planned = self.call(root, "plan-gc", block=0, job=job)
        self.check("initial GC capacity", planned, {"status": "PLANNED", "block": 0, "live_pages": 1, "temporary_pages_available": 7})
        self.call(root, "finish-gc", job=job)
        self.state("copy publish erase GC literal", root, e["gc"])

        root = self.case("stale_gc")
        job = root.parent / "old-job.json"
        self.call(root, "plan-gc", block=0, job=job)
        self.call(root, "write", lpn=0, data="aaaa0001")
        before = self.file_hashes(root)
        rejected = self.call(root, "finish-gc", code=3, job=job)
        self.check("old GC cannot replace new host version", [rejected["reason"], self.file_hashes(root)], ["STALE_GC_SNAPSHOT", before])
        self.state("stale GC preserves current mapping", root, e["updated"])

        root = self.case("gc_new_live_page_in_victim")
        job = root.parent / "old-job.json"
        self.call(root, "plan-gc", block=0, job=job)
        self.call(root, "write", lpn=1, data="bbbb0002")
        rejected = self.call(root, "finish-gc", code=3, job=job)
        self.check("GC cannot erase a newly live victim page", rejected["reason"], "ERASE_LIVE_BLOCK")
        self.state("GC may publish an earlier copy before final erase rejection", root,
                   {"values": ["11111111", "bbbb0002", "33333333"], "versions": [1, 2, 1],
                    "ppns": [4, 1, 6], "incarnations": [5, 4, 3], "valid": 3, "stale": 2,
                    "free": 7, "data_records": 5, "map_records": 5, "tails": {"data": 0, "map": 0}})

        root = self.case("trim_reuse")
        old_job, empty_job = root.parent / "old-job.json", root.parent / "empty-job.json"
        self.call(root, "plan-gc", block=0, job=old_job)
        self.call(root, "trim", lpn=0)
        self.call(root, "plan-gc", block=0, job=empty_job)
        self.call(root, "finish-gc", job=empty_job)
        self.call(root, "write", lpn=1, data="bbbb0002")
        self.state("PPN0 reused by different LPN incarnation5", root, e["reused"])
        before = self.file_hashes(root)
        rejected = self.call(root, "finish-gc", code=3, job=old_job)
        self.check("pretrim GC cannot touch reused PPN", [rejected["reason"], self.file_hashes(root)], ["STALE_GC_SNAPSHOT", before])

    def bad_path_controls(self):
        e = self.fixture["expected"]
        for mutation in ("publish-first", "erase-old-first"):
            root = self.case("control_" + mutation)
            self.call(root, "write", mutation=mutation, lpn=0, data="aaaa0001", stage="data", cut=0, code=23)
            result = self.call(root, "inspect", mutation="none", code=3)
            self.check(mutation + " interruption leaves missing mapped page", result["reason"], "MAPPED_PAGE_MISSING")
            self.controls.append({"mutation": mutation, "observed": result})
        root = self.case("control_wrong_identity")
        result = self.call(root, "write", mutation="wrong-page-identity", lpn=0, data="aaaa0001", code=3)
        self.check("wrong LPN readback blocks map publication", result["reason"], "WRITE_READBACK_IDENTITY")
        expected = copy.deepcopy(e["seed"])
        expected.update(stale=1, free=8, data_records=4)
        self.state("rejected identity leaves old map and orphan", root, expected, mutation="none")
        self.controls.append({"mutation": "wrong-page-identity", "observed": result})

        root = self.case("control_stale_gc")
        job = root.parent / "job.json"
        self.call(root, "plan-gc", block=0, job=job)
        self.call(root, "write", mutation="none", lpn=0, data="aaaa0001")
        self.call(root, "finish-gc", mutation="stale-gc", job=job)
        bad = self.call(root, "inspect", mutation="stale-gc")
        self.check("unguarded GC exposes old version", [bad["values"], bad["versions"]], [e["seed"]["values"], [1, 1, 1]])
        rejected = self.call(root, "inspect", mutation="none", code=3)
        self.check("correct reader rejects stale GC record", rejected["reason"], "MAP_BASE_CHANGED")
        self.controls.append({"mutation": "stale-gc", "bad_values": bad["values"], "correct_reader": rejected})

        root = self.case("control_ignore_trim")
        self.call(root, "trim", mutation="none", lpn=0)
        bad = self.call(root, "inspect", mutation="ignore-trim")
        self.check("ignoring tombstone exposes old page", bad["values"], e["seed"]["values"])
        self.state("same file correct reader preserves tombstone", root, e["trimmed"], mutation="none")
        self.controls.append({"mutation": "ignore-trim", "bad_values": bad["values"]})

    def workload(self):
        e = self.fixture["expected"]
        root = self.case("workload")
        for lpn, data in self.fixture["workload"]:
            self.call(root, "write", lpn=lpn, data=data)
        before = self.state("six host writes before GC", root, e["trace_before_gc"])
        job = root.parent / "first-job.json"
        self.call(root, "plan-gc", block=0, job=job)
        self.call(root, "finish-gc", job=job)
        after = self.state("one live copy net free gain two", root, e["trace_after_gc"])
        self.check("GC capacity arithmetic", [before["free"], after["free"], after["free"] - before["free"]], [3, 5, 2])
        self.trace.append({"host_data_writes_after_seed": 6, "data_allocations_including_GC_after_seed": 7,
                           "ratio_numerator": 7, "ratio_denominator": 6, "before": before, "after": after})
        self.call(root, "trim", lpn=0)
        empty = root.parent / "second-job.json"
        self.call(root, "plan-gc", block=3, job=empty)
        self.call(root, "finish-gc", job=empty)
        self.call(root, "write", lpn=2, data="cccc0003")
        self.state("trim erase and PPN0 incarnation13 reuse", root, e["trace_final"])

        root = self.case("temporary_capacity")
        for number in range(1, 9):
            self.call(root, "write", lpn=0, data=f"{number:02x}000000")
        result = self.call(root, "inspect")
        self.check("one free page can be inside victim", [result["ppns"], result["free"]], [[10, 3, 6], 1])
        rejected = self.call(root, "plan-gc", block=3, job=root.parent / "bad-job.json", code=3)
        self.check("GC needs temporary space outside victim", rejected["reason"], "NO_GC_TEMP_SPACE")
        rejected = self.call(root, "write", lpn=0, data="09000000", code=3)
        self.check("host write preserves GC reserve", rejected["reason"], "GC_RESERVE_REQUIRED")
        job = root.parent / "empty-job.json"
        self.call(root, "plan-gc", block=0, job=job)
        self.call(root, "finish-gc", job=job)
        self.check("stale-only block releases space", self.call(root, "inspect")["free"], 4)

    def corruption_and_inputs(self):
        e = self.fixture["expected"]
        physical_seed, map_seed = bytes.fromhex(e["seed_physical_hex"]), bytes.fromhex(e["seed_mapping_hex"])
        data, mapping = bytes.fromhex(e["update_physical_hex"]), bytes.fromhex(e["update_mapping_hex"])
        corruptions = [
            ("wrong_lpn", physical_seed + bytes.fromhex(e["wrong_lpn_physical_hex"]), map_seed + mapping, "PAGE_IDENTITY"),
            ("wrong_version", physical_seed + bytes.fromhex(e["wrong_version_physical_hex"]), map_seed + mapping, "PAGE_IDENTITY"),
            ("wrong_incarnation", physical_seed + data, map_seed + bytes.fromhex(e["wrong_incarnation_mapping_hex"]), "PAGE_IDENTITY"),
            ("wrong_mapping_base", physical_seed + data, map_seed + bytes.fromhex(e["wrong_base_mapping_hex"]), "MAP_BASE_CHANGED"),
            ("physical_crc", physical_seed + data[:-1] + bytes((data[-1] ^ 1,)), map_seed + mapping, "RECORD_CRC"),
            ("mapping_crc", physical_seed + data, map_seed + mapping[:-1] + bytes((mapping[-1] ^ 1,)), "RECORD_CRC"),
            ("program_occupied", physical_seed + physical_record(1, 4, 0, 0, 2, bytes.fromhex("aaaa0001")), map_seed, "PROGRAM_OCCUPIED_PAGE"),
            ("physical_sequence", physical_seed + physical_record(1, 5, 1, 0, 2, bytes.fromhex("aaaa0001")), map_seed, "PHYSICAL_SEQUENCE"),
            ("erase_live", physical_seed + physical_record(2, 4, 0), map_seed, "MAPPED_PAGE_MISSING"),
        ]
        for name, physical, metadata, reason in corruptions:
            root = self.case("corrupt_" + name)
            self.inject(root / "physical.log", physical)
            self.inject(root / "mapping.log", metadata)
            result = self.call(root, "inspect", code=3)
            self.check(name + " rejection literal", [result["reason"], "values" in result], [reason, False])
        root = self.case("unresolved_tail")
        self.call(root, "write", lpn=0, stage="data", cut=1, code=23)
        before = self.file_hashes(root)
        result = self.call(root, "write", lpn=0, code=3)
        self.check("partial tail blocks append without modifying files", [result["reason"], self.file_hashes(root)], ["TAIL_NEEDS_REPAIR", before])
        root = self.case("erase_guard")
        result = self.call(root, "erase-empty", block=0, code=3)
        self.check("live block cannot be erased", result["reason"], "ERASE_LIVE_BLOCK")

        cases = [
            ("bool_lpn", lambda: write(root, True, "01020304"), "LPN_RANGE"),
            ("negative_lpn", lambda: trim(root, -1), "LPN_RANGE"),
            ("lpn3", lambda: trim(root, 3), "LPN_RANGE"),
            ("odd_hex", lambda: payload("123"), "DATA_HEX"),
            ("nonhex", lambda: payload("xxxxxxxx"), "DATA_HEX"),
            ("space_hex", lambda: payload("11 22 33"), "DATA_HEX"),
            ("data_bytes_not_hex_string", lambda: payload(bytes(4)), "DATA_HEX"),
            ("ppn12", lambda: physical_record(1, 1, 12, 0, 1), "PHYSICAL_ADDRESS"),
            ("version0", lambda: physical_record(1, 1, 0, 0, 0), "VERSION_RANGE"),
            ("incarnation65536", lambda: physical_record(1, 65536, 0, 0, 1), "PHYSICAL_SEQUENCE_RANGE"),
            ("physical_file_header", lambda: decode_physical(b"DAT"), "FILE_MAGIC"),
            ("mapping_file_header", lambda: decode_mapping(b"BAD1"), "FILE_MAGIC"),
            ("oversized_file", lambda: decode_physical(b"DAT1" + bytes(65533)), "FILE_SIZE"),
        ]
        for name, function, reason in cases:
            try:
                function()
            except FtlError as exc:
                self.check(name, str(exc), reason)
            else:
                raise RuntimeError(name + " accepted")
        self.check("maximum encoded physical fields size", len(physical_record(1, 65535, 11, 2, 65535)), 32)

    def cut_matrices(self):
        e = self.fixture["expected"]
        for stage, size in (("data", 32), ("map", 48)):
            for cut in range(size + 1):
                root = self.case(f"write_{stage}_{cut:02}")
                self.call(root, "write", lpn=0, data="aaaa0001", stage=stage, cut=cut, code=23)
                expected = copy.deepcopy(e["updated"] if stage == "map" and cut == 48 else e["seed"])
                if stage == "data":
                    expected["tails"]["data"] = cut % 32
                    if cut == 32:
                        expected.update(stale=1, free=8, data_records=4)
                elif cut < 48:
                    expected.update(stale=1, free=8, data_records=4)
                    expected["tails"]["map"] = cut
                self.state(f"write {stage} prefix {cut}", root, expected)
                self.check(f"write {stage} prefix {cut} bytes", {
                    "physical": (root / "physical.log").read_bytes().hex(), "mapping": (root / "mapping.log").read_bytes().hex()}, {
                    "physical": e["seed_physical_hex"] + e["update_physical_hex"][:cut * 2] if stage == "data" else e["seed_physical_hex"] + e["update_physical_hex"],
                    "mapping": e["seed_mapping_hex"] if stage == "data" else e["seed_mapping_hex"] + e["update_mapping_hex"][:cut * 2]})
                self.cuts.append({"operation": "write", "stage": stage, "prefix": cut, "expected": expected})

        for stage, size in (("data", 32), ("map", 48), ("erase", 32)):
            for cut in (0, 1, size - 1, size):
                root = self.case(f"gc_{stage}_{cut:02}")
                job = root.parent / "job.json"
                self.call(root, "plan-gc", block=0, job=job)
                self.call(root, "finish-gc", job=job, stage=stage, cut=cut, code=23)
                expected = copy.deepcopy(e["seed"])
                if stage == "data":
                    expected["tails"]["data"] = cut % 32
                    if cut == 32:
                        expected.update(stale=1, free=8, data_records=4)
                else:
                    expected.update(stale=1, free=8, data_records=4)
                    if stage == "map" and cut < 48:
                        expected["tails"]["map"] = cut
                    else:
                        expected.update(ppns=[4, 3, 6], incarnations=[4, 2, 3], map_records=4)
                        if stage == "erase":
                            expected["tails"]["data"] = cut % 32
                            if cut == 32:
                                expected.update(stale=0, free=9, data_records=5)
                self.state(f"GC {stage} prefix {cut}", root, expected)
                self.cuts.append({"operation": "gc", "stage": stage, "prefix": cut, "expected": expected})
        for cut in (0, 1, 47, 48):
            root = self.case(f"trim_map_{cut:02}")
            self.call(root, "trim", lpn=0, stage="map", cut=cut, code=23)
            expected = copy.deepcopy(e["trimmed"] if cut == 48 else e["seed"])
            expected["tails"]["map"] = cut % 48
            self.state(f"TRIM map prefix {cut}", root, expected)
            self.cuts.append({"operation": "trim", "stage": "map", "prefix": cut, "expected": expected})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mutation", choices=MUTATIONS, default="none")
    args = parser.parse_args()
    output = args.output.resolve()
    try:
        output.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        parser.error("output already exists: " + str(output))
    hashes = {name: sha(BASE / name) for name in ("models.py", "verify.py", "fixtures.json")}
    report = {"scope": "append-only host event files and fresh Python processes; no NAND, SSD firmware, NVMe command, OS crash or hardware power cut",
              "utc": datetime.now(timezone.utc).isoformat(), "python": sys.version, "executable": sys.executable,
              "platform": platform.platform(), "argv": sys.argv, "optimize": sys.flags.optimize,
              "mutation": args.mutation, "source_and_input_sha256": hashes}
    suite = Suite(output, json.loads((BASE / "fixtures.json").read_text(encoding="utf-8")), args.mutation)
    try:
        suite.basics()
        suite.bad_path_controls()
        suite.workload()
        suite.corruption_and_inputs()
        suite.cut_matrices()
        require(hashes == {name: sha(BASE / name) for name in hashes}, "source changed during execution")
        report["status"] = "PASS"
    except Exception as exc:
        report.update(status="ERROR", exception=type(exc).__name__, message=str(exc))
    report.update(checks=suite.checks, cuts=suite.cuts, commands=suite.commands, bad_controls=suite.controls, workload=suite.trace)
    report["counts"] = {"checks": len(suite.checks), "cuts": len(suite.cuts), "subprocesses": len(suite.commands),
                        "bad_controls": len(suite.controls), "workload_summaries": len(suite.trace)}
    (output / "results.json").write_bytes((json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({"status": report["status"], "output": str(output), **report["counts"]}, ensure_ascii=False))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
