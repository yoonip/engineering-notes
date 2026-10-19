#!/usr/bin/env python3
# Transformer 데이터 이동과 추상 DRAM bank 명령/지연을 계산하는 software 모델이다.
# 미융합 baseline은 중간값을 host-memory 경계로 읽고 쓰며 PIM은 중간값이 메모리 가까이 남는 가정이다.
# PIM은 초기 weight/입력 적재 및 최종 출력만 경계를 넘는다. bytes/cycle은 이 정의의 결과다.
# Nexys DDR2 실측/실제 PIM silicon 결과가 아니다. burst 올림 때문에 tensor bytes와 이동 bytes가 다를 수 있다.
"""Transformer decoder의 off-chip DRAM 이동과 bank timing을 재현하는 모델.

실제 PIM 칩의 실측이 아니라, 공개된 parameter로 동일한 workload trace를 구성해
비-PIM unfused 기준과 PIM data-resident 가정을 비교한다. HBM/DDR 제품을 정확히
재현하려는 시뮬레이터가 아니며 refresh, command queue, PHY, 전력/온도, GPU cache,
다중 채널 스케줄링은 빠져 있다. 보고서에 가정과 제외 항목을 JSON으로 함께 쓴다.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


# DRAM/PIM 공개 가정 모음. frozen dataclass로 실행 중 configuration 변경을 막는다.
@dataclass(frozen=True)
class Config:
    # context T. 한 head의 attention 점수는 T*T개다.
    tokens: int = 16
    # 토큰 hidden D. embedding/residual/cache 채널 폭이다.
    d_model: int = 32
    # head H. head_dim=D/H의 독립 점수 관점을 만든다.
    heads: int = 4
    # FFN 확장 F. W1/W2 weight/연산 크기에 반영한다.
    d_ff: int = 64
    # decoder L. 층별 weight와 K/V를 갖는다.
    layers: int = 2
    # 저장 원소 bytes. signed Q8.8=16bit=2byte다.
    bytes_per_element: int = 2
    # bank 수 가정. 주소/compute dot을 순환 분산한다.
    banks: int = 8
    # bank row 길이. 같은 open row는 row hit다.
    row_bytes: int = 8192
    # data command 한 번 이동 bytes. 명령수*이 값으로 이동량을 계산한다.
    burst_bytes: int = 64
    # ACT->READ/WRITE 추상 대기 cycle 가정.
    t_rcd: int = 14
    # PRE->새 ACT 추상 대기 cycle 가정.
    t_rp: int = 14
    # data 명령 이후 데이터 도착/준비 추상 cycle 가정.
    t_cas: int = 14
    # data command 사이 공유 bus 간격 cycle 가정.
    t_ccd: int = 4
    # bank당 동시에 처리하는 MAC 항수 가정. board 실측은 아니다.
    pim_mac_lanes_per_bank: int = 16
    # lane 한 묶음의 가정 cycle.
    pim_cycles_per_mac_chunk: int = 1
    # Softmax 한 vector의 가정 latency. 원본 PU timing 실측이 아니다.
    pu_softmax_cycles_per_vector: int = 12
    # Norm 한 vector의 가정 latency.
    pu_layernorm_cycles_per_vector: int = 10

    # 양의 shape/head 나눗셈/row-burst 정렬을 검사해 잘못된 설정을 trace 생성 전에 거절한다.
    def validate(self) -> None:
        # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
        if min(self.tokens, self.d_model, self.heads, self.d_ff, self.layers, self.banks,
               self.row_bytes, self.burst_bytes, self.pim_mac_lanes_per_bank) <= 0:
            raise ValueError("차원과 bank/row/burst/parallelism 값은 양수여야 합니다.")
        # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
        if self.d_model % self.heads:
            raise ValueError("d_model은 heads로 나누어져야 합니다.")
        # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
        if self.row_bytes % self.burst_bytes:
            raise ValueError("row_bytes는 burst_bytes의 배수여야 합니다.")


# 한 burst의 logical 주소/READ 또는 WRITE/tensor/offset. 실제 DDR packet 규격은 아니다.
@dataclass(frozen=True)
class Request:
    # burst logical byte 주소. 실제 controller bit encoding이 아니다.
    address: int
    # READ/WRITE 요청 종류.
    operation: str
    # 명령의 tensor 이름. Transformer 중간값 이동을 trace에서 추적한다.
    tensor: str
    # tensor 시작부터 byte offset. word index와 다르다.
    offset: int


# command 발행 cycle/bank/row/tensor 기록. CSV trace 한 행의 근거다.
@dataclass
class Event:
    # 추상 명령 시각 cycle. ns 변환은 별도 clock 가정이 필요하다.
    cycle: int
    # baseline/PIM 분류. 같은 tensor 주소표를 공유한다.
    scenario: str
    # ACT/PRE/READ/WRITE 명령 종류.
    command: str
    # logical bank 번호 0..banks-1.
    bank: int
    # 해당 bank에서 열거나 접근하는 logical row 번호.
    row: int
    # 명령의 tensor 이름. Transformer 중간값 이동을 trace에서 추적한다.
    tensor: str
    # tensor 시작부터 byte offset. word index와 다르다.
    offset: int


# 두 시나리오가 같은 tensor를 같은 logical 주소에서 사용하게 관리한다.
class TensorAddresses:
    """같은 logical tensor를 baseline/PIM 시나리오에서 같은 주소에 매핑한다."""

    # 객체 초기 설정/저장 상태. 학습 model은 층/parameter를 등록하고 DRAM model은 logical 상태를 만든다.
    # 생성자 호출 자체가 inference/FPGA bitstream 생성은 아니다.
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.next_address = 0
        self.addresses: dict[str, tuple[int, int]] = {}

    # tensor를 burst 정렬 logical 주소에 한 번 배치한다. FPGA 실제 DDR 주소 예약이 아닌 모델 주소표다.
    def allocate(self, name: str, byte_count: int) -> None:
        if name in self.addresses:
            return
        alignment = self.cfg.burst_bytes
        base = (self.next_address + alignment - 1) // alignment * alignment
        self.addresses[name] = (base, byte_count)
        self.next_address = base + max(byte_count, alignment)

    # tensor byte 범위를 READ/WRITE burst 요청으로 쪼갠다. 마지막 부분도 전체 burst 한 명령으로 센다.
    def requests(self, tensor: str, operation: str) -> Iterable[Request]:
        base, size = self.addresses[tensor]
        burst = self.cfg.burst_bytes
        for offset in range(0, size, burst):
            yield Request(base + offset, operation, tensor, offset)


# open row/bank ready/command bus ready를 보존해 추상 서비스 지연을 계산한다.
class DramBankTrace:
    """Bank/row open-page 모델. burst 단위 요청을 단일 command bus에서 처리한다."""

    # 객체 초기 설정/저장 상태. 학습 model은 층/parameter를 등록하고 DRAM model은 logical 상태를 만든다.
    # 생성자 호출 자체가 inference/FPGA bitstream 생성은 아니다.
    def __init__(self, cfg: Config, scenario: str):
        self.cfg = cfg
        self.scenario = scenario
        self.open_rows: list[int | None] = [None] * cfg.banks
        self.bank_ready = [0] * cfg.banks
        self.bus_ready = 0
        self.events: list[Event] = []
        self.row_hits = 0
        self.row_misses = 0
        self.row_conflicts = 0
        self.read_commands = 0
        self.write_commands = 0

    # burst 번호를 순환 bank/row로 매핑한다. 실제 DDR PHY/controller address 규격이 아닌 공개 모델이다.
    def locate(self, address: int) -> tuple[int, int]:
        # model config의 shape/수치 규칙. config와 weight가 같아야 같은 모델이다.
        cfg = self.cfg
        burst_number = address // cfg.burst_bytes
        bursts_per_row = cfg.row_bytes // cfg.burst_bytes
        # logical bank 번호 0..banks-1.
        bank = burst_number % cfg.banks
        # 해당 bank에서 열거나 접근하는 logical row 번호.
        row = burst_number // (cfg.banks * bursts_per_row)
        return bank, row

    # cycle/command/bank/row/tensor/offset Event를 기록한다. CSV trace 한 행의 원본 증거다.
    def emit(self, cycle: int, command: str, bank: int, row: int, req: Request) -> None:
        self.events.append(Event(cycle, self.scenario, command, bank, row, req.tensor, req.offset))

    # 단일 command bus/open-page 모델 요청 처리. row hit면 접근, 충돌이면 PRE+tRP/ACT+tRCD를 기다린다.
    # refresh/reordering/실제 PHY는 포함하지 않는 추상 cycle 추정이다.
    def service(self, requests: Iterable[Request]) -> None:
        # model config의 shape/수치 규칙. config와 weight가 같아야 같은 모델이다.
        cfg = self.cfg
        # burst를 bank/row/open 상태에 따라 서비스한다. 현재 모델은 요청을 재정렬하지 않는다.
        for req in requests:
            bank, row = self.locate(req.address)
            now = max(self.bus_ready, self.bank_ready[bank])
            opened = self.open_rows[bank]
            if opened == row:
                self.row_hits += 1
                cmd_cycle = now
            else:
                self.row_misses += 1
                if opened is not None:
                    self.row_conflicts += 1
                    pre_cycle = now
                    self.emit(pre_cycle, "PRE", bank, opened, req)
                    now += cfg.t_rp
                self.emit(now, "ACT", bank, row, req)
                self.open_rows[bank] = row
                cmd_cycle = now + cfg.t_rcd

            self.emit(cmd_cycle, req.operation, bank, row, req)
            if req.operation == "READ":
                self.read_commands += 1
            else:
                self.write_commands += 1
            # tCAS은 burst read/write 뒤 데이터 도착에 반영하고, tCCD는 command bus
            # 간격으로 반영한다. 단일 채널 순차 trace여서 병렬 command reordering은 없다.
            self.bus_ready = cmd_cycle + cfg.t_ccd
            self.bank_ready[bank] = cmd_cycle + cfg.t_cas + cfg.t_ccd

    # byte/명령/hit/miss/conflict/service cycle 통계. 실제 DRAM bandwidth/전력 실측이 아니다.
    def result(self, total_bytes: int) -> dict[str, int | float]:
        last = max([self.bus_ready, *self.bank_ready], default=0)
        return {
            "bytes_crossing_host_memory_boundary": total_bytes,
            "read_commands": self.read_commands,
            "write_commands": self.write_commands,
            "activate_commands": sum(e.command == "ACT" for e in self.events),
            "precharge_commands": sum(e.command == "PRE" for e in self.events),
            "row_hits": self.row_hits,
            "row_misses": self.row_misses,
            "row_conflicts": self.row_conflicts,
            "estimated_memory_service_cycles": last,
        }


# 같은 tensor 주소로 baseline 경계 이동/PIM 외부 요청/연산 job을 만든다.
# 숫자 Q8.8 정답을 계산하지 않고 shape/크기/명령 순서만 모델링한다.
def build_workload(cfg: Config, address_map: TensorAddresses) -> tuple[list[Request], list[Request], list[dict[str, int | str]]]:
    """unfused baseline, data-resident PIM host-transfer trace, PIM compute jobs."""
    bpe = cfg.bytes_per_element
    t, d, h, hd, f, layers = cfg.tokens, cfg.d_model, cfg.heads, cfg.d_model // cfg.heads, cfg.d_ff, cfg.layers
    baseline: list[Request] = []
    pim_external: list[Request] = []
    compute_jobs: list[dict[str, int | str]] = []

    # 원소수*bytes_per_element의 logical tensor를 주소표에 등록하고 이름을 반환한다.
    def tensor(name: str, elements: int) -> str:
        address_map.allocate(name, elements * bpe)
        return name

    # tensor를 burst READ/WRITE로 쪼개 해당 시나리오 요청 목록에 추가한다.
    def transfer(target: list[Request], name: str, op: str) -> None:
        target.extend(address_map.requests(name, op))

    # 입력/가중치 주소는 실제 중복 할당 없이 모든 연산에서 재사용한다.
    current = tensor("input_hidden", t*d)
    all_weight_names: list[str] = []
    # head는 채널별 관점,layer는 직렬 block 반복. 올바른 slice/층 가중치를 선택해 처리한다.
    for layer in range(layers):
        for name, count in (("wq", d*d), ("wk", d*d), ("wv", d*d), ("wo", d*d),
                            ("w1", d*f), ("w2", f*d)):
            full_name = f"L{layer}_{name}"
            tensor(full_name, count)
            all_weight_names.append(full_name)
    for weight in all_weight_names:
        transfer(pim_external, weight, "WRITE")  # 가중치를 PIM bank에 최초 1회 적재
        # baseline의 weight READ는 아래 해당 VMM 실행에서 한 번 기록한다.
        # 여기서 미리 READ를 추가하면 같은 host-memory 경계/같은 주소를 두 번
        # 읽게 된다. 별도 cache/bus 계층을 모델링하지 않으므로 중복 계산하지 않는다.
    transfer(pim_external, current, "WRITE")      # 입력 hidden state를 PIM에 최초 적재

    # head는 채널별 관점,layer는 직렬 block 반복. 올바른 slice/층 가중치를 선택해 처리한다.
    for layer in range(layers):
        # activation/weight READ와 output WRITE를 baseline에 기록하고 [m,k,n] VMM 작업량을 추가한다.
        def vmm(name: str, a_name: str, weight_name: str, out_name: str,
                m: int, k: int, n: int) -> str:
            tensor(out_name, m*n)
            transfer(baseline, a_name, "READ")
            # 학습 가중치는 이 matrix의 전체 [m,k,n] 연산을 처리할 때 1회 읽는
            # 가정이다. 행 m마다 weight를 다시 읽는 모델이 아니며 초기 사전 READ도 없다.
            transfer(baseline, weight_name, "READ")
            transfer(baseline, out_name, "WRITE")
            compute_jobs.append({"kind": "VMM", "name": name, "m": m, "k": k, "n": n})
            return out_name

        # QK/PV처럼 두 activation이 피연산자인 내적의 읽기/쓰기와 MAC shape를 기록한다.
        def vmm_two_inputs(name: str, a_name: str, b_name: str, out_name: str,
                           m: int, k: int, n: int) -> str:
            """QK^T와 P×V처럼 두 활성 텐서가 피연산자인 행렬곱."""
            tensor(out_name, m*n)
            transfer(baseline, a_name, "READ")
            transfer(baseline, b_name, "READ")
            transfer(baseline, out_name, "WRITE")
            compute_jobs.append({"kind": "VMM", "name": name, "m": m, "k": k, "n": n})
            return out_name

        # non-VMM의 입력 READ/출력 WRITE와 vector 개수별 가정 지연 작업을 기록한다.
        def pu(name: str, input_names: list[str], out_name: str, out_elements: int,
               vectors: int, latency: int) -> str:
            tensor(out_name, out_elements)
            for source in input_names:
                transfer(baseline, source, "READ")
            transfer(baseline, out_name, "WRITE")
            compute_jobs.append({"kind": "PU", "name": name, "vectors": vectors, "latency": latency})
            return out_name

        # Query projection. 찾을 특징이며 K와의 내적으로 관련성을 계산한다.
        q = vmm(f"L{layer}_Q", current, f"L{layer}_wq", f"L{layer}_Q_out", t, d, d)
        # Key projection. 검색 대상 특징이며 여러 query와 비교할 수 있다.
        k = vmm(f"L{layer}_K", current, f"L{layer}_wk", f"L{layer}_K_out", t, d, d)
        # Value projection. attention 확률로 가중 합산할 내용이다.
        v = vmm(f"L{layer}_V", current, f"L{layer}_wv", f"L{layer}_V_out", t, d, d)
        # 모든 head의 QK^T를 batch 차원 H*T로 묶는다. 따라서 Q/K 전체 텐서를 head
        # 개수만큼 중복 off-chip read한다고 잘못 세지 않고, 실제 dot 수는 head 수를
        # 포함해 계산한다.
        scores = vmm_two_inputs(f"L{layer}_QK_all_heads", q, k,
                                f"L{layer}_scores", h*t, hd, t)
        # query별 key 축 비중. causal 미래 위치는0으로 제외한다.
        probabilities = pu(f"L{layer}_softmax_all_heads", [scores],
                           f"L{layer}_probabilities", h*t*t, h*t,
                           cfg.pu_softmax_cycles_per_vector)
        context = vmm_two_inputs(f"L{layer}_context_all_heads", probabilities, v,
                                 f"L{layer}_context_concat", h*t, t, hd)
        attn = vmm(f"L{layer}_Wo", context, f"L{layer}_wo", f"L{layer}_attn_out", t, d, d)
        # 입력+attention 포화 덧셈. attention 전 정보도 보존한다.
        residual1 = pu(f"L{layer}_residual1", [current, attn], f"L{layer}_res1", t*d,
                       t, 1)
        # 첫 residual Norm/선택 affine. FFN 입력/둘째 residual 기본 특징이다.
        norm1 = pu(f"L{layer}_layernorm1", [residual1], f"L{layer}_norm1", t*d,
                   t, cfg.pu_layernorm_cycles_per_vector)
        # FFN 확장/activation 특징. W1 선형 뒤 비선형 ReLU/GELU를 적용한다.
        ff1 = vmm(f"L{layer}_FFN1", norm1, f"L{layer}_w1", f"L{layer}_ff1", t, d, f)
        relu = pu(f"L{layer}_ReLU", [ff1], f"L{layer}_relu", t*f, t, 1)
        # FFN 축소 linear 결과. norm1과 residual로 더한다.
        ff2 = vmm(f"L{layer}_FFN2", relu, f"L{layer}_w2", f"L{layer}_ff2", t, f, d)
        # norm1+ff2 포화 덧셈. 뒤 Norm이 block 출력을 만든다.
        residual2 = pu(f"L{layer}_residual2", [norm1, ff2], f"L{layer}_res2", t*d,
                       t, 1)
        current = pu(f"L{layer}_layernorm2", [residual2], f"L{layer}_output", t*d,
                     t, cfg.pu_layernorm_cycles_per_vector)

    transfer(pim_external, current, "READ")
    return baseline, pim_external, compute_jobs


# bank별 lane/chunk 가정의 VMM/vector PU service cycle을 계산한다.
# m*k*n=MAC 항수,ceil(k/lanes)=dot chunk 수. 업체 PIM 실측 처리량이 아니다.
def simulate_pim_compute(cfg: Config, jobs: list[dict[str, int | str]]) -> dict[str, int]:
    """단순 bank-local throughput 모델: 각 bank가 같은 시간에 독립 실행한다."""
    per_bank = [0] * cfg.banks
    vmm_mac_ops = 0
    pu_vectors = 0
    command_count = 0
    job_cycles = 0
    # Transformer 의존 순서대로 VMM/PU job의 추상 bank 병렬 시간을 누적한다.
    for job in jobs:
        if job["kind"] == "VMM":
            m, k, n = int(job["m"]), int(job["k"]), int(job["n"])
            dots = m*n
            # ceil(내적 길이/bank lane) 묶음 수. 항수를 cycle로 바꾸는 공개 가정.
            chunks = math.ceil(k / cfg.pim_mac_lanes_per_bank)
            service = chunks * cfg.pim_cycles_per_mac_chunk
            for dot in range(dots):
                # logical bank 번호 0..banks-1.
                bank = dot % cfg.banks
                per_bank[bank] += service
            vmm_mac_ops += m*k*n
            command_count += dots
            job_cycles += max(per_bank, default=0)
            per_bank = [0] * cfg.banks
        else:
            vectors, latency = int(job["vectors"]), int(job["latency"])
            per_bank = [0] * cfg.banks
            for vector in range(vectors):
                per_bank[vector % cfg.banks] += latency
            pu_vectors += vectors
            command_count += vectors
            job_cycles += max(per_bank, default=0)
    return {
        "vmm_multiply_accumulates": vmm_mac_ops,
        "nonvmm_vectors": pu_vectors,
        "abstract_pim_commands": command_count,
        "estimated_bank_parallel_compute_cycles": job_cycles,
    }


# 논리 K/V bytes=2*L*T*D*bytes_per_element. 실제 BRAM macro port/배치 효율은 포함하지 않는다.
def kv_cache_capacity(cfg: Config) -> dict[str, int | str]:
    """Layer별 K/V cache를 Q8.8 element로 저장할 때 필요한 논리 용량."""
    cfg.validate()
    elements = 2 * cfg.layers * cfg.tokens * cfg.d_model
    return {
        "maximum_cached_tokens": cfg.tokens,
        "layers": cfg.layers,
        "channels_per_layer": cfg.d_model,
        "key_and_value_elements": elements,
        "bytes_per_element": cfg.bytes_per_element,
        "total_bytes": elements * cfg.bytes_per_element,
        "bytes_per_added_token": 2 * cfg.layers * cfg.d_model * cfg.bytes_per_element,
        "interpretation_ko": "각 layer의 Key와 Value를 저장하는 논리 용량 산술이다. 실제 memory macro 크기, port, 배치, FPGA BRAM 추론 또는 PIM 내부 용량을 증명하지 않는다.",
    }


# 두 trace/compute/cache 용량을 계산해 가정/제외항목과 함께 JSON/CSV를 저장한다.
# 감소율만 보고 실제 GPU/FPGA 속도 향상을 주장하면 안 된다.
def run(cfg: Config, output_dir: Path) -> dict[str, object]:
    cfg.validate()
    output_dir.mkdir(parents=True, exist_ok=True)
    addresses = TensorAddresses(cfg)
    baseline_requests, pim_requests, compute_jobs = build_workload(cfg, addresses)
    baseline = DramBankTrace(cfg, "unfused_baseline")
    pim = DramBankTrace(cfg, "pim_data_resident")
    baseline.service(baseline_requests)
    pim.service(pim_requests)

    # baseline READ/WRITE 수*burst bytes. 실측이 아닌 모델 경계 이동량.
    baseline_bytes = baseline.read_commands * cfg.burst_bytes + baseline.write_commands * cfg.burst_bytes
    # PIM 최초 적재/최종 출력의 요청 수*burst bytes. 내부 이동은 경계 밖으로 세지 않는다.
    pim_bytes = pim.read_commands * cfg.burst_bytes + pim.write_commands * cfg.burst_bytes
    compute = simulate_pim_compute(cfg, compute_jobs)
    # autoregressive decoding에서 layer별 K와 V를 재사용하려면 저장해야 하는
    # 최소 논리 용량이다. 여기서는 element를 Q8.8 16-bit로 보고 계산한다.
    # 이 값은 필요한 bit 수의 산술 추정이지, FPGA BRAM/DRAM primitive mapping은 아니다.
    result: dict[str, object] = {
        "model_name": "abstract_open_page_dram_and_dram_pim_command_model",
        "date_note": "기능·트래픽 모델이며 실제 DRAM/PIM 계측값이 아님",
        "configuration": asdict(cfg),
        "unfused_baseline": baseline.result(baseline_bytes),
        "pim_data_resident": pim.result(pim_bytes),
        "comparison": {
            "offchip_bytes_saved": baseline_bytes - pim_bytes,
            "offchip_byte_reduction_percent": round((baseline_bytes-pim_bytes)*100/baseline_bytes, 2) if baseline_bytes else 0.0,
            "interpretation": "가중치를 prompt 계산당 1회 읽고, PIM은 중간 activation이 bank 근처에 머문다고 가정한 모델 결과",
        },
        "pim_internal_compute_estimate": compute,
        "autoregressive_kv_cache_capacity": kv_cache_capacity(cfg),
        "memory_model_exclusions": [
            "refresh와 ECC", "DDR/HBM PHY·채널·rank·실제 command queue", "전력·열·공정·timing closure",
            "GPU cache와 fused kernel", "실제 PIM 명령 규격 및 bank 내부 데이터 경로",
            "PU/VMM 동시 실행 스케줄링과 bank conflict에 대한 업체별 구현 세부사항",
        ],
    }
    report_path = output_dir / "dram_pim_model.json"
    report_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    trace_path = output_dir / "dram_pim_command_trace.csv"
    with trace_path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["cycle", "scenario", "command", "bank", "row", "tensor", "byte_offset"])
        for event in sorted([*baseline.events, *pim.events], key=lambda e: (e.scenario, e.cycle, e.bank)):
            writer.writerow([event.cycle, event.scenario, event.command, event.bank, event.row, event.tensor, event.offset])

    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"\nJSON 보고서: {report_path}")
    print(f"DRAM 명령 trace: {trace_path}")
    return result


# model/memory 가정 shape와 output 경로를 command line에서 받는다. 실제 설정은 JSON에 남는다.
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    # generation에서는 새 token 수, DRAM 모델에서는 context token 수. 파일 목적에 따라 의미가 다르다.
    parser.add_argument("--tokens", type=int, default=16)
    # hidden 채널 D. 모든 head 폭의 합이며 embedding/residual 폭이다.
    parser.add_argument("--d-model", type=int, default=32)
    # attention 관점 H. D가 H로 나누어져야 channel slice를 분할할 수 있다.
    parser.add_argument("--heads", type=int, default=4)
    # FFN 확장 F. W1 D*F/W2 F*D의 저장 및 MAC 비용을 결정한다.
    parser.add_argument("--d-ff", type=int, default=64)
    # decoder 층 L. 앞층 결과를 다음층에 전달하고 층별 weight를 사용한다.
    parser.add_argument("--layers", type=int, default=2)
    # 추상 bank 개수. 실제 Nexys DDR/PIM 제품 동일 구성이라고 주장하는 값은 아니다.
    parser.add_argument("--banks", type=int, default=8)
    # 추상 row bytes. burst의 배수로 주소/지연 규칙을 정의한다.
    parser.add_argument("--row-bytes", type=int, default=8192)
    # 명령 한 번의 이동 bytes. 불완전 마지막 부분도 전체 burst 한 개로 센다.
    parser.add_argument("--burst-bytes", type=int, default=64)
    # bank별 병렬 MAC 항수 가정. chunk=ceil(k/lanes)이며 실측 lane 수가 아니다.
    parser.add_argument("--pim-lanes", type=int, default=16)
    # checkpoint/trace/JSON 생성 폴더. model parameter가 아닌 파일 경로다.
    parser.add_argument("--output-dir", type=Path, default=Path("build/reports"))
    return parser.parse_args()


# 직접 실행할 때만 진입점을 실행한다. import한 다른 파일은 여기 함수/정의를 호출해 사용한다.
if __name__ == "__main__":
    args = parse_args()
    config = Config(
        tokens=args.tokens, d_model=args.d_model, heads=args.heads,
        d_ff=args.d_ff, layers=args.layers, banks=args.banks,
        row_bytes=args.row_bytes, burst_bytes=args.burst_bytes,
        pim_mac_lanes_per_bank=args.pim_lanes,
    )
    run(config, args.output_dir)
