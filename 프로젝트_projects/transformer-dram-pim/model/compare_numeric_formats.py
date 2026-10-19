#!/usr/bin/env python3
# 같은 float weight의 Q8.8/E8M7 저장 표현 오차만 비교한다.
# MAE/RMSE/max error는 파라미터 오차이고 전체 Transformer 정확도/FPGA E8M7 연산기 증거는 아니다.
"""float32 학습 가중치를 Q8.8/E8M7로 반올림해 수치 오차를 비교한다.

이것은 가중치 표현 비교만 수행한다. Q8.8은 RTL 연산까지 있는 기준 경로지만,
E8M7은 형식 인코더/디코더 비교이며 SystemVerilog E8M7 산술 구현이 아니다.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from model.torch_runtime import enable_local_torch
enable_local_torch()
import torch

from model.e8m7 import decode_e8m7, encode_e8m7

# 같은 원소의 절대 오차 평균/제곱 평균 제곱근/최대값을 계산한다. 저장 표현 오차이고 모델 정확도는 아니다.
def summarize(reference: list[float], quantized: list[float], tags: dict[str, int]) -> dict:
    absolute = [abs(a - b) for a, b in zip(reference, quantized)]
    return {
        "values": len(reference),
        "mean_absolute_error": sum(absolute) / max(1, len(absolute)),
        "rmse": math.sqrt(sum(error * error for error in absolute) / max(1, len(absolute))),
        "max_absolute_error": max(absolute, default=0.0),
        **tags,
    }


# 같은 float weight의 Q8.8/E8M7 표현 오차를 계산해 JSON으로 저장한다.
def compare(float_checkpoint: Path, output: Path) -> dict:
    payload = torch.load(float_checkpoint, map_location="cpu", weights_only=False)
    state = payload["model_state_dict"]
    values = [float(value) for tensor in state.values() for value in tensor.reshape(-1).tolist()]

    q88_values: list[float] = []
    q88_saturated = 0
    for value in values:
        # x*256의 raw 격자 값. 정수화/포화 후 /256하면 격자 위 근사 실수다.
        scaled = value * 256.0
        # activation floor/weight nearest 정책의 raw 정수화. 함수 문맥의 rounding 정책을 확인한다.
        rounded = round(scaled)
        clamped = max(-32768, min(32767, rounded))
        q88_saturated += int(clamped != rounded)
        q88_values.append(clamped / 256.0)

    e8m7_words = [encode_e8m7(value) for value in values]
    e8m7_values = [decode_e8m7(word) for word in e8m7_words]
    e8m7_inf = sum(math.isinf(value) for value in e8m7_values)
    e8m7_nan = sum(math.isnan(value) for value in e8m7_values)
    e8m7_subnormal = sum(((word >> 7) & 0xFF) == 0 and (word & 0x7F) != 0
                         for word in e8m7_words)
    e8m7_zero = sum((word & 0x7FFF) == 0 for word in e8m7_words)

    report = {
        "title_ko": "float32 학습 가중치의 Q8.8/E8M7 표현 오차 비교",
        "definition_ko": "E8M7은 sign 1-bit, exponent 8-bit(bias 127), fraction 7-bit, subnormal/signed zero/Inf/NaN, round-to-nearest-ties-to-even으로 정의했다.",
        "scope_ko": "파라미터 표현 오차만 비교한다. attention/LayerNorm 누적 오차, E8M7 연산기, RTL 구현 비용은 이 결과에 포함하지 않는다.",
        "source": str(float_checkpoint),
        "parameter_count": len(values),
        "q8_8": summarize(values, q88_values, {
            "saturated_values": q88_saturated,
            "zero_values": sum(value == 0 for value in q88_values),
            "word_bits": 16,
        }),
        "e8m7": summarize(values, e8m7_values, {
            "infinity_values": e8m7_inf,
            "nan_values": e8m7_nan,
            "subnormal_values": e8m7_subnormal,
            "zero_values": e8m7_zero,
            "word_bits": 16,
        }),
        "interpretation_ko": [
            "Q8.8은 절대 오차가 거의 일정하지만 값이 약 ±128 범위를 넘으면 포화된다.",
            "E8M7은 표현 범위가 매우 넓지만 일반 수의 유효 정밀도가 대략 7 fraction bit다.",
            "같은 16-bit 저장 폭만으로 어떤 형식이 모델 정확도나 하드웨어 성능에서 더 낫다고 결론내릴 수 없다.",
        ],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


# 명령행 진입 함수. 옵션/입력/도구를 준비해 이 파일의 학습·추론·검증·분석 결과를 저장한다.
# 성공은 return0,오류는 예외/종료코드로 알린다. __main__ 직접 실행에서 자동 호출된다.
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    # PyTorch weight/config/vocab 저장본. QAT 출발점 또는 float 비교 기준이다.
    parser.add_argument("--float-checkpoint", type=Path,
                        default=ROOT / "output" / "tiny_gpt_demo" / "tiny_gpt_float_state.pt")
    # 비교/검증 JSON 저장 경로. 실패 조건은 정상 결과로 기록하지 않아야 한다.
    parser.add_argument("--output", type=Path,
                        default=ROOT / "build" / "reports" / "numeric_format_comparison.json")
    args = parser.parse_args()
    report = compare(args.float_checkpoint, args.output)
    print(json.dumps({"parameter_count": report["parameter_count"],
                      "q8_8": report["q8_8"], "e8m7": report["e8m7"],
                      "output": str(args.output)}, ensure_ascii=False, indent=2))
    return 0


# 직접 실행할 때만 진입점을 실행한다. import한 다른 파일은 여기 함수/정의를 호출해 사용한다.
if __name__ == "__main__":
    raise SystemExit(main())
