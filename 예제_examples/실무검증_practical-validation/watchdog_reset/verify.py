"""워치독 모형의 literal 기대값·순환 경계·오류 대조를 새 결과 폴더에 기록합니다."""
import argparse  # 명령행 인수를 읽습니다.
from datetime import datetime, timezone  # UTC 실행 시각을 기록합니다.
import hashlib  # 파일 내용의 SHA-256을 계산합니다.
import json  # JSON 입력과 결과를 다룹니다.
from pathlib import Path  # 파일 경로를 객체로 표현합니다.
import platform  # 운영체제 정보를 읽습니다.
import sys  # 실행파일·종료 코드·최적화 수준을 읽습니다.

from models import BootLedger, HealthGate, ResetLatch, boot_sequence, elapsed, monitor, window_action


class ContractError(ValueError):
    """입력으로 정한 계약과 관측이 다를 때 발생합니다."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)  # assert를 쓰지 않아 -O에서도 검사를 유지합니다.


def rejected(callback, expected_type=ContractError) -> dict:
    try:
        callback()
    except expected_type as error:
        return {"detected": True, "error": f"{type(error).__name__}: {error}"}
    raise ContractError("intentional faulty path or invalid input escaped detection")


def check_monitor(observed: dict, expected: dict) -> None:
    require(observed["feeds"] == expected["feeds"], "feed sequence differs from literal expectation")
    require(observed["reset_at"] == expected["reset_at"], "reset time differs from literal expectation")
    actions = [item["action"] for item in observed["trace"]]
    require(actions == expected["actions"], "window actions differ from literal expectation")


def check_boot(observed: list[dict], expected: dict) -> None:
    require([item["failures"] for item in observed] == expected["boot_failures"], "boot streak differs")
    require([item["mode"] for item in observed] == expected["boot_modes"], "boot recovery policy differs")


def run_checks(fixture: dict, inject: str | None) -> dict:
    expected = fixture["literal_expected"]
    main = monitor(fixture["monitor"], periodic_feed=inject == "periodic-feed",
                   raw_deadline=inject == "raw-deadline")
    check_monitor(main, expected["gated"])
    periodic = monitor(fixture["monitor"], periodic_feed=True)
    check_monitor(periodic, expected["periodic"])
    windows = []
    for item in expected["window"]:
        action = window_action(item["now"], item["start"], item["requested"])
        require(action == item["action"], "literal window boundary differs")
        windows.append({**item, "actual": action})

    sweep = 0
    for initial in range(256):
        current = initial
        for unwrapped_age in range(128):
            require(elapsed(current, initial) == unwrapped_age, "elapsed differs from advancing clock oracle")
            wanted = "reset_late" if unwrapped_age >= 12 else ("reset_early" if unwrapped_age < 4 else "feed")
            require(window_action(current, initial, True) == wanted, "window sweep differs")
            current += 1  # oracle를 한 칸씩 진행하며 모형의 나머지 식을 복사하지 않습니다.
            if current == 256:
                current = 0
            sweep += 1

    gate = HealthGate(["a", "b"], 250, 10)
    gate.progress("a", 252)
    gate.progress("b", 252)
    fresh10 = gate.inspect(6)  # 252→6은 10 tick으로 허용 경계입니다.
    stale11 = gate.inspect(7)
    require(fresh10["healthy"] and not stale11["healthy"], "freshness boundary differs")
    gate.accept_epoch()
    unchanged = gate.inspect(6)
    require(not unchanged["healthy"], "old progress authorized a new epoch")
    gate.progress("a", 6)
    gate.progress("b", 6)
    renewed = gate.inspect(7)
    require(renewed["healthy"], "new task progress was not accepted")

    latch = ResetLatch()
    latch.latch("power")
    latch.latch("watchdog")
    captured = latch.capture(clear_first=inject == "clear-before-capture")
    require(captured == expected["capture"], "reset causes were lost or collapsed")
    require(latch.capture() == {"raw": 0, "causes": []}, "flags not cleared after capture")
    boots = boot_sequence(fixture["boot_events"], always_restart=inject == "always-restart")
    check_boot(boots, expected)

    bad_latch = ResetLatch()
    bad_latch.latch("power")
    bad_latch.latch("watchdog")
    lost = bad_latch.capture(clear_first=True)
    negatives = {
        "periodic_masks_stalled_task": rejected(lambda: check_monitor(periodic, expected["gated"])),
        "raw_wrapped_deadline": rejected(lambda: check_monitor(monitor(fixture["monitor"], raw_deadline=True), expected["gated"])),
        "clear_before_capture": rejected(lambda: require(lost == expected["capture"], "reset evidence erased")),
        "always_restart_bootloop": rejected(lambda: check_boot(boot_sequence(fixture["boot_events"], always_restart=True), expected)),
        "accept_old_epoch": rejected(lambda: require(unchanged["healthy"], "unchanged epoch is unhealthy")),
        "accept_stale_checkpoint": rejected(lambda: require(stale11["healthy"], "stale checkpoint is unhealthy")),
    }
    invalid = {
        "boolean_tick": rejected(lambda: elapsed(True, 0), ValueError),
        "half_range": rejected(lambda: elapsed(128, 0), ValueError),
        "negative_tick": rejected(lambda: elapsed(-1, 0), ValueError),
        "empty_tasks": rejected(lambda: HealthGate([], 0, 10), ValueError),
        "duplicate_tasks": rejected(lambda: HealthGate(["a", "a"], 0, 10), ValueError),
        "unknown_task": rejected(lambda: gate.progress("missing", 0), ValueError),
        "invalid_window": rejected(lambda: window_action(0, 0, True, 4, 4), ValueError),
    }
    return {"gated": main, "periodic": periodic, "literal_windows": windows, "tick_window_sweep": sweep,
            "health_boundaries": {"fresh10": fresh10, "stale11": stale11, "unchanged": unchanged, "renewed": renewed},
            "captured": captured, "boots": boots, "negative_controls": negatives, "invalid_inputs": invalid}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--inject", choices=("periodic-feed", "raw-deadline", "clear-before-capture", "always-restart"))
    args = parser.parse_args()
    output = args.output.resolve()
    try:
        output.mkdir(parents=True, exist_ok=False)  # 기존 결과를 덮어쓰지 않습니다.
    except FileExistsError:
        parser.error(f"output already exists: {output}")
    base = Path(__file__).resolve().parent
    hashes = {name: hashlib.sha256((base / name).read_bytes()).hexdigest()
              for name in ("models.py", "verify.py", "fixtures.json")}
    report = {"scope": "deterministic host model; no hardware watchdog, MCU reset, RTOS or retention execution",
              "utc": datetime.now(timezone.utc).isoformat(), "python": sys.version, "executable": sys.executable,
              "platform": platform.platform(), "optimize": sys.flags.optimize, "arguments": sys.argv,
              "source_and_input_sha256": hashes, "injection": args.inject}
    try:
        fixture = json.loads((base / "fixtures.json").read_text(encoding="utf-8"))
        report["checks"] = run_checks(fixture, args.inject)
        report["status"] = "passed"
    except Exception as error:
        report["status"] = "failed"
        report["error"] = f"{type(error).__name__}: {error}"
    (output / "results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "output": str(output)}, ensure_ascii=False))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
