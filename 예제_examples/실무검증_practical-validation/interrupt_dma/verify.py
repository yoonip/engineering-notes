"""호스트 IRQ/DMA/캐시 모형의 독립 기대값과 오류 검출 결과를 새 폴더에 기록합니다."""
import argparse  # 명령행 인수를 해석합니다.
from datetime import datetime, timezone  # 시간대가 있는 실행 시각을 남깁니다.
import hashlib  # 입력과 소스의 지문을 계산합니다.
import json  # 사전·목록을 JSON으로 읽고 씁니다.
from pathlib import Path  # 파일 경로를 객체로 다룹니다.
import platform  # 실행 운영체제 정보를 확인합니다.
import sys  # Python 실행 환경과 종료 상태를 다룹니다.

from models import (buffer_reuse, covered_lines, dirty_rx_case, integer, neighbor_case,
                    rx_case, tx_case, w1c_after)


class ContractError(ValueError):
    """실제 관측이 요청한 계약과 다를 때 발생합니다."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)  # 일반 예외이므로 Python -O에서도 검사합니다.


def w1c_oracle(pending: int, handled: int) -> int:
    bits = {bit for bit in range(8) if pending & (1 << bit)}  # set은 중복 없는 집합입니다.
    removed = {bit for bit in range(8) if handled & (1 << bit)}
    return sum(1 << bit for bit in bits - removed)  # 집합 차이로 남아야 할 원인을 만듭니다.


def check_w1c(observed: dict, pending: int, handled: int) -> None:
    require(observed["pending_before"] == pending and observed["handled_mask"] == handled,
            "requested pending/mask was changed")
    require(observed["pending_after"] == w1c_oracle(pending, handled), "unhandled IRQ cause was cleared")
    require(observed["written"] == handled, "W1C write must contain only handled bits")


def check_owner(observed: dict, first: int, second: int) -> None:
    require(not observed["reuse_allowed"], "CPU-owned buffer was reused")
    require(observed["cpu_observed"] == first, "completed payload was overwritten")
    require(observed["outstanding_B"] == second, "other completed buffer changed")


def check_bytes(observed: dict, field: str, expected: bytes) -> None:
    require(observed[field] == expected.hex(), f"{field}: {observed[field]} != {expected.hex()}")


def rejected(check) -> dict:
    try:
        check()
    except ContractError as error:
        return {"detected": True, "reason": str(error)}
    raise ContractError("intentional fault escaped verification")


def run_checks(fixture: dict, inject: str | None) -> dict:
    require(fixture["line_bytes"] == 32 and fixture["memory_bytes"] == 128, "fixture geometry unsupported")
    irq = fixture["irq"]
    pending = integer(irq["pending"], 0, 255)
    handled = integer(irq["handled_mask"], 0, 255)
    w1c_count = 0
    for old in range(256):
        for mask in range(256):
            outcome = w1c_after(old, mask, rmw=inject == "w1c-rmw")
            check_w1c(outcome, old, mask)
            w1c_count += 1
    line_count = 0
    for start in range(129):
        for length in range(129 - start):
            expected = sorted({address // 32 * 32 for address in range(start, start + length)})
            require(covered_lines(start, length) == expected, "line range differs from bytewise oracle")
            line_count += 1
    owner = fixture["ownership"]
    for value in owner.values():
        integer(value, 0, 255)
    wrong_owner = buffer_reuse(owner["first"], owner["second"], owner["replacement"], False)
    right_owner = buffer_reuse(owner["first"], owner["second"], owner["replacement"],
                               respect_owner=inject != "allow-owned-reuse")
    check_owner(right_owner, owner["first"], owner["second"])
    tx = fixture["tx"]
    tx_data = bytes.fromhex(tx["payload_hex"])
    bad_tx = tx_case(tx["address"], tx_data, False)
    good_tx = tx_case(tx["address"], tx_data, clean_before=inject != "tx-no-clean")
    check_bytes(good_tx, "dma_hex", tx_data)
    rx = fixture["rx"]
    rx_data = bytes.fromhex(rx["payload_hex"])
    bad_rx, good_rx = rx_case(rx["address"], rx_data, False), rx_case(rx["address"], rx_data, True)
    check_bytes(good_rx, "cpu_hex", rx_data)
    bad_dirty = dirty_rx_case(rx["address"], rx_data, False)
    good_dirty = dirty_rx_case(rx["address"], rx_data, True)
    check_bytes(good_dirty, "ram_hex", rx_data)
    nearby = fixture["neighbor"]
    rx16 = bytes.fromhex(nearby["payload_hex"])
    require(len(rx16) == 16 and nearby["address"] == 0 and nearby["shared_flag_address"] == 16
            and nearby["isolated_flag_address"] == 32, "neighbor fixture layout unsupported")
    flag = integer(nearby["flag_value"], 1, 255)
    shared_drop = neighbor_case(rx16, nearby["shared_flag_address"], flag, False)
    shared_clean = neighbor_case(rx16, nearby["shared_flag_address"], flag, True)
    isolated = neighbor_case(rx16, nearby["isolated_flag_address"], flag, False)
    check_bytes(isolated, "cpu_hex", rx16)
    require(isolated["flag"] == flag, "isolated neighbor flag was lost")
    require(shared_drop["flag"] == 0, "shared-line flag loss was not reproduced")
    require(shared_clean["cpu_hex"] == bytes(16).hex(), "post-clean RX corruption was not reproduced")
    negatives = {
        "w1c_rmw": rejected(lambda: check_w1c(w1c_after(pending, handled, True), pending, handled)),
        "owned_buffer_reuse": rejected(lambda: check_owner(wrong_owner, owner["first"], owner["second"])),
        "tx_without_clean": rejected(lambda: check_bytes(bad_tx, "dma_hex", tx_data)),
        "rx_without_invalidate": rejected(lambda: check_bytes(bad_rx, "cpu_hex", rx_data)),
        "dirty_rx_without_prepare": rejected(lambda: check_bytes(bad_dirty, "ram_hex", rx_data)),
        "shared_line_invalidate": rejected(lambda: require(shared_drop["flag"] == flag, "shared neighbor lost")),
        "shared_line_post_clean": rejected(lambda: check_bytes(shared_clean, "cpu_hex", rx16)),
    }
    return {"w1c_combinations": w1c_count, "line_range_combinations": line_count,
            "irq": {"faulty": w1c_after(pending, handled, True), "corrected": w1c_after(pending, handled, False)},
            "ownership": {"faulty": wrong_owner, "corrected": right_owner},
            "tx": {"faulty": bad_tx, "corrected": good_tx}, "rx": {"faulty": bad_rx, "corrected": good_rx},
            "dirty_rx": {"faulty": bad_dirty, "corrected": good_dirty},
            "neighbor": {"shared_invalidate": shared_drop, "shared_clean_invalidate": shared_clean,
                         "isolated": isolated}, "negative_controls": negatives}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--inject", choices=("w1c-rmw", "tx-no-clean", "allow-owned-reuse"))
    args = parser.parse_args()
    folder = args.output.resolve()
    try:
        folder.mkdir(parents=True, exist_ok=False)  # 기존 결과를 덮어쓰지 않습니다.
    except FileExistsError:
        parser.error(f"output already exists: {folder}")
    base = Path(__file__).resolve().parent
    sources = {name: hashlib.sha256((base / name).read_bytes()).hexdigest()
               for name in ("models.py", "verify.py", "fixtures.json")}
    report = {"scope": "deterministic host model; no MCU, register, DMA or cache instruction execution",
              "utc": datetime.now(timezone.utc).isoformat(), "python": sys.version,
              "executable": sys.executable, "platform": platform.platform(), "arguments": sys.argv,
              "source_and_input_sha256": sources, "injection": args.inject}
    try:
        fixture = json.loads((base / "fixtures.json").read_text(encoding="utf-8"))
        report["checks"] = run_checks(fixture, args.inject)
        report["status"] = "passed"
    except Exception as error:
        report["status"] = "failed"
        report["error"] = f"{type(error).__name__}: {error}"
    (folder / "results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "output": str(folder)}, ensure_ascii=False))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
