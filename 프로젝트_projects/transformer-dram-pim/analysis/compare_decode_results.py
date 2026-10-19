#!/usr/bin/env python3
# 동일 prompt/생성 ID를 먼저 확인하고 recompute/KV RTL의 cycle/MAC 감소율을 계산한다.
# simulation cycle 감소와 board 실측 속도 향상은 다르다. 실제 시간에는 만족한 clock/timing이 필요하다.
"""같은 checkpoint/prompt의 context-recompute와 RTL KV-cache 생성 로그를 비교한다."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


# prompt/생성 ID 동등성을 먼저 확인하고 recompute/KV RTL의 cycle/MAC 감소율을 계산한다.
def compare(recompute_path: Path, cache_path: Path, output: Path) -> dict:
    recompute = json.loads(recompute_path.read_text(encoding="utf-8"))
    cached = json.loads(cache_path.read_text(encoding="utf-8"))
    for key in ("prompt", "generated_token_ids"):
        # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
        if recompute.get(key) != cached.get(key):
            raise ValueError(f"두 RTL 실행에서 {key}가 다릅니다.")
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if recompute.get("tokens_generated") != cached.get("tokens_generated"):
        raise ValueError("두 RTL 실행의 생성 token 수가 다릅니다.")
    recompute_cycles, cache_cycles = int(recompute["total_cycles"]), int(cached["total_cycles"])
    recompute_macs, cache_macs = int(recompute["total_macs"]), int(cached["total_macs"])
    result = {
        "title_ko": "동일 prompt 생성에서 context 재계산 RTL과 layer-wise K/V cache RTL 비교",
        "prompt": recompute["prompt"],
        "generated_token_ids": recompute["generated_token_ids"],
        "generated_tokens": recompute["tokens_generated"],
        "generation_outputs_equal": True,
        "context_recompute": {
            "transactions": recompute["transaction_count"],
            "cycles": recompute_cycles,
            "macs": recompute_macs,
        },
        "layerwise_kv_cache": {
            "transactions": cached["transaction_count"],
            "cycles": cache_cycles,
            "macs": cache_macs,
        },
        "simulation_cycle_reduction_percent": round((recompute_cycles-cache_cycles)*100/recompute_cycles, 2),
        "mac_reduction_percent": round((recompute_macs-cache_macs)*100/recompute_macs, 2),
        "interpretation_ko": "두 결과는 같은 Q8.8 checkpoint, prompt, greedy 출력 token을 사용한다. cycle은 Icarus transaction의 RTL cycle count이며, 실제 FPGA clock/Fmax/latency 계측이 아니다. cache 구조는 prompt 각 token을 한번씩 prefill한 뒤 과거 K/V를 재사용한다.",
        "source_files": [str(recompute_path), str(cache_path)],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


# 명령행 진입 함수. 옵션/입력/도구를 준비해 이 파일의 학습·추론·검증·분석 결과를 저장한다.
# 성공은 return0,오류는 예외/종료코드로 알린다. __main__ 직접 실행에서 자동 호출된다.
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    # 동일 prompt context-recompute RTL generation JSON 입력.
    parser.add_argument("--recompute", type=Path,
                        default=ROOT / "build" / "reports" / "trained_sequential_generation.json")
    # 동일 prompt KV RTL generation JSON 입력.
    parser.add_argument("--kvcache", type=Path,
                        default=ROOT / "build" / "reports" / "trained_kvcache_rtl_generation.json")
    # 비교/검증 JSON 저장 경로. 실패 조건은 정상 결과로 기록하지 않아야 한다.
    parser.add_argument("--output", type=Path,
                        default=ROOT / "build" / "reports" / "decode_kvcache_comparison.json")
    args = parser.parse_args()
    result = compare(args.recompute, args.kvcache, args.output)
    print(json.dumps({
        "context_recompute": result["context_recompute"],
        "layerwise_kv_cache": result["layerwise_kv_cache"],
        "cycles_saved_pct": result["simulation_cycle_reduction_percent"],
        "macs_saved_pct": result["mac_reduction_percent"],
        "generated_tokens_equal": result["generated_token_ids"],
        "output": str(args.output),
    }, ensure_ascii=False, indent=2))
    return 0


# 직접 실행할 때만 진입점을 실행한다. import한 다른 파일은 여기 함수/정의를 호출해 사용한다.
if __name__ == "__main__":
    raise SystemExit(main())
