"""독립 기대값과 RTOS 사건 모델을 비교하고 새 출력 폴더에 JSON을 남깁니다."""
import argparse  # 명령행 옵션을 해석하는 표준 모듈입니다.
from datetime import datetime, timezone  # 시간대가 명시된 실행 시각을 기록합니다.
import hashlib  # 소스의 SHA-256 지문을 계산합니다.
from itertools import permutations  # 사건 배치의 모든 순열을 만듭니다.
import json  # dict와 list를 JSON 파일로 저장합니다.
from pathlib import Path  # 운영체제 경로를 객체로 다룹니다.
import platform  # 실제 실행 환경을 기록합니다.
import sys  # Python 버전과 종료 코드를 다룹니다.

from models import coalesced_batch, priority_schedule, wakeup_schedule


class ContractError(ValueError):
    """관측값이 독립 기대값과 다를 때 발생하는 예외입니다."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)  # Python -O에서도 제거되지 않는 검사입니다.


def priority_oracle(low: int, medium: int, high: int, inherit: bool) -> tuple[str, int]:
    """시간별 상태 전이와 독립적으로, 작업 블록을 연결해 기대값을 구성합니다."""
    if low == 1:
        return "L" + "H" * high + "M" * medium, 1 + high
    if inherit:
        return "L" * low + "H" * high + "M" * medium, low + high
    return "L" + "M" * medium + "L" * (low - 1) + "H" * high, low + medium + high


def check_priority(observed: dict, low: int, medium: int, high: int, inherit: bool,
                   expected_deadline: int = 5) -> None:
    expected_trace, expected_finish = priority_oracle(low, medium, high, inherit)
    require(observed["trace"] == expected_trace, f"priority trace: {observed['trace']} != {expected_trace}")
    require(observed["high_finished"] == expected_finish, "priority completion mismatch")
    require(observed["high_response"] == expected_finish - 1, "release/response mismatch")
    require(observed["deadline"] == expected_deadline, "requested deadline was changed")
    require(observed["deadline_met"] == (expected_finish <= expected_deadline), "deadline mismatch")


def check_wakeup(observed: dict) -> None:
    require(observed["consumed"] == [42], f"payload not consumed: {observed['consumed']}")
    require(not observed["remaining"] and not observed["lost_wakeup"], "pending payload is asleep")


def rejected(callable_check) -> dict:
    try:
        callable_check()
    except ContractError as error:
        return {"detected": True, "reason": str(error)}
    raise ContractError("negative control was not detected")


def run_checks(inject: str | None) -> dict:
    count, boundaries = 0, 0
    for low in range(1, 6):
        for medium in range(9):
            for high in range(1, 4):
                for inherit in (False, True):
                    actual_inherit = False if inject == "priority-no-inherit" else inherit
                    observed = priority_schedule(low, medium, high, actual_inherit)
                    check_priority(observed, low, medium, high, inherit)
                    expected_finish = priority_oracle(low, medium, high, inherit)[1]
                    for deadline in (expected_finish - 1, expected_finish):
                        edge = priority_schedule(low, medium, high, actual_inherit, deadline)
                        check_priority(edge, low, medium, high, inherit, deadline)
                        boundaries += 1
                    count += 1
    orders = ["".join(parts) for parts in permutations("CWP")
              if parts.index("C") < parts.index("W")]
    require(set(orders) == {"PCW", "CPW", "CWP"}, "event enumeration mismatch")
    faulty, corrected = [], []
    for order in orders:
        wrong = wakeup_schedule(order, retained=False)
        expected_loss = order.index("C") < order.index("P") < order.index("W")
        require(wrong["lost_wakeup"] == expected_loss, "resume-only ordering oracle mismatch")
        right = wakeup_schedule(order, retained=True, clear_before_wait=inject == "notify-clear")
        check_wakeup(right)
        faulty.append(wrong)
        corrected.append(right)
    batch_bad, batch_good = coalesced_batch(False), coalesced_batch(True)
    require(batch_bad["would_block_with_work"], "batch fault not reproduced")
    require(batch_good["consumed"] == [42, 43] and not batch_good["remaining"], "batch drain mismatch")
    changed_deadline = priority_schedule(3, 8, 1, False)
    changed_deadline["deadline"], changed_deadline["deadline_met"] = 100, True
    negatives = {
        "inheritance_removed": rejected(lambda: check_priority(priority_schedule(3, 8, 1, False), 3, 8, 1, True)),
        "pending_cleared_before_wait": rejected(lambda: check_wakeup(wakeup_schedule("CPW", True, True))),
        "one_item_after_clear": rejected(lambda: require(not batch_bad["would_block_with_work"], "payload left after notification cleared")),
        "deadline_and_verdict_changed": rejected(lambda: check_priority(changed_deadline, 3, 8, 1, False, 5)),
    }
    return {"priority_sweep_cases": count, "deadline_boundary_checks": boundaries,
            "priority_default": {"without": priority_schedule(3, 8, 1, False),
                                 "with": priority_schedule(3, 8, 1, True)},
            "wakeup": {"faulty": faulty, "corrected": corrected,
                       "batch_faulty": batch_bad, "batch_corrected": batch_good},
            "negative_controls": negatives}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--inject", choices=("priority-no-inherit", "notify-clear"))
    args = parser.parse_args()
    folder = args.output.resolve()
    folder.mkdir(parents=True, exist_ok=False)  # 기존 기록을 덮어쓰지 않습니다.
    sources = {name: hashlib.sha256((Path(__file__).parent / name).read_bytes()).hexdigest()
               for name in ("models.py", "verify.py")}
    report = {"scope": "deterministic Python host model; no FreeRTOS kernel/MCU/ISR execution",
              "utc": datetime.now(timezone.utc).isoformat(), "python": sys.version,
              "platform": platform.platform(), "executable": sys.executable, "arguments": sys.argv,
              "source_sha256": sources, "injection": args.inject}
    try:
        report["checks"] = run_checks(args.inject)
        report["status"] = "passed"
    except Exception as error:
        report["status"] = "failed"
        report["error"] = f"{type(error).__name__}: {error}"
    (folder / "results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "output": str(folder)}, ensure_ascii=False))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
