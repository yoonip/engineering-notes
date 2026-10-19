#!/usr/bin/env python3
# 원문 corpus의 다음 문자를 예측하는 작은 GPT-style 모델을 PyTorch CPU로 학습한다.
# 학습은 backward/optimizer로 weight를 바꾸는 과정이고 inference는 고정 weight로 score를 계산한다.
# Q8.8 JSON/.mem은 실제 RTL에 넣을 숫자다. PyTorch Linear weight [out,in]을 .T로
# [in,out]으로 바꾸어 SV row-major 주소/내적 방향과 일치시킨다.
# 기본 main은 float 학습 후 PTQ export이고 QAT 재학습은 qat_tiny_gpt.py가 담당한다.
"""Tiny Shakespeare로 작은 GPT-style character model을 학습하고 Q8.8로 내보낸다.

이건 상용 GPT 모델이 아니라, 이 RTL 구조를 위해 직접 학습하는 재현 가능한 작은
언어 모델이다. 학습 구조는 RTL과 맞춘 causal multi-head attention, residual+LayerNorm,
ReLU FFN, 두 개 decoder layer를 쓴다. PyTorch는 CPU만 사용한다.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from model.torch_runtime import enable_local_torch
enable_local_torch()

import torch
import torch.nn as nn
import torch.nn.functional as F

from model.gpt_q88 import generate_q88, write_mem_files

DATA_URL = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"


# forward는 Q8.8 격자/포화값, backward는 gradient를 그대로 통과시키는 STE 가짜 양자화다.
# detach 보정이 forward 값만 바꾼다. activation floor/weight nearest를 구분하며 정수 PU 완전 모사는 아니다.
def fake_q88(value: torch.Tensor, rounding: str = "floor") -> torch.Tensor:
    """Q8.8 가짜 양자화: 순전파는 고정소수점 격자, 역전파는 straight-through.

    음수 산술 right shift의 RTL 의미에 맞춰 activation은 floor를 기본 사용한다.
    가중치 export 규칙처럼 round-to-nearest가 필요한 지점은 rounding="nearest"를
    넘긴다. gradient는 clipping/rounding을 통과한 것처럼 전달한다.
    """
    # x*256의 raw 격자 값. 정수화/포화 후 /256하면 격자 위 근사 실수다.
    scaled = value * 256.0
    # activation floor/weight nearest 정책의 raw 정수화. 함수 문맥의 rounding 정책을 확인한다.
    rounded = torch.floor(scaled) if rounding == "floor" else torch.round(scaled)
    quantized = rounded.clamp(-32768, 32767) / 256.0
    return value + (quantized - value).detach()


# 일반 Linear 또는 입력/weight/bias fake-quant Linear를 적용한다.
# SV 단계별 포화/bias 경계의 bit 완전 모사가 아니므로 export 후 정수 oracle 평가가 필요하다.
def fake_linear(layer: nn.Linear, value: torch.Tensor, quant_aware: bool) -> torch.Tensor:
    if not quant_aware:
        return layer(value)
    quantized_input = fake_q88(value)
    quantized_weight = fake_q88(layer.weight, rounding="nearest")
    bias = None if layer.bias is None else fake_q88(layer.bias, rounding="nearest")
    return fake_q88(F.linear(quantized_input, quantized_weight, bias))


# 학습용 decoder 한 층. QKV/out projection/두 residual-postnorm/FFN을 nn.Module로 구성한다.
# SV 한 층의 큰 구조와 대응하지만 float/QAT surrogate와 정수 LUT 수치는 별도 평가한다.
class DecoderBlock(nn.Module):
    # 객체 초기 설정/저장 상태. 학습 model은 층/parameter를 등록하고 DRAM model은 logical 상태를 만든다.
    # 생성자 호출 자체가 inference/FPGA bitstream 생성은 아니다.
    def __init__(self, d_model: int, heads: int, d_ff: int, quant_aware: bool = False,
                 linear_bias: bool = False, norm_affine: bool = False,
                 activation: str = "relu"):
        super().__init__()
        self.d_model = d_model
        self.heads = heads
        self.head_dim = d_model // heads
        self.quant_aware = quant_aware
        self.activation = activation
        # D->D Query 학습 projection. SV wq와 대응하며 찾을 특징을 만든다.
        self.q_proj = nn.Linear(d_model, d_model, bias=linear_bias)
        # D->D Key projection. SV wk와 대응하며 검색 대상 특징을 만든다.
        self.k_proj = nn.Linear(d_model, d_model, bias=linear_bias)
        # D->D Value projection. SV wv와 대응하며 모을 내용을 만든다.
        self.v_proj = nn.Linear(d_model, d_model, bias=linear_bias)
        # head context->D attention 출력 projection. SV wo와 대응한다.
        self.out_proj = nn.Linear(d_model, d_model, bias=linear_bias)
        # 첫 residual 후 Norm. epsilon1/256 및 선택 학습 gamma/beta를 사용한다.
        self.ln1 = nn.LayerNorm(d_model, elementwise_affine=norm_affine, eps=1.0/256.0)
        # D->F FFN 확장 학습 linear. SV w1과 대응한다.
        self.ff1 = nn.Linear(d_model, d_ff, bias=linear_bias)
        # F->D FFN 축소 학습 linear. SV w2와 대응한다.
        self.ff2 = nn.Linear(d_ff, d_model, bias=linear_bias)
        # 두 번째 residual 후 Norm. 이 프로젝트는 post-norm 순서를 사용한다.
        self.ln2 = nn.LayerNorm(d_model, elementwise_affine=norm_affine, eps=1.0/256.0)

    # 순전파 QKV/head attention->residual/norm->FFN->residual/norm. score/hidden을 계산하며 batch는 동시에 처리하는 학습 예제 차원이다.
    # PyTorch float/fake-quant 수학. export 후 정수 gpt_q88/RTL exact 비교를 따로 수행한다.
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch, tokens, width = x.shape
        # Query projection. 찾을 특징이며 K와의 내적으로 관련성을 계산한다.
        q = fake_linear(self.q_proj, x, self.quant_aware).view(batch, tokens, self.heads, self.head_dim).transpose(1, 2)
        # Key projection. 검색 대상 특징이며 여러 query와 비교할 수 있다.
        k = fake_linear(self.k_proj, x, self.quant_aware).view(batch, tokens, self.heads, self.head_dim).transpose(1, 2)
        # Value projection. attention 확률로 가중 합산할 내용이다.
        v = fake_linear(self.v_proj, x, self.quant_aware).view(batch, tokens, self.heads, self.head_dim).transpose(1, 2)
        # 행/열이 같은 token 방향으로 쌓인다. 상삼각 mask가 미래 token을 차단한다.
        score = (q @ k.transpose(-2, -1)) / math.sqrt(self.head_dim)
        if self.quant_aware:
            score = fake_q88(score)
        future = torch.triu(torch.ones(tokens, tokens, device=x.device, dtype=torch.bool), diagonal=1)
        score = score.masked_fill(future, torch.finfo(score.dtype).min)
        # attention 비중. 학습은 실수 Softmax, 정수 모델은 Q8.8 LUT 근사다.
        probability = torch.softmax(score, dim=-1)
        if self.quant_aware:
            # attention 비중. 학습은 실수 Softmax, 정수 모델은 Q8.8 LUT 근사다.
            probability = fake_q88(probability)
        context = (probability @ v).transpose(1, 2).contiguous().view(batch, tokens, width)
        if self.quant_aware:
            context = fake_q88(context)
        # context*Wo. 여러 head의 내용을 섞어 residual에 더한다.
        attention = fake_linear(self.out_proj, context, self.quant_aware)
        x = self.ln1(x + attention)
        if self.quant_aware:
            x = fake_q88(x)
        ff1_linear = fake_linear(self.ff1, x, self.quant_aware)
        if self.activation == "gelu":
            # FFN 확장/activation 특징. W1 선형 뒤 비선형 ReLU/GELU를 적용한다.
            ff1 = F.gelu(ff1_linear)
        else:
            # FFN 확장/activation 특징. W1 선형 뒤 비선형 ReLU/GELU를 적용한다.
            ff1 = F.relu(ff1_linear)
        if self.quant_aware:
            # FFN 확장/activation 특징. W1 선형 뒤 비선형 ReLU/GELU를 적용한다.
            ff1 = fake_q88(ff1)
        # FFN 축소 linear 결과. norm1과 residual로 더한다.
        ff2 = fake_linear(self.ff2, ff1, self.quant_aware)
        x = self.ln2(x + ff2)
        if self.quant_aware:
            x = fake_q88(x)
        return x


# ID embedding/position embedding/여러 decoder/LM head를 연결한 학습 모델.
# nn.Module은 parameter 등록/backward 지원 클래스이며 FPGA 회로 그 자체는 아니다.
class TinyGPT(nn.Module):
    # 객체 초기 설정/저장 상태. 학습 model은 층/parameter를 등록하고 DRAM model은 logical 상태를 만든다.
    # 생성자 호출 자체가 inference/FPGA bitstream 생성은 아니다.
    def __init__(self, vocab_size: int, context_length: int, d_model: int,
                 heads: int, d_ff: int, layers: int, quant_aware: bool = False,
                 linear_bias: bool = False, norm_affine: bool = False,
                 activation: str = "relu"):
        super().__init__()
        # ID별 hidden vector 학습 표. SV token_embedding ROM과 대응한다.
        self.token_embedding = nn.Embedding(vocab_size, d_model)
        # 위치별 학습 vector 표. 같은 문자도 순서에 따라 다른 입력 표현을 받는다.
        self.position_embedding = nn.Embedding(context_length, d_model)
        self.quant_aware = quant_aware
        self.linear_bias = linear_bias
        self.norm_affine = norm_affine
        self.activation = activation
        # 서로 독립 weight의 decoder 층 list. 앞층 결과가 다음층 입력이다.
        self.blocks = nn.ModuleList([DecoderBlock(d_model, heads, d_ff, quant_aware,
                                                   linear_bias, norm_affine, activation)
                                     for _ in range(layers)])
        # hidden->V 후보 점수 linear. SV lm_head 및 선택 lm_bias와 대응한다.
        self.lm_head = nn.Linear(d_model, vocab_size, bias=linear_bias)
        self.context_length = context_length

    # 순전파 embedding+position->decoder 층들->LM head. score/hidden을 계산하며 batch는 동시에 처리하는 학습 예제 차원이다.
    # PyTorch float/fake-quant 수학. export 후 정수 gpt_q88/RTL exact 비교를 따로 수행한다.
    def forward(self, token_ids: torch.Tensor) -> torch.Tensor:
        _, tokens = token_ids.shape
        positions = torch.arange(tokens, device=token_ids.device)
        x = self.token_embedding(token_ids) + self.position_embedding(positions)[None, :, :]
        if self.quant_aware:
            x = fake_q88(x, rounding="nearest")
        for block in self.blocks:
            x = block(x)
        return fake_linear(self.lm_head, x, self.quant_aware)


# corpus의 context 입력 창과 한 글자 뒤 정답 창을 batch_size개 뽑는다.
# 시작 위치는 torch Generator seed로 재현한다. next-character 각 위치의 정답은 바로 다음 문자다.
def get_batch(data: torch.Tensor, block_size: int, batch_size: int,
              generator: torch.Generator) -> tuple[torch.Tensor, torch.Tensor]:
    # seed로 고른 창 시작 위치. 입력과 한 글자 뒤 target이 같은 기준에서 만들어진다.
    starts = torch.randint(len(data)-block_size-1, (batch_size,), generator=generator)
    x = torch.stack([data[start:start+block_size] for start in starts])
    y = torch.stack([data[start+1:start+block_size+1] for start in starts])
    return x, y


# train/validation 표본의 평균 next-character cross entropy를 gradient 없이 평가한다.
# 낮으면 정답 문자에 높은 확률을 주지만 사람 수준 대화 능력 점수는 아니다.
@torch.no_grad()
def estimate_loss(model: TinyGPT, train_data: torch.Tensor, val_data: torch.Tensor,
                  block_size: int, batch_size: int, seed: int) -> dict[str, float]:
    model.eval()
    result: dict[str, float] = {}
    for name, data in (("train", train_data), ("validation", val_data)):
        generator = torch.Generator().manual_seed(seed + (1 if name == "validation" else 0))
        losses = []
        for _ in range(30):
            x, y = get_batch(data, block_size, batch_size, generator)
            # 어휘 후보 점수. 자체는 확률이 아니며 argmax/sampling 입력이다.
            logits = model(x)
            losses.append(F.cross_entropy(logits.reshape(-1, logits.shape[-1]), y.reshape(-1)).item())
        result[name] = sum(losses) / len(losses)
    model.train()
    return result


# 학습 float*256을 nearest 반올림/signed16 포화하여 raw 정수 list로 export한다.
# weight 저장 nearest와 inference 산술 >>8 floor는 서로 다른 수치 경계/목적이다.
def q88(value: torch.Tensor) -> list[list[int]] | list[int]:
    quantized = torch.round(value.detach().cpu() * 256).clamp(-32768, 32767).to(torch.int32)
    return quantized.tolist()


# PyTorch [out,in] weight를 RTL [in,out]으로 .T하고 embedding/bias/gamma/beta를 Q8.8로 내보낸다.
# config/vocab 순서도 저장해야 같은 ID/bit가 같은 다음 문자 점수를 나타낸다.
def quantized_checkpoint(model: TinyGPT, vocabulary: list[str], config: dict[str, Any]) -> dict[str, Any]:
    state = model.state_dict()
    layers = []
    # head는 채널별 관점,layer는 직렬 block 반복. 올바른 slice/층 가중치를 선택해 처리한다.
    for layer_index in range(config["layers"]):
        prefix = f"blocks.{layer_index}."
        layer = {
            "wq": q88(state[prefix + "q_proj.weight"].T),
            "wk": q88(state[prefix + "k_proj.weight"].T),
            "wv": q88(state[prefix + "v_proj.weight"].T),
            "wo": q88(state[prefix + "out_proj.weight"].T),
            "w1": q88(state[prefix + "ff1.weight"].T),
            "w2": q88(state[prefix + "ff2.weight"].T),
        }
        for name, module_name in (("bq", "q_proj"), ("bk", "k_proj"),
                                  ("bv", "v_proj"), ("bo", "out_proj"),
                                  ("b1", "ff1"), ("b2", "ff2")):
            key = prefix + module_name + ".bias"
            if key in state:
                layer[name] = q88(state[key])
        for name, module_name in (("ln1_gamma", "ln1"), ("ln1_beta", "ln1"),
                                  ("ln2_gamma", "ln2"), ("ln2_beta", "ln2")):
            parameter_name = "weight" if name.endswith("gamma") else "bias"
            key = prefix + module_name + "." + parameter_name
            if key in state:
                layer[name] = q88(state[key])
        layers.append(layer)
    lm_bias = state.get("lm_head.bias")
    return {
        "format": "signed_q8.8_row_major_v1",
        "description_ko": "Tiny Shakespeare로 학습한 2-layer causal GPT-style 모델. 가중치는 float32에서 signed Q8.8로 반올림/포화했다.",
        "config": config,
        "vocab": vocabulary,
        "unknown_token_id": vocabulary.index(" ") if " " in vocabulary else 0,
        "weights": {
            "token_embedding": q88(state["token_embedding.weight"]),
            "position_embedding": q88(state["position_embedding.weight"]),
            "layers": layers,
            "lm_head": q88(state["lm_head.weight"].T),
            **({"lm_bias": q88(lm_bias)} if lm_bias is not None else {}),
        },
    }


# 실수 학습 모델의 마지막 score를 확률로 바꿔 sampling하는 예시다. RTL integer oracle은 아니다.
def generate_float(model: TinyGPT, prompt_ids: list[int], vocabulary: list[str],
                   count: int, seed: int) -> str:
    generator = torch.Generator().manual_seed(seed)
    ids = torch.tensor([prompt_ids], dtype=torch.long)
    model.eval()
    # 평가/생성은 gradient를 저장하지 않고 weight도 update하지 않아 메모리/시간을 줄인다.
    with torch.no_grad():
        for _ in range(count):
            context = ids[:, -model.context_length:]
            # 어휘 후보 점수. 자체는 확률이 아니며 argmax/sampling 입력이다.
            logits = model(context)[:, -1, :]
            # 마지막 score로 고른 다음 문자 번호. vocab[next_id]가 실제 문자다.
            next_id = torch.multinomial(torch.softmax(logits, dim=-1), 1, generator=generator)
            ids = torch.cat([ids, next_id], dim=1)
    return "".join(vocabulary[index] for index in ids[0].tolist())


# 명령행 진입 함수. 옵션/입력/도구를 준비해 이 파일의 학습·추론·검증·분석 결과를 저장한다.
# 성공은 return0,오류는 예외/종료코드로 알린다. __main__ 직접 실행에서 자동 호출된다.
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    # optimizer update 횟수. step 한 번은 batch forward/backward/weight update다.
    parser.add_argument("--steps", type=int, default=800)
    # 입력 표본/random 초기화/sampling 재현 seed. 비교의 무작위 조건을 맞춘다.
    parser.add_argument("--seed", type=int, default=20261003)
    # context 최대 token 수. learned position table/KV cache 상한을 결정한다.
    parser.add_argument("--context-length", type=int, default=32)
    # hidden 채널 D. 모든 head 폭의 합이며 embedding/residual 폭이다.
    parser.add_argument("--d-model", type=int, default=16)
    # attention 관점 H. D가 H로 나누어져야 channel slice를 분할할 수 있다.
    parser.add_argument("--heads", type=int, default=4)
    # FFN 확장 F. W1 D*F/W2 F*D의 저장 및 MAC 비용을 결정한다.
    parser.add_argument("--d-ff", type=int, default=32)
    # decoder 층 L. 앞층 결과를 다음층에 전달하고 층별 weight를 사용한다.
    parser.add_argument("--layers", type=int, default=2)
    # 학습 step에서 동시에 처리할 context 창 수. head 수와 다른 차원이다.
    parser.add_argument("--batch-size", type=int, default=32)
    # optimizer weight update 크기. inference clock/score scale이 아니다.
    parser.add_argument("--learning-rate", type=float, default=0.001)
    # 선형 QKV/Wo/FFN/LM bias 학습. checkpoint와 RTL ENABLE_BIAS를 맞춘다.
    parser.add_argument("--linear-bias", action="store_true",
                        help="attention/FFN/LM linear에 학습 bias를 추가")
    # LayerNorm gamma/beta 학습. RTL ENABLE_NORM_AFFINE과 맞춘다.
    parser.add_argument("--layernorm-affine", action="store_true",
                        help="LayerNorm에 학습 gamma/beta를 추가")
    # FFN 비선형 ReLU/GELU. 학습 정의와 RTL ENABLE_GELU를 맞춘다.
    parser.add_argument("--activation", choices=("relu", "gelu"), default="relu")
    # checkpoint/trace/JSON 생성 폴더. model parameter가 아닌 파일 경로다.
    parser.add_argument("--output-dir", type=Path, default=ROOT / "output" / "tiny_gpt_demo")
    # UTF-8 corpus 원문. character-level 모델은 고유 문자마다 ID를 만든다.
    parser.add_argument("--data", type=Path, default=ROOT / "build" / "data" / "tinyshakespeare.txt")
    args = parser.parse_args()
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if args.d_model % args.heads:
        raise ValueError("d_model은 heads로 나누어져야 합니다.")

    torch.set_num_threads(max(1, min(4, os.cpu_count() or 1)))
    torch.manual_seed(args.seed)
    args.data.parent.mkdir(parents=True, exist_ok=True)
    if not args.data.exists():
        print(f"데이터 다운로드: {DATA_URL}")
        request = urllib.request.Request(DATA_URL, headers={"User-Agent": "research-transformer-demo/1.0"})
        with urllib.request.urlopen(request, timeout=60) as response:
            args.data.write_bytes(response.read())
    text = args.data.read_text(encoding="utf-8")
    # ID 순서 문자 목록. checkpoint export와 decoding에서 순서를 보존한다.
    vocabulary = sorted(set(text))
    # 문자->정수 매핑. 순서가 바뀌면 동일 ID도 다른 문자가 된다.
    stoi = {char: index for index, char in enumerate(vocabulary)}
    encoded = torch.tensor([stoi[char] for char in text], dtype=torch.long)
    # corpus 앞90% train/뒤10% validation 경계. 뒤 자료는 weight update에 쓰지 않는다.
    split = int(len(encoded) * 0.9)
    train_data, val_data = encoded[:split], encoded[split:]
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if min(len(train_data), len(val_data)) <= args.context_length + 1:
        raise ValueError("학습 corpus가 context_length보다 짧습니다.")

    config = {
        "vocab_size": len(vocabulary), "context_length": args.context_length,
        "d_model": args.d_model, "heads": args.heads, "head_dim": args.d_model // args.heads,
        "d_ff": args.d_ff, "layers": args.layers, "score_scale_q8": round(256 / math.sqrt(args.d_model // args.heads)),
        "q_format": "signed Q8.8, 16-bit", "activation": "ReLU",
        "normalization": ("post-residual LayerNorm, epsilon=1/256, learned gamma/beta affine parameters"
                          if args.layernorm_affine else
                          "post-residual LayerNorm, epsilon=1/256, no learned affine parameters"),
        "tokenizer": "character-level; each corpus character is one token",
        "linear_bias": args.linear_bias,
        "layernorm_affine": args.layernorm_affine,
        "activation": args.activation,
    }
    model = TinyGPT(len(vocabulary), args.context_length, args.d_model,
                    args.heads, args.d_ff, args.layers,
                    linear_bias=args.linear_bias, norm_affine=args.layernorm_affine,
                    activation=args.activation)
    # 학습하는 scalar weight 총수. vocabulary/head 수와 다른 규모 지표다.
    parameter_count = sum(parameter.numel() for parameter in model.parameters())
    # gradient로 weight를 업데이트하는 AdamW. inference에는 필요 없다.
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate)
    generator = torch.Generator().manual_seed(args.seed)
    before = estimate_loss(model, train_data, val_data, args.context_length, args.batch_size, args.seed)

    started = time.monotonic()
    model.train()
    # 학습 step 반복. batch->forward->loss->backward->optimizer update로 동일 구조의 weight를 개선한다.
    for step in range(1, args.steps + 1):
        x, y = get_batch(train_data, args.context_length, args.batch_size, generator)
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
        if step == 1 or step % 100 == 0 or step == args.steps:
            print(f"step={step}/{args.steps} train_batch_loss={loss.item():.4f}", flush=True)
    elapsed = time.monotonic() - started
    after = estimate_loss(model, train_data, val_data, args.context_length, args.batch_size, args.seed + 7)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    float_path = args.output_dir / "tiny_gpt_float_state.pt"
    torch.save({"model_state_dict": model.state_dict(), "config": config,
                "vocab": vocabulary}, float_path)
    quantized = quantized_checkpoint(model, vocabulary, config)
    q88_path = args.output_dir / "tiny_gpt_q88.json"
    q88_path.write_text(json.dumps(quantized, ensure_ascii=True, separators=(",", ":")), encoding="utf-8")
    write_mem_files(quantized, args.output_dir / "mem")

    prompt = "ROMEO:" if all(char in stoi for char in "ROMEO:") else text[:8]
    prompt_ids = [stoi[char] for char in prompt]
    float_sample = generate_float(model, prompt_ids, vocabulary, 120, args.seed + 11)
    quant_sample = generate_q88(quantized, prompt, 120, seed=args.seed + 11)
    report = {
        "title_ko": "작은 GPT-style character language model 학습 기록",
        "data_source": DATA_URL,
        "data_sha256": hashlib.sha256(args.data.read_bytes()).hexdigest(),
        "data_characters": len(text),
        "vocabulary_size": len(vocabulary),
        "parameter_count": parameter_count,
        "steps": args.steps,
        "seed": args.seed,
        "device": "CPU",
        "elapsed_training_seconds": round(elapsed, 2),
        "loss_before_training": before,
        "loss_after_training": after,
        "float32_sample": float_sample,
        "q8_8_sample": quant_sample,
        "output_files": [float_path.name, q88_path.name, "mem/*.mem"],
        "limitations": [
            "소규모 character corpus와 CPU로 학습한 연구용 모델이며 사람 수준 텍스트 생성 모델이 아니다.",
            "Q8.8은 float32 학습 가중치를 사후 양자화한 것으로 QAT/재학습을 하지 않았다.",
            "RTL에는 문자 tokenizer와 sampling loop/KV cache가 포함되지 않고, 토큰 ID·logits 사이를 계산한다.",
        ],
    }
    report_path = args.output_dir / "training_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    sample_path = args.output_dir / "generated_text.txt"
    sample_path.write_text(
        "[float32 모델 출력]\n" + float_sample + "\n\n[Q8.8 정수 모델 출력]\n" + quant_sample + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"loss_before": before, "loss_after": after,
                      "elapsed_seconds": round(elapsed, 2), "parameters": parameter_count,
                      "float_sample": float_sample, "q88_sample": quant_sample}, ensure_ascii=False, indent=2))
    print(f"모델 및 보고서: {args.output_dir}")
    return 0


# 직접 실행할 때만 진입점을 실행한다. import한 다른 파일은 여기 함수/정의를 호출해 사용한다.
if __name__ == "__main__":
    raise SystemExit(main())
