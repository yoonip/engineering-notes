#!/usr/bin/env python3
# 기존 float weight를 Q8.8 격자/포화를 고려하도록 추가 학습하는 QAT 실행기다.
# STE는 반올림의 실제 미분 대신 gradient를 통과시켜 optimizer가 숫자를 조절하게 한다.
# 학습 Softmax/LayerNorm/GELU는 PyTorch 실수 연산이므로 RTL과 bit 동일한 학습은 아니다.
# export한 정수 checkpoint를 gpt_q88 및 RTL에서 별도 검증해야 실제 수치 정확도를 알 수 있다.
"""float32 pretrained TinyGPT를 Q8.8 가짜 양자화로 fine-tune한다.

Straight-through estimator를 이용해 학습 중 Q8.8 반올림/포화를 순전파에
반영한다. Softmax LUT와 RTL 정수 LayerNorm까지 비트 단위로 모사하는 학습은
아니므로, 최종 성능은 별도 정수 checkpoint 평가로 판정해야 한다.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from model.torch_runtime import enable_local_torch
enable_local_torch()

import torch
import torch.nn.functional as F

from model.gpt_q88 import generate_q88_cached, write_mem_files
from model.train_tiny_gpt import TinyGPT, get_batch, quantized_checkpoint


# 명령행 진입 함수. 옵션/입력/도구를 준비해 이 파일의 학습·추론·검증·분석 결과를 저장한다.
# 성공은 return0,오류는 예외/종료코드로 알린다. __main__ 직접 실행에서 자동 호출된다.
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    # PyTorch weight/config/vocab 저장본. QAT 출발점 또는 float 비교 기준이다.
    parser.add_argument("--float-checkpoint", type=Path,
                        default=ROOT / "output" / "tiny_gpt_demo" / "tiny_gpt_float_state.pt")
    # UTF-8 corpus 원문. character-level 모델은 고유 문자마다 ID를 만든다.
    parser.add_argument("--data", type=Path, default=ROOT / "build" / "data" / "tinyshakespeare.txt")
    # optimizer update 횟수. step 한 번은 batch forward/backward/weight update다.
    parser.add_argument("--steps", type=int, default=1000)
    # 입력 표본/random 초기화/sampling 재현 seed. 비교의 무작위 조건을 맞춘다.
    parser.add_argument("--seed", type=int, default=20261004)
    # optimizer weight update 크기. inference clock/score scale이 아니다.
    parser.add_argument("--learning-rate", type=float, default=0.0001)
    # 학습 step에서 동시에 처리할 context 창 수. head 수와 다른 차원이다.
    parser.add_argument("--batch-size", type=int, default=32)
    # checkpoint/trace/JSON 생성 폴더. model parameter가 아닌 파일 경로다.
    parser.add_argument("--output-dir", type=Path, default=ROOT / "output" / "tiny_gpt_qat")
    args = parser.parse_args()
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if args.steps < 1:
        raise ValueError("--steps는 1 이상이어야 합니다.")

    torch.set_num_threads(max(1, min(4, os.cpu_count() or 1)))
    torch.manual_seed(args.seed)
    random.seed(args.seed)
    saved = torch.load(args.float_checkpoint, map_location="cpu", weights_only=False)
    config = dict(saved["config"])
    # 이전 실행 파일의 설명 문자열이 남았더라도 실제 활성 옵션과 일치시킨다.
    # 학습 tensor/수치 동작은 layernorm_affine 옵션에 의해 결정된다.
    config["normalization"] = (
        "post-residual LayerNorm, epsilon=1/256, learned gamma/beta affine parameters"
        if config.get("layernorm_affine", False) else
        "post-residual LayerNorm, epsilon=1/256, no learned affine parameters"
    )
    # ID 순서 문자 목록. checkpoint export와 decoding에서 순서를 보존한다.
    vocabulary = saved["vocab"]
    text = args.data.read_text(encoding="utf-8")
    # 문자->정수 매핑. 순서가 바뀌면 동일 ID도 다른 문자가 된다.
    stoi = {char: index for index, char in enumerate(vocabulary)}
    unknown = [char for char in set(text) if char not in stoi]
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if unknown:
        raise ValueError("학습 checkpoint에 없는 corpus 문자가 있습니다.")
    encoded = torch.tensor([stoi[char] for char in text], dtype=torch.long)
    # corpus 앞90% train/뒤10% validation 경계. 뒤 자료는 weight update에 쓰지 않는다.
    split = int(len(encoded) * 0.9)
    train_data, validation_data = encoded[:split], encoded[split:]
    block_size = int(config["context_length"])
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if len(validation_data) <= block_size + 1:
        raise ValueError("validation corpus가 context 길이보다 짧습니다.")

    model = TinyGPT(
        int(config["vocab_size"]), block_size, int(config["d_model"]),
        int(config["heads"]), int(config["d_ff"]), int(config["layers"]),
        quant_aware=True,
        linear_bias=bool(config.get("linear_bias", False)),
        norm_affine=bool(config.get("layernorm_affine", False)),
        activation=str(config.get("activation", "relu")),
    )
    model.load_state_dict(saved["model_state_dict"])
    # gradient로 weight를 업데이트하는 AdamW. inference에는 필요 없다.
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate)
    batch_rng = torch.Generator().manual_seed(args.seed)
    val_rng = torch.Generator().manual_seed(args.seed + 1)

    # QAT fake-quant validation loss를 no_grad 평균 후 training 모드로 복귀한다. 정수 RTL 평가와 다르다.
    def estimate(data: torch.Tensor, generator: torch.Generator, batches: int = 24) -> float:
        model.eval()
        losses = []
        # 평가/생성은 gradient를 저장하지 않고 weight도 update하지 않아 메모리/시간을 줄인다.
        with torch.no_grad():
            for _ in range(batches):
                x, y = get_batch(data, block_size, args.batch_size, generator)
                # 어휘 후보 점수. 자체는 확률이 아니며 argmax/sampling 입력이다.
                logits = model(x)
                losses.append(F.cross_entropy(logits.reshape(-1, logits.shape[-1]), y.reshape(-1)).item())
        model.train()
        return sum(losses) / len(losses)

    initial_validation = estimate(validation_data, val_rng)
    started = time.monotonic()
    model.train()
    # 학습 step 반복. batch->forward->loss->backward->optimizer update로 동일 구조의 weight를 개선한다.
    for step in range(1, args.steps + 1):
        x, y = get_batch(train_data, block_size, args.batch_size, batch_rng)
        # 어휘 후보 점수. 자체는 확률이 아니며 argmax/sampling 입력이다.
        logits = model(x)
        # 정답 문자와 예측 분포 cross entropy. backward는 이 오차를 줄일 weight gradient를 계산한다.
        loss = F.cross_entropy(logits.reshape(-1, len(vocabulary)), y.reshape(-1))
        # 이전 batch gradient를 지워 현재 batch의 오차로 update하도록 한다.
        optimizer.zero_grad(set_to_none=True)
        # loss의 각 weight gradient를 역전파한다. 학습 전용 과정이며 RTL inference에는 없다.
        loss.backward()
        # gradient 크기를 제한해 큰 update를 줄인다. Q8.8 sat16와 다른 학습 안정화다.
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        # optimizer가 gradient로 weight를 변경한다. 다음 forward부터 새 학습 숫자를 사용한다.
        optimizer.step()
        if step == 1 or step % 200 == 0 or step == args.steps:
            print(f"QAT step={step}/{args.steps} train_batch_loss={loss.item():.4f}", flush=True)
    elapsed = time.monotonic() - started
    final_validation = estimate(validation_data, val_rng)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    float_path = args.output_dir / "tiny_gpt_qat_float_state.pt"
    torch.save({"model_state_dict": model.state_dict(), "config": config,
                "vocab": vocabulary}, float_path)
    checkpoint = quantized_checkpoint(model, vocabulary, config)
    checkpoint["description_ko"] += " Q8.8 fake-quantization QAT fine-tuning을 거친 가중치."
    checkpoint["format"] = "signed_q8.8_row_major_qat_v1"
    checkpoint_path = args.output_dir / "tiny_gpt_qat_q88.json"
    checkpoint_path.write_text(json.dumps(checkpoint, ensure_ascii=True, separators=(",", ":")), encoding="utf-8")
    write_mem_files(checkpoint, args.output_dir / "mem")
    prompt = "ROMEO:" if all(char in stoi for char in "ROMEO:") else text[:8]
    sample = generate_q88_cached(checkpoint, prompt, max_new_tokens=80, seed=args.seed)
    report = {
        "title_ko": "Q8.8 가짜 양자화 인식 fine-tuning 실행 기록",
        "source_checkpoint": str(args.float_checkpoint),
        "data_sha256": __import__("hashlib").sha256(args.data.read_bytes()).hexdigest(),
        "steps": args.steps,
        "seed": args.seed,
        "learning_rate": args.learning_rate,
        "elapsed_seconds": round(elapsed, 2),
        "fake_quant_validation_loss_before": initial_validation,
        "fake_quant_validation_loss_after": final_validation,
        "fake_quant_method_ko": "activation은 Q8.8 격자로 floor 절삭, embedding과 weight는 round-to-nearest, signed 16-bit saturation, gradient는 STE로 통과.",
        "limitation_ko": "학습의 softmax는 PyTorch 연산, LayerNorm은 PyTorch 실수 연산을 거친 뒤 Q8.8 가짜 양자화하므로 RTL LUT/정수 LayerNorm과 비트 동일하지 않다. 실제 Q8.8 정수 validation 결과를 별도로 비교해야 한다.",
        "generated_q88_sample": sample,
        "files": [float_path.name, checkpoint_path.name, "mem/*.mem"],
    }
    report_path = args.output_dir / "qat_training_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"fake_quant_validation_before": initial_validation,
                      "fake_quant_validation_after": final_validation,
                      "elapsed_seconds": round(elapsed, 2),
                      "checkpoint": str(checkpoint_path),
                      "report": str(report_path)}, ensure_ascii=False, indent=2))
    return 0


# 직접 실행할 때만 진입점을 실행한다. import한 다른 파일은 여기 함수/정의를 호출해 사용한다.
if __name__ == "__main__":
    raise SystemExit(main())
