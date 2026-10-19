#!/usr/bin/env python3
# 같은 vocabulary/config/validation 입력/정답으로 float와 integer 모델 정확도를 비교한다.
# cross entropy/top1 정답률과 두 구현의 top1 agreement는 서로 다른 지표다.
"""float32와 Q8.8 integer checkpoint의 held-out next-character 결과를 비교한다."""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from model.torch_runtime import enable_local_torch
enable_local_torch()

import torch
import torch.nn.functional as F

from model.gpt_q88 import forward_q88, load_checkpoint
from model.config_metadata import canonical_config
from model.train_tiny_gpt import TinyGPT


# 명령행 진입 함수. 옵션/입력/도구를 준비해 이 파일의 학습·추론·검증·분석 결과를 저장한다.
# 성공은 return0,오류는 예외/종료코드로 알린다. __main__ 직접 실행에서 자동 호출된다.
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    # PyTorch weight/config/vocab 저장본. QAT 출발점 또는 float 비교 기준이다.
    parser.add_argument("--float-checkpoint", type=Path,
                        default=ROOT / "output" / "tiny_gpt_demo" / "tiny_gpt_float_state.pt")
    # 동일 config/vocab의 정수 checkpoint. 실제 integer oracle 평가에 사용한다.
    parser.add_argument("--q88-checkpoint", type=Path,
                        default=ROOT / "output" / "tiny_gpt_demo" / "tiny_gpt_q88.json")
    # UTF-8 corpus 원문. character-level 모델은 고유 문자마다 ID를 만든다.
    parser.add_argument("--data", type=Path, default=ROOT / "build" / "data" / "tinyshakespeare.txt")
    # held-out 평가 표본 context 창 수. 전체 corpus/통계 신뢰구간이 아니다.
    parser.add_argument("--windows", type=int, default=32)
    # 입력 표본/random 초기화/sampling 재현 seed. 비교의 무작위 조건을 맞춘다.
    parser.add_argument("--seed", type=int, default=20261005)
    # 비교/검증 JSON 저장 경로. 실패 조건은 정상 결과로 기록하지 않아야 한다.
    parser.add_argument("--output", type=Path,
                        default=ROOT / "build" / "reports" / "quantization_validation.json")
    args = parser.parse_args()
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if args.windows < 1:
        raise ValueError("--windows는 1 이상이어야 합니다.")

    saved = torch.load(args.float_checkpoint, map_location="cpu", weights_only=False)
    q88 = load_checkpoint(args.q88_checkpoint)
    # 과거 .pt에는 affine=True인데 설명 문자열만 no-affine으로 적힌 판본이 있다.
    # 실제 계산을 고르는 boolean을 기준으로 알려진 두 설명만 정정한다.
    # 차원/activation/epsilon 등 다른 설정 차이는 여전히 실패해야 한다.
    config, float_metadata_corrections = canonical_config(saved["config"])
    q_config, q_metadata_corrections = canonical_config(q88["config"])
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if saved["vocab"] != q88["vocab"] or config != q_config:
        raise ValueError("float/Q8.8 checkpoint vocabulary 또는 설정이 다릅니다.")
    text = args.data.read_text(encoding="utf-8")
    # 문자->정수 매핑. 순서가 바뀌면 동일 ID도 다른 문자가 된다.
    stoi = {char: index for index, char in enumerate(saved["vocab"])}
    encoded = [stoi[char] for char in text]
    # corpus 앞90% train/뒤10% validation 경계. 뒤 자료는 weight update에 쓰지 않는다.
    split = int(len(encoded) * 0.9)
    validation = encoded[split:]
    context = int(config["context_length"])
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if len(validation) <= context + 1:
        raise ValueError("validation corpus가 context 길이보다 짧습니다.")

    rng = random.Random(args.seed)
    # seed로 고른 창 시작 위치. 입력과 한 글자 뒤 target이 같은 기준에서 만들어진다.
    starts = sorted(rng.sample(range(len(validation) - context),
                               min(args.windows, len(validation) - context)))
    # 평가 context ID들. float/integer에 동일 입력을 공급한다.
    input_windows = [validation[start:start + context] for start in starts]
    # 입력보다 한 token 뒤 정답 ID들. next-character prediction 정답이다.
    target_windows = [validation[start + 1:start + context + 1] for start in starts]

    model = TinyGPT(int(config["vocab_size"]), context, int(config["d_model"]),
                    int(config["heads"]), int(config["d_ff"]), int(config["layers"]),
                    linear_bias=bool(config.get("linear_bias", False)),
                    norm_affine=bool(config.get("layernorm_affine", False)),
                    activation=str(config.get("activation", "relu")))
    model.load_state_dict(saved["model_state_dict"])
    model.eval()
    # 평가/생성은 gradient를 저장하지 않고 weight도 update하지 않아 메모리/시간을 줄인다.
    with torch.no_grad():
        inputs = torch.tensor(input_windows, dtype=torch.long)
        targets = torch.tensor(target_windows, dtype=torch.long)
        float_logits = model(inputs)
        float_loss = F.cross_entropy(float_logits.reshape(-1, float_logits.shape[-1]),
                                     targets.reshape(-1)).item()
        float_top1 = float_logits.argmax(dim=-1)

    q_logits = [forward_q88(q88, window)[1] for window in input_windows]
    # raw 정수 score를 /256한 float값. 평가 cross entropy 계산에 사용한다.
    q_tensor = torch.tensor(q_logits, dtype=torch.float32) / 256.0
    q_top1 = q_tensor.argmax(dim=-1)
    q_loss = F.cross_entropy(q_tensor.reshape(-1, q_tensor.shape[-1]), targets.reshape(-1)).item()
    # 두 구현의 top1 ID 일치율. 실제 정답에 맞았는지는 accuracy로 따로 본다.
    agreement = (float_top1 == q_top1).float().mean().item()
    # validation 정답 문자와 float argmax ID 일치율.
    float_accuracy = (float_top1 == targets).float().mean().item()
    # validation 정답 문자와 Q8.8 argmax ID 일치율.
    q_accuracy = (q_top1 == targets).float().mean().item()
    evaluated = len(starts) * context
    report = {
        "title_ko": "held-out 문자 예측에서 float32와 Q8.8 integer 모델 비교",
        "float_checkpoint": str(args.float_checkpoint),
        "q88_checkpoint": str(args.q88_checkpoint),
        "data_sha256": __import__("hashlib").sha256(args.data.read_bytes()).hexdigest(),
        "seed": args.seed,
        "sampled_windows": len(starts),
        "context_length": context,
        "metadata_description_corrections": {
            "float_checkpoint": float_metadata_corrections,
            "q88_checkpoint": q_metadata_corrections,
        },
        "evaluated_next_character_positions": evaluated,
        "metrics": {
            "float32_cross_entropy": float_loss,
            "q8_8_integer_cross_entropy": q_loss,
            "float32_next_character_top1_accuracy": float_accuracy,
            "q8_8_next_character_top1_accuracy": q_accuracy,
            "float_vs_q8_8_top1_agreement": agreement,
        },
        "interpretation_ko": "고정 seed로 validation split의 일부 context window를 평가한 연구용 표본이다. 전체 corpus 평균이나 통계적 신뢰구간이 아니며, 서로 다른 수치 구현의 정확도 비교다.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report["metrics"] | {
        "sampled_windows": len(starts),
        "evaluated_positions": evaluated,
        "output": str(args.output),
    }, ensure_ascii=False, indent=2))
    return 0


# 직접 실행할 때만 진입점을 실행한다. import한 다른 파일은 여기 함수/정의를 호출해 사용한다.
if __name__ == "__main__":
    raise SystemExit(main())
