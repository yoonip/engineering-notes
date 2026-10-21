"""실제 파일 prefix 중단·새 프로세스 복구·고정 기대값·오류 변이를 검사합니다."""
import argparse
import copy  # 바꾼 입력이 원본 fixture와 섞이지 않게 복사합니다.
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess  # seed·append·recover를 매번 새 Python 프로세스로 실행합니다.
import sys
import zlib

from models import JournalError, frame, recover_bytes

BASE = Path(__file__).resolve().parent
MUTATIONS = ("none", "apply-uncommitted", "ignore-crc", "ignore-sequence", "commit-first")


def require(condition, message):
    if not condition:  # assert를 사용하지 않아 -O에서도 검사가 사라지지 않습니다.
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Suite:
    def __init__(self, output, fixture, mutation):
        self.output, self.fixture, self.mutation = output, fixture, mutation
        self.commands, self.checks, self.cuts, self.injections = [], [], [], []

    def check(self, name, actual, expected):
        require(actual == expected, f"{name}: {actual!r} != {expected!r}")
        self.checks.append({"name": name, "actual": actual, "expected": expected})

    def call(self, root, fixture, action, expected_exit=0, cut=-1):
        command = [sys.executable, "-X", "utf8", "-B"]
        if sys.flags.optimize:
            command.append("-O")  # 자식에도 같은 최적화 조건을 전달합니다.
        command += [str(BASE / "models.py"), "--root", str(root), "--fixture", str(fixture),
                    "--action", action, "--mutation", self.mutation, "--cut", str(cut)]
        run = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=10)
        result = json.loads(run.stdout)
        self.commands.append({"command": command, "exit": run.returncode,
                              "stdout": run.stdout, "stderr": run.stderr, "result": result})
        require(run.returncode == expected_exit,
                f"{action} expected exit {expected_exit}, got {run.returncode}: {result}")
        return result

    def case(self, name, fixture=None):
        folder = self.output / name
        folder.mkdir()
        input_path = folder / "input.json"
        input_path.write_text(json.dumps(self.fixture if fixture is None else fixture, indent=2) + "\n", encoding="utf-8")
        store = folder / "store"
        self.call(store, input_path, "seed")
        return store, input_path

    def inject(self, root, raw, label):
        with (root / "journal.bin").open("wb") as stream:
            require(stream.write(raw) == len(raw), "fault injection short write")
            stream.flush()
            os.fsync(stream.fileno())
        self.injections.append({"label": label, "file": str(root / "journal.bin"),
                                "bytes": len(raw), "sha256": sha(root / "journal.bin")})

    def literals_and_faults(self):
        e = self.fixture["expected"]
        self.check("standard CRC32 literal", zlib.crc32(b"123456789"), 0xCBF43926)
        root, fixture = self.case("happy")
        self.check("seed encoded bytes literal", (root / "journal.bin").read_bytes().hex(), e["seed_file_hex"])
        self.check("seed file size literal", (root / "journal.bin").stat().st_size, 64)
        self.check("seed SHA256 literal", sha(root / "journal.bin"), e["seed_sha256"])
        self.call(root, fixture, "append")
        expected_hex = e["seed_file_hex"] + e["update_batch_hex"]
        self.check("normal appended bytes literal", (root / "journal.bin").read_bytes().hex(), expected_hex)
        got = self.call(root, fixture, "recover")
        self.check("normal recovered state literal", got["state"], {"credit": 80, "stock": 7})
        self.check("normal recovered sequence literal", [got["sequence"], got["commits"], got["tail_kind"]], [2, [1, 2], "CLEAN"])
        self.check("normal journal SHA256 literal", got["journal_sha256"], e["complete_sha256"])
        before = sha(root / "journal.bin")
        again = self.call(root, fixture, "recover")
        self.check("recovery is readonly and repeatable", [again, sha(root / "journal.bin")], [got, before])
        (root.parent / "recovered.json").write_text(json.dumps(got, indent=2) + "\n", encoding="utf-8")

        root, fixture = self.case("uncommitted_data")
        self.call(root, fixture, "append", expected_exit=23, cut=39)
        got = self.call(root, fixture, "recover")
        self.check("DATA alone cannot publish new values", got["state"], {"credit": 50, "stock": 10})
        self.check("DATA alone ignored tail literal", [got["sequence"], got["tail_kind"], got["ignored_bytes"]], [1, "UNCOMMITTED_DATA", 39])
        before = sha(root / "journal.bin")
        refused = self.call(root, fixture, "append", expected_exit=3)
        self.check("append refuses unresolved tail", [refused["reason"], sha(root / "journal.bin")], ["TAIL_NEEDS_REPAIR", before])

        seed = bytes.fromhex(e["seed_file_hex"])
        data, commit = bytes.fromhex(e["update_data_hex"]), bytes.fromhex(e["update_commit_hex"])
        bad_data = data[:-1] + bytes((data[-1] ^ 1,))
        bad_commit = commit[:-1] + bytes((commit[-1] ^ 1,))
        bad_length = data[:6] + b"\x81\x00" + data[8:]
        corruptions = [
            ("data_crc", bad_data + commit, "FRAME_CRC"),
            ("commit_crc", data + bad_commit, "FRAME_CRC"),
            ("internal_crc_not_resynchronized", bad_data + commit + bytes.fromhex(e["third_batch_hex"]), "FRAME_CRC"),
            ("frame_magic", b"X" + data[1:] + commit, "FRAME_MAGIC"),
            ("length_above_limit", bad_length + commit, "INTEGER_1_128"),
            ("sequence_gap", bytes.fromhex(e["gap_batch_hex"]), "DATA_SEQUENCE"),
            ("commit_before_data", commit + data, "COMMIT_WITHOUT_DATA"),
            ("commit_sequence", data + bytes.fromhex(e["gap_batch_hex"])[39:], "COMMIT_SEQUENCE"),
            ("commit_binding", data + bytes.fromhex(e["bad_binding_commit_hex"]), "COMMIT_BINDING"),
            ("duplicate_json_key", bytes.fromhex(e["duplicate_json_data_hex"]) + commit, "DATA_CANONICAL"),
            ("boolean_json_value", bytes.fromhex(e["boolean_json_data_hex"]) + commit, "INTEGER_0_1000"),
            ("second_uncommitted_data", data + data + commit, "SECOND_DATA_BEFORE_COMMIT"),
        ]
        for name, suffix, reason in corruptions:
            root, fixture = self.case("corrupt_" + name)
            self.inject(root, seed + suffix, name)
            got = self.call(root, fixture, "recover", expected_exit=3)
            self.check(name + " strict rejection", [got["status"], got["reason"]], ["REJECTED", reason])
            self.check(name + " does not publish state", "state" in got, False)

        root, fixture = self.case("ambiguous_length_tail")
        longer_header = data[:6] + b"\x80\x00" + data[8:]
        self.inject(root, seed + longer_header + commit + bytes.fromhex(e["third_batch_hex"]), "length damage looks incomplete")
        got = self.call(root, fixture, "recover")
        self.check("legal-range length damage is ambiguous", [got["state"], got["sequence"], got["tail_kind"], got["ignored_bytes"], got["file_bytes"]],
                   [{"credit": 50, "stock": 10}, 1, "INCOMPLETE_FRAME", 118, 182])

    def boundaries(self):
        changed = copy.deepcopy(self.fixture)
        changed["update"]["values"] = {"credit": 0, "stock": 1000}
        root, fixture = self.case("value_boundaries", changed)
        self.call(root, fixture, "append")
        self.check("inclusive value bounds", self.call(root, fixture, "recover")["state"], {"credit": 0, "stock": 1000})
        invalid = [
            ("bool_sequence", {"seq": True, "values": {"credit": 80, "stock": 7}}, "APPEND_SEQUENCE"),
            ("zero_sequence", {"seq": 0, "values": {"credit": 80, "stock": 7}}, "APPEND_SEQUENCE"),
            ("gap_sequence", {"seq": 3, "values": {"credit": 80, "stock": 7}}, "APPEND_SEQUENCE"),
            ("over_sequence", {"seq": 65536, "values": {"credit": 80, "stock": 7}}, "APPEND_SEQUENCE"),
            ("bool_value", {"seq": 2, "values": {"credit": True, "stock": 7}}, "INTEGER_0_1000"),
            ("negative_value", {"seq": 2, "values": {"credit": -1, "stock": 7}}, "INTEGER_0_1000"),
            ("over_value", {"seq": 2, "values": {"credit": 1001, "stock": 7}}, "INTEGER_0_1000"),
            ("missing_key", {"seq": 2, "values": {"stock": 7}}, "VALUE_KEYS"),
            ("extra_key", {"seq": 2, "values": {"credit": 80, "stock": 7, "extra": 1}}, "VALUE_KEYS"),
            ("extra_request", {"seq": 2, "values": {"credit": 80, "stock": 7}, "extra": 1}, "REQUEST_KEYS"),
        ]
        for name, update, reason in invalid:
            changed = copy.deepcopy(self.fixture)
            changed["update"] = update
            root, fixture = self.case("invalid_" + name, changed)
            before = sha(root / "journal.bin")
            got = self.call(root, fixture, "append", expected_exit=3)
            self.check(name + " rejected before append", [got["reason"], sha(root / "journal.bin")], [reason, before])
        for name, function, reason in [
            ("file_header_missing", lambda: recover_bytes(b""), "FILE_HEADER"),
            ("file_header_partial", lambda: recover_bytes(b"JNL"), "FILE_HEADER"),
            ("file_limit_exceeded", lambda: recover_bytes(b"JNL1" + b"\x00" * 65533), "LOG_SIZE"),
            ("payload_over128", lambda: frame(1, 1, b"x" * 129), "PAYLOAD_LENGTH"),
            ("payload_empty", lambda: frame(1, 1, b""), "PAYLOAD_LENGTH"),
            ("commit_length3", lambda: frame(2, 1, b"abc"), "COMMIT_LENGTH"),
            ("sequence_upper_exceeded", lambda: frame(1, 65536, b"x"), "INTEGER_1_65535"),
        ]:
            try:
                function()
            except JournalError as exc:
                self.check(name, str(exc), reason)
            else:
                raise RuntimeError(name + " was accepted")
        self.check("payload128 frame size", len(frame(1, 65535, b"x" * 128)), 144)
        self.check("empty valid journal", recover_bytes(b"JNL1"), {"state": {}, "sequence": 0, "commits": [],
                   "committed_end": 4, "tail_kind": "CLEAN", "ignored_bytes": 0, "file_bytes": 4})

    def cut_matrix(self):
        e = self.fixture["expected"]
        self.check("matrix sizes are fixed literals", [e["seed_file_bytes"], e["update_data_bytes"], e["update_commit_bytes"], e["update_batch_bytes"]], [64, 39, 20, 59])
        seed_hex, batch_hex = e["seed_file_hex"], e["update_batch_hex"]
        for cut in range(60):  # 선택한 59바이트 트랜잭션의 prefix 0~59를 빠짐없이 실행합니다.
            root, fixture = self.case(f"cut_{cut:02}")
            self.call(root, fixture, "append", expected_exit=23, cut=cut)
            self.check(f"cut {cut} persisted byte prefix", (root / "journal.bin").read_bytes().hex(), seed_hex + batch_hex[:cut * 2])
            got = self.call(root, fixture, "recover")
            full = cut == 59
            tail = "CLEAN" if cut in (0, 59) else "UNCOMMITTED_DATA" if cut == 39 else "INCOMPLETE_FRAME"
            expected = {"state": {"credit": 80, "stock": 7} if full else {"credit": 50, "stock": 10},
                        "sequence": 2 if full else 1, "commits": [1, 2] if full else [1],
                        "committed_end": 123 if full else 64, "tail_kind": tail,
                        "ignored_bytes": 0 if full else cut, "file_bytes": 64 + cut}
            actual = {key: got[key] for key in expected}
            self.check(f"cut {cut} recovery literal", actual, expected)
            self.cuts.append({"prefix_bytes": cut, "actual": actual})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mutation", choices=MUTATIONS, default="none")
    args = parser.parse_args()
    output = args.output.resolve()
    try:
        output.mkdir(parents=True, exist_ok=False)  # 이미 있는 결과 폴더는 만들지 않습니다.
    except FileExistsError:
        parser.error("output already exists: " + str(output))
    hashes = {name: sha(BASE / name) for name in ("models.py", "verify.py", "fixtures.json")}
    report = {"scope": "real host files, synced selected prefixes and explicit child exit; no OS crash, storage power cut, filesystem durability or SQLite execution",
              "python": sys.version, "executable": sys.executable, "platform": platform.platform(),
              "argv": sys.argv, "optimize": sys.flags.optimize, "utc": datetime.now(timezone.utc).isoformat(),
              "mutation": args.mutation, "source_and_input_sha256": hashes}
    suite = Suite(output, json.loads((BASE / "fixtures.json").read_text(encoding="utf-8")), args.mutation)
    try:
        suite.literals_and_faults()
        suite.boundaries()
        suite.cut_matrix()
        require(hashes == {name: sha(BASE / name) for name in hashes}, "source changed during execution")
        report["status"] = "PASS"
    except Exception as exc:
        report.update(status="ERROR", exception=type(exc).__name__, message=str(exc))
    report.update(checks=suite.checks, cuts=suite.cuts, commands=suite.commands, injections=suite.injections)
    report["counts"] = {"checks": len(suite.checks), "cuts": len(suite.cuts), "subprocesses": len(suite.commands),
                        "intentional_fault_files": len(suite.injections)}
    (output / "results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "output": str(output), **report["counts"]}, ensure_ascii=False))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
