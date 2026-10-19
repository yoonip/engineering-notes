# 공개한 추상 DRAM/PIM의 요청/bytes/주소/shape/cache 용량 산술 회귀시험이다.
# 재현 가능한 모델 수치는 실제 DRAM 제품/FPGA board 측정 증거와 구분한다.
"""DRAM/PIM trace 모델의 산술과 경계 조건을 확인하는 회귀 시험."""

from __future__ import annotations

import unittest

from analysis.dram_pim_model import (
    Config,
    DramBankTrace,
    TensorAddresses,
    build_workload,
    kv_cache_capacity,
    simulate_pim_compute,
)


# DRAM 회귀시험용 두 시나리오 계산 도우미. 통계뿐 아니라 원본 Event도 반환한다.
def simulate(config: Config) -> dict[str, object]:
    config.validate()
    address_map = TensorAddresses(config)
    baseline_requests, pim_requests, jobs = build_workload(config, address_map)
    baseline = DramBankTrace(config, "baseline")
    pim = DramBankTrace(config, "pim")
    baseline.service(baseline_requests)
    pim.service(pim_requests)
    # baseline READ/WRITE 수*burst bytes. 실측이 아닌 모델 경계 이동량.
    baseline_bytes = (baseline.read_commands + baseline.write_commands) * config.burst_bytes
    # PIM 최초 적재/최종 출력의 요청 수*burst bytes. 내부 이동은 경계 밖으로 세지 않는다.
    pim_bytes = (pim.read_commands + pim.write_commands) * config.burst_bytes
    return {
        "baseline": baseline.result(baseline_bytes),
        "pim": pim.result(pim_bytes),
        "compute": simulate_pim_compute(config, jobs),
        "jobs": jobs,
        "baseline_events": baseline.events,
        "pim_events": pim.events,
    }


# logical 요청/bytes/주소와 cache 용량 산술 assert 모음.
class DramPimModelTests(unittest.TestCase):
    # 기본 모델 요청/bytes/MAC/PU의 재현 산술 정답 검사.
    # assert 실패는 이 경계/규칙이 기대값과 달라졌다는 뜻이다. PASS 표시만으로 숫자 검사를 대체하지 않는다.
    def test_default_research_case_is_reproducible(self) -> None:
        result = simulate(Config())
        baseline = result["baseline"]
        pim = result["pim"]
        compute = result["compute"]
        # 2026-10-04 수정: baseline의 weight 최초 READ와 VMM READ가 중복되어
        # 32768byte를 더 세던 오류를 제거했다. 각 matrix의 외부 READ는 1회다.
        self.assertEqual(baseline["bytes_crossing_host_memory_boundary"], 114688)
        self.assertEqual(pim["bytes_crossing_host_memory_boundary"], 34816)
        self.assertEqual(
            baseline["bytes_crossing_host_memory_boundary"]
            - pim["bytes_crossing_host_memory_boundary"],
            79872,
        )
        self.assertEqual(baseline["read_commands"], 1216)
        self.assertEqual(baseline["write_commands"], 576)
        self.assertEqual(pim["write_commands"], 528)
        self.assertEqual(compute["vmm_multiply_accumulates"], 294912)
        self.assertEqual(compute["nonvmm_vectors"], 288)
        self.assertGreater(baseline["estimated_memory_service_cycles"], 0)
        self.assertGreater(pim["estimated_memory_service_cycles"], 0)

    # 합계 값만 검사하면 activation/weight의 서로 다른 오류가 상쇄될 수 있다.
    # matrix별 burst offset/READ 또는 WRITE 종류/개수를 직접 검사하여 같은
    # weight가 baseline에서 사전 적재와 VMM으로 두 번 읽히는 회귀를 잡는다.
    # 정렬된 기본 shape뿐 아니라 72byte/60byte 행렬의 부분 burst도 포함한다.
    def test_each_weight_has_one_baseline_read_and_one_pim_initial_load(self) -> None:
        for config in (
            Config(),
            Config(tokens=3, d_model=6, heads=3, d_ff=5, layers=1,
                   banks=4, row_bytes=256, burst_bytes=64),
        ):
            with self.subTest(d_model=config.d_model, layers=config.layers):
                config.validate()
                addresses = TensorAddresses(config)
                baseline, pim, _ = build_workload(config, addresses)
                for layer in range(config.layers):
                    for name, elements in (
                        ("wq", config.d_model*config.d_model),
                        ("wk", config.d_model*config.d_model),
                        ("wv", config.d_model*config.d_model),
                        ("wo", config.d_model*config.d_model),
                        ("w1", config.d_model*config.d_ff),
                        ("w2", config.d_ff*config.d_model),
                    ):
                        tensor_name = f"L{layer}_{name}"
                        byte_count = elements*config.bytes_per_element
                        expected_offsets = list(range(0, byte_count, config.burst_bytes))
                        baseline_weight = [request for request in baseline
                                           if request.tensor == tensor_name]
                        pim_weight = [request for request in pim
                                      if request.tensor == tensor_name]
                        self.assertEqual([request.operation for request in baseline_weight],
                                         ["READ"]*len(expected_offsets), tensor_name)
                        self.assertEqual([request.operation for request in pim_weight],
                                         ["WRITE"]*len(expected_offsets), tensor_name)
                        self.assertEqual([request.offset for request in baseline_weight],
                                         expected_offsets, tensor_name)
                        self.assertEqual([request.offset for request in pim_weight],
                                         expected_offsets, tensor_name)
                        # 두 시나리오가 같은 논리 weight 주소를 사용해야 비교가
                        # input/주소 차이가 아닌 resident 실행 가정 차이에서 나온다.
                        self.assertEqual([request.address for request in baseline_weight],
                                         [request.address for request in pim_weight], tensor_name)

    # 다른 shape의 유효 bank/양의 cycle/연산량 검사.
    # assert 실패는 이 경계/규칙이 기대값과 달라졌다는 뜻이다. PASS 표시만으로 숫자 검사를 대체하지 않는다.
    def test_smaller_configuration_keeps_valid_command_trace(self) -> None:
        config = Config(
            tokens=4, d_model=8, heads=2, d_ff=16, layers=1,
            banks=4, row_bytes=256, burst_bytes=64,
            pim_mac_lanes_per_bank=4,
        )
        result = simulate(config)
        for scenario in ("baseline_events", "pim_events"):
            events = result[scenario]
            self.assertTrue(events)
            self.assertTrue(all(0 <= event.bank < config.banks for event in events))
            self.assertTrue(all(event.cycle >= 0 for event in events))
        self.assertGreater(
            result["baseline"]["bytes_crossing_host_memory_boundary"],
            result["pim"]["bytes_crossing_host_memory_boundary"],
        )
        self.assertEqual(result["compute"]["vmm_multiply_accumulates"],
                         3*4*8*8 + 2*4*4*4 + 2*4*4*4 + 4*8*8 + 4*8*16 + 4*16*8)

    # head 나눗셈/row-burst 정렬 오류를 trace 전에 거절하는지 검사.
    # assert 실패는 이 경계/규칙이 기대값과 달라졌다는 뜻이다. PASS 표시만으로 숫자 검사를 대체하지 않는다.
    def test_invalid_dimensions_fail_before_building_trace(self) -> None:
        with self.assertRaisesRegex(ValueError, "나누어져야"):
            Config(d_model=10, heads=4).validate()
        with self.assertRaisesRegex(ValueError, "배수"):
            Config(row_bytes=1000, burst_bytes=64).validate()

    # 모든 layer의 K/V 2*L*T*D*2byte 산술 검사.
    # assert 실패는 이 경계/규칙이 기대값과 달라졌다는 뜻이다. PASS 표시만으로 숫자 검사를 대체하지 않는다.
    def test_kv_cache_storage_accounts_for_each_layer_key_and_value(self) -> None:
        capacity = kv_cache_capacity(Config())
        self.assertEqual(capacity["key_and_value_elements"], 2 * 2 * 16 * 32)
        self.assertEqual(capacity["total_bytes"], 4096)
        self.assertEqual(capacity["bytes_per_added_token"], 256)


# 직접 실행할 때만 진입점을 실행한다. import한 다른 파일은 여기 함수/정의를 호출해 사용한다.
if __name__ == "__main__":
    unittest.main(verbosity=2)
