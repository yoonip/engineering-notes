#!/usr/bin/env python3
# 같은 checkpoint/seed/sampling의 Python cache/recompute 생성 결과를 비교한다.
# software wall time은 FPGA cycle/Fmax 측정과 다르다. 실제 KV RTL 검증은 verify_trained_generation --kvcache-rtl이다.
"""학습 checkpoint의 cached/uncached Q8.8 생성 결과를 비교한다."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from model.gpt_q88 import generate_q88, generate_q88_cached, load_checkpoint

ROOT = Path(__file__).resolve().parent


# 명령행 진입 함수. 옵션/입력/도구를 준비해 이 파일의 학습·추론·검증·분석 결과를 저장한다.
# 성공은 return0,오류는 예외/종료코드로 알린다. __main__ 직접 실행에서 자동 호출된다.
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    # 정수 inference JSON config/vocab/weight. 저장한 숫자를 읽고 새 학습을 하지 않는다.
    parser.add_argument("--checkpoint", type=Path,
                        default=ROOT / "output" / "tiny_gpt_full_ops_qat" / "tiny_gpt_qat_q88.json")
    # 입력 문자열->ID. prompt 마지막 score가 첫 생성 token을 예측한다.
    parser.add_argument("--prompt", default="ROMEO:")
    # generation에서는 새 token 수, DRAM 모델에서는 context token 수. 파일 목적에 따라 의미가 다르다.
    parser.add_argument("--tokens", type=int, default=20)
    # 입력 표본/random 초기화/sampling 재현 seed. 비교의 무작위 조건을 맞춘다.
    parser.add_argument("--seed", type=int, default=20261003)
    # 비교/검증 JSON 저장 경로. 실패 조건은 정상 결과로 기록하지 않아야 한다.
    parser.add_argument("--output", type=Path,
                        default=ROOT / "build" / "reports" / "trained_q88_kv_cache.json")
    args = parser.parse_args()
    model = load_checkpoint(args.checkpoint)
    start = time.perf_counter()
    full = generate_q88(model, args.prompt, args.tokens, temperature=0.8, top_k=8, seed=args.seed)
    full_seconds = time.perf_counter() - start
    start = time.perf_counter()
    cached = generate_q88_cached(model, args.prompt, args.tokens,
                                 temperature=0.8, top_k=8, seed=args.seed)
    cached_seconds = time.perf_counter() - start
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if full != cached:
        raise AssertionError("KV cache를 사용한 Q8.8 생성 문자열이 전체 재계산 경로와 다릅니다.")

    config = model["config"]
    d_model = int(config["d_model"])
    layers = int(config["layers"])
    context = int(config["context_length"])
    peak_tokens = min(context, len(args.prompt) + args.tokens)
    # 2(K,V)*L*유효T*D*2byte의 논리 용량. 실제 BRAM port/배치 mapping이 아니다.
    cache_bytes = 2 * layers * peak_tokens * d_model * 2  # K와 V, signed 16-bit
    report = {
        "checkpoint": str(args.checkpoint),
        "prompt": args.prompt,
        "generated_tokens": args.tokens,
        "seed": args.seed,
        "sampling": "temperature=0.8, top_k=8, Python random.Random 동일 seed",
        "full_recompute_and_kv_cache_exact_text_match": True,
        "generated_text": cached,
        "uncached_python_seconds": full_seconds,
        "cached_python_seconds": cached_seconds,
        "kv_cache_peak_bytes_q8_8": cache_bytes,
        "cache_definition_ko": "각 decoder layer에 hidden 폭 D의 key와 value를 token마다 저장한다. 16-bit 정수 기준 byte=2(K/V)×layer×token×D×2 bytes.",
        "window_limit_ko": "학습된 absolute position embedding을 context 초과 시 0부터 다시 매기는 full reference와 동등하려고 context 창이 넘으면 cache를 비우고 재계산한다. 이 경계 이후에는 계속 재사용되는 무효화 없는 KV-cache 구현이 아니다.",
        "rtl_scope_ko": "RTL token generation은 별도 verify_trained_generation.py가 host/testbench argmax loop로 검사한다. sequential RTL은 매 transaction context 전체를 재계산하고 내부 KV cache는 없다.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"exact_match": True, "generated_tokens": args.tokens,
                      "full_seconds": round(full_seconds, 4),
                      "cached_seconds": round(cached_seconds, 4),
                      "peak_cache_bytes": cache_bytes,
                      "output": str(args.output)}, ensure_ascii=False, indent=2))
    return 0


# 직접 실행할 때만 진입점을 실행한다. import한 다른 파일은 여기 함수/정의를 호출해 사용한다.
if __name__ == "__main__":
    raise SystemExit(main())
