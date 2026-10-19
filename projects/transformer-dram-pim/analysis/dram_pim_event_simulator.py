#!/usr/bin/env python3
"""유한 FIFO·공유 버스·all-bank refresh를 갖는 독립 DRAM 이벤트 모델.

기존 dram_pim_model.py/CSV의 결과를 변경하지 않는다. 이 파일은 READ/WRITE 요청의
메모리 서비스만 계산한다. Transformer 계산·의존성·PHY·실물 PIM/DDR2 측정이 아니다.
모든 timing은 연구자가 공개한 정수 cycle 가정이며 특정 Micron 부품 사양이 아니다.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import heapq
import json
from collections import Counter, deque
from dataclasses import asdict, dataclass
from itertools import islice
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class TimingConfig:
    """한 command/data bus, 여러 bank, 정해진 burst 길이를 갖는 공개 모델 설정."""
    banks: int = 8
    queue_depth: int = 16
    burst_bytes: int = 64
    t_cmd: int = 1            # 모든 command의 공유 bus 최소 간격
    t_rcd: int = 14          # ACT→해당 bank의 RD/WR
    t_rp: int = 14           # PRE→ACT/REF
    t_ras: int = 28          # ACT→PRE
    t_rc: int = 42           # 같은 bank의 ACT→ACT
    t_ccd: int = 4           # 모든 bank에 걸친 RD/WR→RD/WR 간격
    t_rrd: int = 2           # 서로 다른 bank를 포함한 모든 ACT 사이 최소 간격
    t_faw: int = 8           # rolling 네 ACT 뒤 다섯 번째 ACT까지의 창
    read_latency: int = 14   # RD issue→data start
    write_latency: int = 8   # WR issue→data start
    burst_cycles: int = 4    # data bus의 [start,end) 점유 길이
    t_rtp: int = 4           # RD issue→PRE
    t_wr: int = 6            # write data end→PRE
    t_rtw: int = 4           # read data end→write data start
    t_wtr: int = 6           # write data end→read data start
    refresh_enabled: bool = True
    t_refi: int = 512        # 512,1024,...의 고정 refresh 예정 시각
    t_rfc: int = 70          # REF issue→다음 어떤 command든 가능한 시각
    max_cycles: int = 1_000_000_000
    max_events: int = 2_000_000
    max_requests: int = 100_000

    def refresh_progress_bound(self) -> int:
        """계속 refresh만 하는 구성을 사전에 거부하는 보수적 충분 여유.

        실제 JEDEC의 최소 tREFI가 아니다. 마지막 data/recovery·bank PRE·REF와
        최악 head 준비 여유를 합해 유용한 RD/WR을 발행할 공간을 보수적으로 확보한다.
        물리적으로 가능한 일부 촘촘한 설정도 이 교육 모델에서는 거부할 수 있다.
        """
        drain = max(self.t_ras, max(self.read_latency, self.write_latency)
                    + self.burst_cycles + max(self.t_rtp, self.t_wr))
        head = max(self.t_rc, self.t_rp + self.t_rcd) + max(self.t_ccd, self.t_cmd)
        return (self.t_rfc + self.banks * self.t_cmd + self.t_rp + drain + head
                + max(self.t_rtw, self.t_wtr) + max(self.t_rrd, self.t_faw))

    def validate(self) -> None:
        """bool을 숫자로 받지 않고 양수/폭/refresh 진행 여유를 실행 전에 확인한다."""
        values = asdict(self)
        for name, value in values.items():
            if name == "refresh_enabled":
                if type(value) is not bool: raise ValueError("refresh_enabled는 bool이어야 합니다.")
                continue
            if type(value) is not int: raise ValueError(f"{name}은 정수 cycle/개수여야 합니다.")
            minimum = 0 if name in {"t_rtp", "t_wr", "t_rtw", "t_wtr"} else 1
            if value < minimum: raise ValueError(f"{name}은 {minimum} 이상이어야 합니다.")
        if self.t_rc < self.t_ras + self.t_rp:
            raise ValueError("이 모델의 tRC는 tRAS+tRP 이상이어야 합니다.")
        if self.refresh_enabled and self.t_refi <= self.refresh_progress_bound():
            raise ValueError("연속 refresh 포화 거부: tREFI가 보수적 진행 여유보다 커야 합니다.")


@dataclass(frozen=True)
class MemoryRequest:
    """FIFO에 들어가는 burst 하나. arrival은 요청 준비 시각이고 enqueue와 다를 수 있다."""
    request_id: str
    arrival_cycle: int
    operation: str            # READ/WRITE. 명령 원시 이벤트에서는 RD/WR로 표기
    bank: int
    row: int
    byte_count: int = 64
    tensor: str = "synthetic"
    byte_offset: int = 0
    source_trace_cycle: int | None = None


@dataclass
class _Bank:
    """bank별 open-row/마지막 timing 경계. data 내용 자체는 저장하지 않는다."""
    open_row: int | None = None
    last_act: int | None = None
    pre_done: int = 0
    column_ready: int = 0
    last_read: int | None = None
    last_write_end: int | None = None
    data_end: int = 0


class SimulationLimitError(RuntimeError):
    """유한 종료 guard에 걸린 작업은 PASS나 무한 대기 대신 명시적 오류가 된다."""


def _validate_requests(requests: list[MemoryRequest], cfg: TimingConfig) -> None:
    if len(requests) > cfg.max_requests: raise ValueError("요청 개수 제한을 넘었습니다.")
    ids: set[str] = set()
    previous = -1
    for req in requests:
        if not isinstance(req, MemoryRequest): raise ValueError("MemoryRequest 목록이 필요합니다.")
        if not isinstance(req.request_id, str) or not req.request_id or req.request_id in ids:
            raise ValueError("request_id는 비어 있지 않은 고유 문자열이어야 합니다.")
        ids.add(req.request_id)
        for name in ("arrival_cycle", "bank", "row", "byte_count", "byte_offset"):
            if type(getattr(req, name)) is not int: raise ValueError(f"요청의 {name}은 정수여야 합니다.")
        if not (previous <= req.arrival_cycle <= cfg.max_cycles):
            raise ValueError("arrival은 비음수·비감소·max_cycles 이내여야 합니다.")
        if req.arrival_cycle < 0 or not 0 <= req.bank < cfg.banks or req.row < 0 or req.byte_offset < 0:
            raise ValueError("arrival/bank/row/offset 범위가 잘못됐습니다.")
        if req.operation not in {"READ", "WRITE"}: raise ValueError("READ 또는 WRITE 요청만 가능합니다.")
        if req.byte_count != cfg.burst_bytes: raise ValueError("한 요청은 설정한 고정 burst_bytes와 같아야 합니다.")
        if req.source_trace_cycle is not None and (type(req.source_trace_cycle) is not int or req.source_trace_cycle < 0):
            raise ValueError("원 trace 시각은 비음수 정수 또는 None입니다.")
        if not isinstance(req.tensor, str): raise ValueError("tensor 이름은 문자열이어야 합니다.")
        previous = req.arrival_cycle


def simulate(requests: Iterable[MemoryRequest], cfg: TimingConfig = TimingConfig()) -> dict:
    """FIFO 순서대로 column을 발행하고 독립 bank/data 대기를 이벤트로 건너뛴다.

    한 cycle의 순서는 data 완료→refresh due→최대1enqueue→최대1command이다.
    FIFO full이 그 cycle의 RD/WR로 풀려도 다음 cycle에만 새 요청을 수락한다.
    refresh pending이면 새 ACT/RD/WR을 중단하고 열린 bank를 닫은 뒤 REF한다.
    """
    cfg.validate()
    # max_requests+1개까지만 소비한다. 무한 generator도 목록화에서 무한히 기다리지 않는다.
    reqs = list(islice(requests, cfg.max_requests + 1))
    _validate_requests(reqs, cfg)
    banks = [_Bank() for _ in range(cfg.banks)]
    fifo: deque[int] = deque()
    inflight: list[tuple[int, int]] = []
    pending_refresh: deque[int] = deque()
    act_history: deque[int] = deque(maxlen=4)
    events: list[dict] = []
    ledger = [{"request_index": i, **asdict(req), "enqueue_cycle": None, "issue_cycle": None,
               "data_start_cycle": None, "data_end_cycle": None, "row_class": None,
               "producer_delay_cycles": None, "fifo_wait_cycles": None} for i, req in enumerate(reqs)]
    activated: set[int] = set()
    conflicted: set[int] = set()
    next_input = completed = now = producer_ready = 0
    command_ready = column_ready = last_data_end = 0
    last_direction: str | None = None
    refresh_until = 0
    next_refresh = cfg.t_refi
    blocked_since: int | None = None
    max_queue = bp_cycles = refresh_count = 0
    refresh_lateness: list[int] = []

    def emit(cycle: int, event: str, **details) -> None:
        if len(events) >= cfg.max_events: raise SimulationLimitError("max_events에 도달했습니다.")
        events.append({"cycle": cycle, "event": event, **details})

    def pre_time(bank: _Bank) -> int:
        # PRE는 ACT 유지시간과 RD→PRE, WR data-end→PRE, 이미 예약한 burst 완료를 모두 기다린다.
        return max(command_ready, (bank.last_act or 0) + cfg.t_ras,
                   (bank.last_read + cfg.t_rtp) if bank.last_read is not None else 0,
                   (bank.last_write_end + cfg.t_wr) if bank.last_write_end is not None else 0,
                   bank.data_end)

    def column_time(req: MemoryRequest, bank: _Bank) -> int:
        latency = cfg.read_latency if req.operation == "READ" else cfg.write_latency
        gap = cfg.t_rtw if last_direction == "READ" and req.operation == "WRITE" else (
            cfg.t_wtr if last_direction == "WRITE" and req.operation == "READ" else 0)
        # data bus에 먼저 예약한 burst 다음에 도착하도록 column issue를 역산한다.
        # 이전 data-end에 gap을 더한 뒤 새 RL/WL을 뺀 것이 issue의 추가 하한이다.
        return max(command_ready, column_ready, bank.column_ready, last_data_end + gap - latency)

    def act_time(bank: _Bank) -> int:
        # tRC는 해당 bank만, tRRD/tFAW는 공유 ACT 전력/명령 제약을 뜻한다.
        # 최근 네 ACT를 보존하여 다섯 번째 ACT가 가장 오래된 ACT+tFAW보다 빠르지 않게 한다.
        return max(command_ready, bank.pre_done,
                   bank.last_act + cfg.t_rc if bank.last_act is not None else 0,
                   act_history[-1] + cfg.t_rrd if act_history else 0,
                   act_history[0] + cfg.t_faw if len(act_history) == 4 else 0)

    def issue_pre(bank_index: int, index: int | None, reason: str) -> None:
        nonlocal command_ready
        bank = banks[bank_index]
        emit(now, "COMMAND", command="PRE", bank=bank_index, row=bank.open_row,
             request_index=index, reason=reason)
        bank.open_row = None
        bank.pre_done = now + cfg.t_rp
        command_ready = now + cfg.t_cmd

    # 빈 입력은 refresh를 영원히 반복하지 않고 시각0의 빈 결과로 종료한다.
    while reqs:
        if now > cfg.max_cycles: raise SimulationLimitError("max_cycles를 넘었습니다.")
        while inflight and inflight[0][0] <= now:
            end, index = heapq.heappop(inflight)
            completed += 1
            emit(end, "DATA_END", request_index=index, request_id=reqs[index].request_id,
                 bank=reqs[index].bank, row=reqs[index].row, operation=reqs[index].operation,
                 byte_count=reqs[index].byte_count)
        if refresh_until and now >= refresh_until:
            emit(refresh_until, "REFRESH_END")
            refresh_until = 0
        # event jump가 due를 넘어가도 여기서 먼저 pending으로 만든다. 새 column을 먼저 발행하지 않는다.
        if cfg.refresh_enabled:
            while next_refresh <= now:
                pending_refresh.append(next_refresh)
                emit(next_refresh, "REFRESH_DUE", scheduled_cycle=next_refresh)
                next_refresh += cfg.t_refi
        if completed == len(reqs) and next_input == len(reqs) and not fifo and not pending_refresh and not refresh_until:
            break

        # producer는 매 cycle 하나까지 요청을 수락시킬 수 있다. FIFO에서 빠진 뒤 재수락을 명시적으로 지연한다.
        if next_input < len(reqs) and reqs[next_input].arrival_cycle <= now and producer_ready <= now:
            if len(fifo) < cfg.queue_depth:
                if blocked_since is not None:
                    emit(now, "BACKPRESSURE_END", request_index=next_input, blocked_since=blocked_since,
                         duration_cycles=now - blocked_since)
                    bp_cycles += now - blocked_since
                    blocked_since = None
                fifo.append(next_input)
                entry = ledger[next_input]
                entry["enqueue_cycle"] = now
                entry["producer_delay_cycles"] = now - reqs[next_input].arrival_cycle
                emit(now, "ENQUEUE", request_index=next_input, request_id=reqs[next_input].request_id,
                     bank=reqs[next_input].bank, row=reqs[next_input].row,
                     operation=reqs[next_input].operation, byte_count=reqs[next_input].byte_count,
                     queue_occupancy=len(fifo))
                max_queue = max(max_queue, len(fifo))
                next_input += 1
                producer_ready = now + 1
            elif blocked_since is None:
                blocked_since = now
                emit(now, "BACKPRESSURE_START", request_index=next_input, queue_occupancy=len(fifo))

        if not refresh_until:
            if pending_refresh:
                # all-bank REF 전에 열린 bank를 하나씩 PRE한다. 준비된 bank를 낮은 번호부터 닫는다.
                ready = [i for i, bank in enumerate(banks) if bank.open_row is not None and pre_time(bank) <= now]
                if ready:
                    issue_pre(ready[0], None, "refresh_drain")
                elif all(bank.open_row is None for bank in banks) and now >= max(
                        command_ready, last_data_end, *(bank.pre_done for bank in banks)):
                    due = pending_refresh.popleft()
                    emit(now, "COMMAND", command="REF", bank=None, row=None, request_index=None,
                         scheduled_cycle=due, lateness_cycles=now - due)
                    refresh_lateness.append(now - due)
                    refresh_count += 1
                    refresh_until = now + cfg.t_rfc
                    command_ready = now + cfg.t_cmd
            elif fifo:
                index = fifo[0]
                req, bank = reqs[index], banks[reqs[index].bank]
                if bank.open_row is None:
                    earliest = act_time(bank)
                    if now >= earliest:
                        bank.open_row, bank.last_act = req.row, now
                        bank.column_ready = now + cfg.t_rcd
                        act_history.append(now)
                        activated.add(index)
                        emit(now, "COMMAND", command="ACT", bank=req.bank, row=req.row, request_index=index)
                        command_ready = now + cfg.t_cmd
                elif bank.open_row != req.row:
                    if now >= pre_time(bank):
                        conflicted.add(index)
                        issue_pre(req.bank, index, "row_conflict")
                elif now >= column_time(req, bank):
                    latency = cfg.read_latency if req.operation == "READ" else cfg.write_latency
                    start, end = now + latency, now + latency + cfg.burst_cycles
                    bank.data_end = end
                    if req.operation == "READ": bank.last_read = now
                    else: bank.last_write_end = end
                    emit(now, "COMMAND", command="RD" if req.operation == "READ" else "WR",
                         bank=req.bank, row=req.row, request_index=index, request_id=req.request_id,
                         operation=req.operation, byte_count=req.byte_count,
                         data_start_cycle=start, data_end_cycle=end)
                    emit(start, "DATA_START", request_index=index, request_id=req.request_id,
                         bank=req.bank, row=req.row, operation=req.operation, byte_count=req.byte_count)
                    entry = ledger[index]
                    entry.update(issue_cycle=now, data_start_cycle=start, data_end_cycle=end,
                                 row_class="conflict" if index in conflicted else ("miss" if index in activated else "hit"),
                                 fifo_wait_cycles=now - entry["enqueue_cycle"])
                    heapq.heappush(inflight, (end, index))
                    fifo.popleft()
                    last_data_end, last_direction = end, req.operation
                    command_ready, column_ready = now + cfg.t_cmd, now + cfg.t_ccd

        # 한 번 반복한 뒤 다음 상태 변화가 가능한 시각으로 이동한다. 주기별 빈 loop를 돌리지 않는다.
        candidates: list[int] = []
        if inflight: candidates.append(inflight[0][0])
        if refresh_until: candidates.append(refresh_until)
        if cfg.refresh_enabled: candidates.append(next_refresh)
        # full 상태라도 아직 BACKPRESSURE_START를 찍지 않았다면 producer 도착 시각으로 이동한다.
        # 한 번 blocked를 기록한 뒤에는 FIFO가 비워질 때까지 같은 시각을 반복하지 않는다.
        if next_input < len(reqs) and (len(fifo) < cfg.queue_depth or blocked_since is None):
            candidates.append(max(reqs[next_input].arrival_cycle, producer_ready))
        if not refresh_until:
            if pending_refresh:
                opened = [bank for bank in banks if bank.open_row is not None]
                candidates.extend(pre_time(bank) for bank in opened)
                if not opened: candidates.append(max(command_ready, last_data_end, *(b.pre_done for b in banks)))
            elif fifo:
                req, bank = reqs[fifo[0]], banks[reqs[fifo[0]].bank]
                if bank.open_row is None:
                    candidates.append(act_time(bank))
                elif bank.open_row != req.row: candidates.append(pre_time(bank))
                else: candidates.append(column_time(req, bank))
        if not candidates: raise SimulationLimitError("다음 사건이 없는데 요청이 남아 있습니다.")
        # 같은 cycle에서 1command/1enqueue를 이미 처리했다. 다음 명령 경계는 최소 다음 cycle이다.
        now = min(max(now + 1, candidate) for candidate in candidates)

    ranks = {"DATA_END": 0, "REFRESH_END": 1, "REFRESH_DUE": 2, "BACKPRESSURE_END": 3,
             "ENQUEUE": 4, "BACKPRESSURE_START": 5, "COMMAND": 6, "DATA_START": 7}
    events.sort(key=lambda event: (event["cycle"], ranks[event["event"]]))
    commands = Counter(event["command"] for event in events if event["event"] == "COMMAND")
    result = {
        "mode": "trace_driven_memory_only_fifo_refresh_event_model", "configuration": asdict(cfg),
        "refresh_progress_bound_cycles": cfg.refresh_progress_bound(),
        "policy_ko": "한 cycle: 완료→due→최대1enqueue→최대1command. RD/WR FIFO순서 보존; due우선; PRE/data/recovery후REF; 예정은고정배수; 기존예약burst는완료한다.",
        "scope_ko": "연구자 timing 가정의 메모리 서비스만. 실제 DDR2/MIG/PHY·PIM·Transformer compute/의존성/학습/전력/실물 측정 제외.",
        "request_count": len(reqs), "completed_requests": completed, "bytes_transferred": sum(r.byte_count for r in reqs),
        "finish_cycle": now, "last_request_data_end_cycle": max((r["data_end_cycle"] for r in ledger), default=0),
        "row_hits": sum(r["row_class"] == "hit" for r in ledger),
        "row_misses": sum(r["row_class"] != "hit" for r in ledger),
        "row_conflicts": sum(r["row_class"] == "conflict" for r in ledger),
        "commands": dict(commands), "max_fifo_occupancy": max_queue,
        "fifo_backpressure_cycles": bp_cycles, "refresh_count": refresh_count,
        "max_refresh_lateness_cycles": max(refresh_lateness, default=0),
        "requests": ledger, "events": events,
        "physical_board_measured": False, "physical_dram_pim_measured": False,
        "new_transformer_computation_executed": False,
    }
    result["invariants"] = check_invariants(result)
    return result


def check_invariants(result: dict) -> dict:
    """출력 원시 사건을 재생해 FIFO 보존·bus·bank timing·refresh를 검사한다.

    DUT의 다음 사건 선택 코드를 호출하지 않는 별도 replay다. 손계산 회귀도 함께 써야
    같은 정의를 잘못 구현한 오류까지 줄일 수 있다. 실제 DDR compliance checker는 아니다.
    """
    cfg = TimingConfig(**result["configuration"])
    cfg.validate()
    requests, events = result["requests"], result["events"]
    accepted: list[int] = []; issued: list[int] = []; started: list[int] = []; ended: list[int] = []
    pending: deque[int] = deque(); fifo: deque[int] = deque(); refresh_ends: deque[int] = deque()
    act_history: deque[int] = deque(maxlen=4)
    activated: set[int] = set(); conflicted: set[int] = set()
    banks = [_Bank() for _ in range(cfg.banks)]
    last_command = last_column = last_enqueue = None
    data_end, direction, refresh_busy = 0, None, 0
    occupancy = inflight = peak = backpressure = refreshes = 0
    blocked: tuple[int, int] | None = None
    next_due = cfg.t_refi
    commands: Counter[str] = Counter()
    lateness: list[int] = []
    previous_cycle = -1
    previous_rank = -1
    ranks = {"DATA_END": 0, "REFRESH_END": 1, "REFRESH_DUE": 2, "BACKPRESSURE_END": 3,
             "ENQUEUE": 4, "BACKPRESSURE_START": 5, "COMMAND": 6, "DATA_START": 7}
    assertions = 0

    def require(condition: bool, message: str) -> None:
        nonlocal assertions
        assertions += 1
        if not condition: raise AssertionError(message)

    def request_link(event: dict) -> dict:
        """같은 row가 두 bank에 있어도 원 요청과 event의 실제 bank/ID/byte를 직접 묶는다."""
        index = event["request_index"]
        require(type(index) is int and 0 <= index < len(requests), "원장 index 범위 오류")
        req = requests[index]
        for key in ("request_id", "bank", "row", "operation", "byte_count"):
            require(event.get(key) == req[key], f"event/원장 {key} 연결 오류")
        return req

    for event in events:
        cycle, kind = event["cycle"], event["event"]
        require(type(cycle) is int and cycle >= previous_cycle, "이벤트 시각은 비감소 정수여야 합니다.")
        require(kind in ranks, "알 수 없는 사건 종류")
        require(cycle != previous_cycle or ranks[kind] >= previous_rank, "같은cycle 처리 순서 오류")
        previous_rank = ranks[kind]
        previous_cycle = cycle
        if kind == "REFRESH_DUE":
            require(cfg.refresh_enabled and cycle == event["scheduled_cycle"] == next_due, "REF due 고정달력/중복 오류")
            pending.append(cycle)
            next_due += cfg.t_refi
        elif kind == "REFRESH_END":
            require(bool(refresh_ends) and cycle == refresh_ends.popleft(), "REF 완료 시각/중복 오류")
        elif kind == "BACKPRESSURE_START":
            index = event["request_index"]
            require(blocked is None and index == len(accepted) and occupancy == cfg.queue_depth,
                    "FIFO full/단일producer backpressure 시작 오류")
            require(cycle >= requests[index]["arrival_cycle"] and (last_enqueue is None or cycle > last_enqueue),
                    "producer 준비전 backpressure")
            require(event["queue_occupancy"] == occupancy, "backpressure FIFO 계수 오류")
            blocked = (index, cycle)
        elif kind == "BACKPRESSURE_END":
            require(blocked is not None and blocked == (event["request_index"], event["blocked_since"]),
                    "backpressure 시작/종료 연결 오류")
            require(occupancy < cfg.queue_depth and event["duration_cycles"] == cycle - blocked[1],
                    "backpressure 종료/기간 오류")
            backpressure += event["duration_cycles"]
            blocked = None
        elif kind == "ENQUEUE":
            index = event["request_index"]
            req = request_link(event)
            require(index == len(accepted) and cycle == req["enqueue_cycle"], "수락순서/중복수락 오류")
            require(last_enqueue is None or cycle > last_enqueue, "같은cycle 두 요청 수락")
            require(cycle >= req["arrival_cycle"] and req["producer_delay_cycles"] == cycle - req["arrival_cycle"],
                    "준비전 요청 수락/producer 지연 계수 오류")
            accepted.append(index); fifo.append(index); occupancy += 1
            last_enqueue = cycle; peak = max(peak, occupancy)
            require(occupancy <= cfg.queue_depth and event["queue_occupancy"] == occupancy, "FIFO 용량 오류")
        elif kind == "DATA_START":
            index = event["request_index"]
            req = request_link(event)
            require(index == len(started) and index < len(issued) and cycle == req["data_start_cycle"],
                    "data start/issue 순서·중복·연결 오류")
            started.append(index)
        elif kind == "DATA_END":
            index = event["request_index"]
            req = request_link(event)
            require(index == len(ended) and index < len(started) and cycle == req["data_end_cycle"],
                    "data 완료순서/누락 오류")
            ended.append(index); inflight -= 1
        elif kind == "COMMAND":
            command = event["command"]
            require(command in {"ACT", "PRE", "RD", "WR", "REF"}, "지원하지 않는 명령")
            require(last_command is None or cycle >= last_command + cfg.t_cmd, "command bus 중첩")
            require(cycle >= refresh_busy, "tRFC 중 명령 발행")
            require(not pending or command in {"PRE", "REF"}, "refresh due보다 새 요청을 우선함")
            last_command = cycle
            commands[command] += 1
            if command == "REF":
                require(bool(pending) and event["scheduled_cycle"] == pending.popleft(), "REF 예정/발행 연결 오류")
                require(all(b.open_row is None and cycle >= b.pre_done for b in banks), "열린 bank/미완료 PRE 상태에서 REF")
                require(cycle >= data_end and inflight == 0, "burst 완료 전 REF")
                require(event["lateness_cycles"] == cycle - event["scheduled_cycle"], "REF 지연 계수 오류")
                refresh_busy = cycle + cfg.t_rfc
                refresh_ends.append(refresh_busy); refreshes += 1
                lateness.append(event["lateness_cycles"])
            else:
                require(type(event["bank"]) is int and 0 <= event["bank"] < cfg.banks, "명령 bank 범위 오류")
                bank = banks[event["bank"]]
                if command == "ACT":
                    index = event["request_index"]
                    require(bool(fifo) and index == fifo[0] and event["bank"] == requests[index]["bank"]
                            and event["row"] == requests[index]["row"], "ACT/FIFO head 연결 오류")
                    require(bank.open_row is None and cycle >= bank.pre_done, "PRE+tRP 미준수 ACT")
                    require(bank.last_act is None or cycle >= bank.last_act + cfg.t_rc, "같은 bank tRC 미준수")
                    require(not act_history or cycle >= act_history[-1] + cfg.t_rrd, "global tRRD 미준수")
                    require(len(act_history) < 4 or cycle >= act_history[0] + cfg.t_faw, "rolling4-ACT tFAW 미준수")
                    act_history.append(cycle); activated.add(index)
                    bank.open_row, bank.last_act, bank.column_ready = event["row"], cycle, cycle + cfg.t_rcd
                elif command == "PRE":
                    require(bank.open_row is not None and bank.open_row == event["row"], "닫힌/다른 row PRE")
                    require(cycle >= bank.last_act + cfg.t_ras and cycle >= bank.data_end, "tRAS/data-end 미준수 PRE")
                    require(bank.last_read is None or cycle >= bank.last_read + cfg.t_rtp, "tRTP 미준수 PRE")
                    require(bank.last_write_end is None or cycle >= bank.last_write_end + cfg.t_wr, "tWR 미준수 PRE")
                    if event["reason"] == "row_conflict":
                        index = event["request_index"]
                        require(not pending and bool(fifo) and index == fifo[0] and event["bank"] == requests[index]["bank"]
                                and bank.open_row != requests[index]["row"], "conflict PRE/head 연결 오류")
                        conflicted.add(index)
                    else:
                        require(event["reason"] == "refresh_drain" and bool(pending) and event["request_index"] is None,
                                "refresh PRE 이유/우선순위 오류")
                    bank.open_row, bank.pre_done = None, cycle + cfg.t_rp
                else:
                    index = event["request_index"]; req = request_link(event)
                    require(bool(fifo) and index == fifo.popleft() and index == len(issued), "FIFO column 순서 오류")
                    require(bank.open_row == req["row"] and cycle >= bank.column_ready, "row/tRCD 미준수 column")
                    require(command == ("RD" if req["operation"] == "READ" else "WR"), "요청/command 종류 오류")
                    require(cycle == req["issue_cycle"] and req["fifo_wait_cycles"] == cycle - req["enqueue_cycle"],
                            "issue 원장/FIFO 지연 계수 오류")
                    row_class = "conflict" if index in conflicted else ("miss" if index in activated else "hit")
                    require(req["row_class"] == row_class, "row hit/miss/conflict 계수 오류")
                    require(last_column is None or cycle >= last_column + cfg.t_ccd, "shared tCCD 미준수")
                    latency = cfg.read_latency if command == "RD" else cfg.write_latency
                    start, end = req["data_start_cycle"], req["data_end_cycle"]
                    require(event["data_start_cycle"] == start and event["data_end_cycle"] == end, "명령 data 원장 연결 오류")
                    require(start == cycle + latency and end == start + cfg.burst_cycles, "RL/WL/burst 길이 오류")
                    gap = cfg.t_rtw if direction == "READ" and command == "WR" else (
                        cfg.t_wtr if direction == "WRITE" and command == "RD" else 0)
                    require(start >= data_end + gap, "data bus 중첩/방향전환 미준수")
                    data_end, direction, last_column = end, req["operation"], cycle
                    bank.data_end = end
                    if command == "RD": bank.last_read = cycle
                    else: bank.last_write_end = end
                    issued.append(index); occupancy -= 1; inflight += 1
        require(len(accepted) == len(ended) + occupancy + inflight, "accepted=complete+FIFO+inflight 보존 실패")
        require(occupancy >= 0 and inflight >= 0, "음수 pending 개수")
    expected = list(range(len(requests)))
    require(accepted == issued == started == ended == expected and occupancy == inflight == 0, "요청 유실/중복/미완료")
    require(not pending and not refresh_ends and blocked is None, "종료시 refresh/backpressure 미완료")
    require(result["finish_cycle"] == max((e["cycle"] for e in events), default=0), "종료시각과 마지막 사건 불일치")
    require(not cfg.refresh_enabled or not requests or next_due > result["finish_cycle"], "due 이벤트 누락")
    require(result["request_count"] == result["completed_requests"] == len(requests), "완료 계수 오류")
    require(result["bytes_transferred"] == sum(r["byte_count"] for r in requests), "전송 byte 계수 오류")
    require(result["commands"] == dict(commands) and result["refresh_count"] == refreshes, "명령/refresh 요약 계수 오류")
    require(result["max_fifo_occupancy"] == peak and result["fifo_backpressure_cycles"] == backpressure, "FIFO 요약 오류")
    require(result["max_refresh_lateness_cycles"] == max(lateness, default=0), "refresh 최대지연 요약 오류")
    require(result["last_request_data_end_cycle"] == max((r["data_end_cycle"] for r in requests), default=0), "최종 data-end 요약 오류")
    require(result["row_hits"] == sum(r["row_class"] == "hit" for r in requests)
            and result["row_conflicts"] == len(conflicted)
            and result["row_misses"] == len(requests) - result["row_hits"], "row 요약 오류")
    return {"passed": True, "assertions": assertions, "request_order_preserved": True,
            "command_bus_nonoverlap": True, "data_bus_nonoverlap": True,
            "refresh_priority_and_timing": True, "fifo_conservation": True}


def load_legacy_csv(path: Path, cfg: TimingConfig = TimingConfig(), *, arrival_mode: str = "burst_stream",
                    arrival_gap: int = 0) -> tuple[dict[str, list[MemoryRequest]], dict]:
    """기존 2448행의 READ/WRITE만 독립 burst 요청으로 옮긴다.

    ACT/PRE와 원 service cycle은 재생 입력 명령으로 사용하지 않는다. bank/row와
    byte/tensor 순서를 보존하고 원 cycle은 참고 필드로 남긴다. burst_stream은 새
    도착 가정 index*gap, trace_cycles는 원 issue시각을도착으로 삼는별도조건이다.
    """
    cfg.validate()
    if arrival_mode not in {"burst_stream", "trace_cycles"}: raise ValueError("잘못된 arrival_mode입니다.")
    # 원 파일에는 byte_count 열이 없으며 기존 생성기의 한 READ/WRITE가 64byte이다.
    # 여기서 폭을 바꾸면 같은 원 trace의 byte 보존이 깨지므로 adapter에서는 명시적으로 거부한다.
    if cfg.burst_bytes != 64: raise ValueError("기존 trace adapter는 원래 64byte burst만 지원합니다.")
    if type(arrival_gap) is not int or arrival_gap < 0: raise ValueError("arrival_gap은 비음수 정수입니다.")
    groups: dict[str, list[MemoryRequest]] = {}
    source_rows = ignored = 0
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"cycle", "scenario", "command", "bank", "row", "tensor", "byte_offset"}
        if reader.fieldnames is None or set(reader.fieldnames) != required or len(reader.fieldnames) != len(required):
            raise ValueError("원 trace CSV 열이 올바르지 않습니다.")
        for line in reader:
            source_rows += 1
            if source_rows > cfg.max_requests * 4: raise ValueError("원 CSV 행 제한을 넘었습니다.")
            if None in line or any(value is None for value in line.values()): raise ValueError("CSV 열 누락/초과입니다.")
            cycle, bank, row, offset = (int(line[k]) for k in ("cycle", "bank", "row", "byte_offset"))
            if min(cycle, bank, row, offset) < 0 or bank >= cfg.banks: raise ValueError("원 CSV 범위 오류입니다.")
            if line["command"] not in {"ACT", "PRE", "READ", "WRITE"}: raise ValueError("원 CSV 명령 종류 오류입니다.")
            if not line["scenario"]: raise ValueError("scenario가 비어 있습니다.")
            if line["command"] not in {"READ", "WRITE"}:
                ignored += 1; continue
            bucket = groups.setdefault(line["scenario"], [])
            index = len(bucket)
            arrival = cycle if arrival_mode == "trace_cycles" else index * arrival_gap
            bucket.append(MemoryRequest(f"{line['scenario']}:{index}", arrival, line["command"], bank, row,
                                        cfg.burst_bytes, line["tensor"], offset, cycle))
    for requests in groups.values(): _validate_requests(requests, cfg)
    return groups, {"source_rows": source_rows, "ignored_original_ACT_PRE_rows": ignored,
                    "input_memory_requests": sum(map(len, groups.values())), "arrival_mode": arrival_mode,
                    "arrival_gap_cycles": arrival_gap,
                    "scenario_requests": {k: len(v) for k,v in groups.items()},
                    "scenario_bytes": {k: sum(r.byte_count for r in v) for k,v in groups.items()},
                    "source_csv_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "scope_ko": "원 issue cycle의 성능을 새 timing결과로대체하지 않는다. saturated/trace-cycle도착은새입력가정이며Transformer tensor의존성과compute는포함하지않는다."}


def write_outputs(result: dict, output_dir: Path, label: str) -> dict[str, str]:
    """JSON과 원시 event/request CSV를 저장한다. 기존 파일이 있으면 덮지 않고 거절한다."""
    if not label or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for c in label):
        raise ValueError("출력 label은 영문·숫자·_-만 사용하세요.")
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {kind: output_dir / f"{label}.{kind}" for kind in ("json", "events.csv", "requests.csv")}
    if any(path.exists() for path in paths.values()): raise FileExistsError("기존 결과를 덮어쓰지 않습니다.")
    paths["json"].write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with paths["events.csv"].open("w", encoding="utf-8", newline="") as handle:
        fields = ["cycle", "event", "command", "bank", "row", "request_index", "request_id", "details_json"]
        writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader()
        for event in result["events"]:
            simple = {key: event.get(key) for key in fields[:-1]}
            simple["details_json"] = json.dumps(event, ensure_ascii=False, sort_keys=True)
            writer.writerow(simple)
    with paths["requests.csv"].open("w", encoding="utf-8", newline="") as handle:
        fields = list(result["requests"][0]) if result["requests"] else ["request_index", "request_id", "arrival_cycle", "enqueue_cycle", "issue_cycle", "data_start_cycle", "data_end_cycle"]
        writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader(); writer.writerows(result["requests"])
    return {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths.values()}


def main() -> None:
    parser = argparse.ArgumentParser(description="독립 FIFO/refresh DRAM memory-only 이벤트 모델")
    parser.add_argument("--input-csv", type=Path, default=Path("fixtures/dram_pim_command_trace.csv"))
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--arrival-mode", choices=["burst_stream", "trace_cycles"], default="burst_stream")
    parser.add_argument("--arrival-gap", type=int, default=0)
    parser.add_argument("--no-refresh", action="store_true")
    for name, value in asdict(TimingConfig()).items():
        if name != "refresh_enabled": parser.add_argument("--" + name.replace("_", "-"), type=int, default=value)
    args = parser.parse_args()
    kwargs = {name: getattr(args, name) for name in asdict(TimingConfig()) if name != "refresh_enabled"}
    cfg = TimingConfig(**kwargs, refresh_enabled=not args.no_refresh)
    groups, adapter = load_legacy_csv(args.input_csv, cfg, arrival_mode=args.arrival_mode, arrival_gap=args.arrival_gap)
    # CLI는 폴더 자체도 새로 지정하게 하여 canonical을 실수로 덮지 못하게 한다.
    args.output_dir.mkdir(parents=True, exist_ok=False)
    summaries = {}
    for label, requests in groups.items():
        result = simulate(requests, cfg)
        paths = write_outputs(result, args.output_dir, label)
        summaries[label] = {key: value for key,value in result.items() if key not in {"requests", "events"}}
        summaries[label]["output_sha256"] = paths
    report = {"passed": all(x["invariants"]["passed"] for x in summaries.values()), "adapter": adapter,
              "configuration": asdict(cfg), "scenarios": summaries, "physical_board_measured": False,
              "scope_ko": "독립 memory-only 가정의 실제Python 실행. 기존DRAM/PIM69.64%나Transformer시뮬레이션결과를수정하지않음."}
    (args.output_dir / "result.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "requests": adapter["input_memory_requests"],
                      "scenarios": {label: result["finish_cycle"] for label,result in summaries.items()},
                      "output_dir": str(args.output_dir)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
