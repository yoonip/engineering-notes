"""새 프로세스의 파일 갱신·선택·중단 지점을 literal 기대값과 비교합니다."""
import argparse  # 검증 결과를 저장할 새 폴더와 오류 주입을 받습니다.
import copy  # 사례별 fixture를 독립적으로 변경합니다.
from datetime import datetime, timezone  # 실행 시각을 UTC로 기록합니다.
import hashlib  # 소스·입력·산출물 해시를 계산합니다.
import json  # 자식 프로세스의 결과와 저장 상태를 읽습니다.
from pathlib import Path
import platform  # 실제 운영체제·Python 정보를 남깁니다.
import subprocess  # 매 단계 새 Python 프로세스로 파일을 다시 읽습니다.
import sys
import zlib  # CRC32 표준 리터럴을 대조합니다.

from models import metadata_bytes

BASE = Path(__file__).resolve().parent


class ContractError(ValueError):
    """실행 결과가 별도로 적은 기대 계약과 다릅니다."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


class Suite:
    def __init__(self, output: Path, fixture: dict, mutation: str):
        self.output, self.fixture, self.mutation = output, fixture, mutation
        self.commands, self.checks, self.cuts = [], [], []

    def check(self, label: str, actual, expected) -> None:
        require(actual == expected, f"{label}: {actual!r} != {expected!r}")
        self.checks.append({"name": label, "actual": actual, "expected": expected})

    def case(self, name: str, fixture: dict | None = None) -> tuple[Path, Path]:
        folder = self.output / name
        folder.mkdir()
        fixture_path = folder / "input.json"
        fixture_path.write_text(json.dumps(fixture or self.fixture, indent=2) + "\n", encoding="utf-8")
        root = folder / "store"
        self.call(root, fixture_path, "seed")
        return root, fixture_path

    def call(self, root: Path, fixture: Path, action: str, cut: str = "none", code: int = 0, app_ok: bool = False) -> dict:
        command = [sys.executable, "-X", "utf8", "-B"]
        if sys.flags.optimize:
            command.append("-O")  # 자식도 부모와 같은 최적화 검사 조건으로 실행합니다.
        command += [str(BASE / "models.py"), "--root", str(root), "--fixture", str(fixture),
                    "--action", action, "--cut", cut, "--mutation", self.mutation]
        if app_ok:
            command.append("--application-ok")
        run = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=10)
        result = json.loads(run.stdout)
        self.commands.append({"command": command, "exit": run.returncode, "stdout": run.stdout,
                              "stderr": run.stderr, "result": result})
        require(run.returncode == code, f"{action} expected exit {code}, got {run.returncode}: {result}")
        return result

    def state(self, label: str, result: dict, literal: str) -> None:
        expected = self.fixture["expected"][literal]
        self.check(label, {name: result[name] for name in expected}, expected)

    def preserved_a(self, root: Path, label: str) -> None:
        self.check(label, (root / "slotA.bin").read_bytes().hex(), self.fixture["old"]["hex"])

    def happy_and_invalid(self) -> None:
        self.check("CRC32 literal", zlib.crc32(b"123456789"), 0xCBF43926)
        root, fixture = self.case("happy")
        self.call(root, fixture, "install")
        self.state("trial before confirm", self.call(root, fixture, "boot"), "trial")
        self.state("health checkpoint confirmation", self.call(root, fixture, "confirm", app_ok=True), "confirmed")
        self.state("confirmed reboot", self.call(root, fixture, "boot"), "new_stable")
        self.preserved_a(root, "old slot survives confirmed update")
        root, fixture = self.case("unconfirmed")
        self.call(root, fixture, "install")
        self.state("unconfirmed first boot", self.call(root, fixture, "boot"), "trial")
        self.state("unconfirmed next boot", self.call(root, fixture, "boot"), "rollback")

        for name, payload in (("bad_hash", self.fixture["corrupt_hex"]),
                              ("short_image", self.fixture["new"]["hex"][:-2]),
                              ("long_image", self.fixture["new"]["hex"] + "00"),
                              ("oversized_image", "aa" * 33)):
            changed = copy.deepcopy(self.fixture)
            changed["new"]["hex"] = payload
            root, fixture = self.case(name, changed)
            result = self.call(root, fixture, "install", code=3)
            self.check(name + " rejected", result["status"], "REJECTED")
            self.state(name + " old boot remains", self.call(root, fixture, "boot"), "old")

        root, fixture = self.case("confirm_contract")
        self.call(root, fixture, "confirm", code=3, app_ok=True)
        self.call(root, fixture, "install")
        self.call(root, fixture, "confirm", code=3, app_ok=True)
        self.state("confirm needs trial", self.call(root, fixture, "boot"), "trial")
        self.call(root, fixture, "confirm", code=3)
        self.state("missing app checkpoint rolls back", self.call(root, fixture, "boot"), "rollback")

    def cut_matrix(self) -> None:
        for count in range(13):
            root, fixture = self.case(f"image_prefix_{count:02}")
            self.call(root, fixture, "install", f"image:{count}", 23)
            self.preserved_a(root, f"image prefix {count} preserves A")
            self.state(f"image prefix {count} restart", self.call(root, fixture, "boot"), "old")
            self.cuts.append({"phase": "image", "prefix": count, "literal": "old"})
        root, fixture = self.case("after_verified")
        self.call(root, fixture, "install", "verified", 23)
        self.state("verified but unpublished restart", self.call(root, fixture, "boot"), "old")
        self.cuts.append({"phase": "verified", "literal": "old"})
        for phase in ("pending", "trial", "confirm", "rollback"):
            for position in ("zero", "one", "half", "last", "full"):
                root, fixture = self.case(phase + "_" + position)
                if phase != "pending":
                    self.call(root, fixture, "install")
                if phase in ("confirm", "rollback"):
                    self.state(phase + " preparation", self.call(root, fixture, "boot"), "trial")
                action = {"pending": "install", "trial": "boot", "confirm": "confirm", "rollback": "boot"}[phase]
                self.call(root, fixture, action, phase + ":" + position, 23, app_ok=phase == "confirm")
                sizes_at_cut = {path.name: len(path.read_bytes()) for path in root.glob("record*.json")}
                if phase == "pending":
                    literal = "trial" if position == "full" else "old"
                elif phase == "trial":
                    literal = "rollback" if position == "full" else "trial"
                elif phase == "confirm":
                    literal = "new_stable" if position == "full" else "rollback"
                else:
                    literal = "old_stable_after_rollback" if position == "full" else "rollback"
                self.preserved_a(root, phase + " " + position + " preserves A")
                result = self.call(root, fixture, "boot")
                self.state(phase + " " + position + " restarted selection", result, literal)
                sizes = {path.name: len(path.read_bytes()) for path in root.glob("record*.json")}
                self.cuts.append({"phase": phase, "position": position, "literal": literal,
                                  "selected": result["selected"], "generation": result["generation"],
                                  "record_sizes_at_cut": sizes_at_cut, "record_sizes_after_recovery": sizes})
        self.check("finite crash checkpoint count", len(self.cuts), 34)

    def corruption_and_limits(self) -> None:
        root, fixture = self.case("metadata_crc_damage")
        self.call(root, fixture, "install")
        path = root / "record1.json"
        record = json.loads(path.read_text(encoding="utf-8"))
        record["crc32"] ^= 1
        path.write_text(json.dumps(record), encoding="utf-8")
        self.state("invalid newest CRC uses old record", self.call(root, fixture, "boot"), "old")
        for path in root.glob("record*.json"):
            path.write_bytes(b"{")
        self.check("both metadata invalid", self.call(root, fixture, "boot", code=3)["status"], "REJECTED")

        root, fixture = self.case("conflicting_generation")
        old = json.loads((root / "record0.json").read_text(encoding="utf-8"))["state"]
        old["images"]["B"] = self.fixture["new"]["manifest"]
        (root / "record1.json").write_bytes(metadata_bytes(old))
        result = self.call(root, fixture, "boot", code=3)
        self.check("conflicting generation rejected", "conflicting" in result["error"], True)

        root, fixture = self.case("pending_image_damage")
        self.call(root, fixture, "install")
        (root / "slotB.bin").write_bytes(bytes.fromhex(self.fixture["corrupt_hex"]))
        self.state("damaged pending image rejected", self.call(root, fixture, "boot"), "invalid_pending")
        root, fixture = self.case("confirmed_image_damage")
        self.call(root, fixture, "install")
        self.call(root, fixture, "boot")
        self.call(root, fixture, "confirm", app_ok=True)
        (root / "slotB.bin").write_bytes(bytes.fromhex(self.fixture["corrupt_hex"]))
        self.check("damaged confirmed image stops", self.call(root, fixture, "boot", code=3)["status"], "REJECTED")

        forged = copy.deepcopy(self.fixture)
        forged["new"]["hex"] = self.fixture["corrupt_hex"]
        forged["new"]["manifest"]["sha256"] = self.fixture["forged_matching_sha256"]
        root, fixture = self.case("hash_is_not_authorization", forged)
        self.call(root, fixture, "install")
        self.state("matching attacker hash still accepted by this unsigned model", self.call(root, fixture, "boot"), "trial")
        downgraded = copy.deepcopy(self.fixture)
        downgraded["new"] = copy.deepcopy(self.fixture["old"])
        root, fixture = self.case("no_antirollback_policy")
        self.call(root, fixture, "install")
        self.call(root, fixture, "boot")
        self.call(root, fixture, "confirm", app_ok=True)
        alternate = root.parent / "downgrade_input.json"
        alternate.write_text(json.dumps(downgraded), encoding="utf-8")
        self.call(root, alternate, "install")
        self.state("old image accepted because model has no antirollback", self.call(root, alternate, "boot"), "downgrade_trial")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--mutation", choices=("none", "erase-active", "confirm-early", "skip-hash", "single-record"), default="none")
    args = parser.parse_args()
    try:
        args.output.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        parser.error("output already exists")
    hashes = {name: hashlib.sha256((BASE / name).read_bytes()).hexdigest() for name in ("models.py", "verify.py", "fixtures.json")}
    report = {"scope": "separate-process disk-file interruption model; not flash power loss, MCUboot execution or secure boot",
              "utc": datetime.now(timezone.utc).isoformat(), "python": sys.version, "executable": sys.executable,
              "platform": platform.platform(), "optimize": sys.flags.optimize, "argv": sys.argv,
              "source_and_input_sha256": hashes, "mutation": args.mutation}
    suite = Suite(args.output, json.loads((BASE / "fixtures.json").read_text(encoding="utf-8")), args.mutation)
    try:
        suite.cut_matrix()
        suite.happy_and_invalid()
        suite.corruption_and_limits()
        report["status"] = "passed"
    except Exception as error:
        report.update(status="failed", error=f"{type(error).__name__}: {error}")
    report.update(checks=suite.checks, cut_matrix=suite.cuts, child_commands=suite.commands,
                  child_processes=len(suite.commands))
    report["file_sha256"] = {str(path.relative_to(args.output)): hashlib.sha256(path.read_bytes()).hexdigest()
                             for path in args.output.rglob("*") if path.is_file()}
    (args.output / "results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "checks": len(suite.checks), "cuts": len(suite.cuts),
                      "child_processes": len(suite.commands), "error": report.get("error")}, ensure_ascii=False))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
