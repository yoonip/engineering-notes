# 학습 checkpoint를 RTL과 같은 Q8.8 수치 정의로 계산하는 독립 Python 기준 모델이다.
# forward_q88는 전체 문맥, forward_q88_step은 K/V를 재사용하는 현재 token 한 개를 처리한다.
# raw256=1.0,-128=-0.5. Python int로 넓게 누산한 후 명시적 포화/절삭 경계에서 16bit로 제한한다.
# 문자->ID, sampling, 반복 생성은 host 역할이며 RTL core는 ID->logit 수학에 대응한다.
# PyTorch float/QAT 학습 수학과 구분하며 최종 RTL 정답 비교에는 이 정수 oracle을 쓴다.
"""학습한 GPT-style 모델을 RTL과 같은 Q8.8 정수 규칙으로 실행한다."""

from __future__ import annotations

import json
import math
import random
from pathlib import Path
from typing import Any


# signed16 -32768..32767 포화. wrap으로 부호가 뒤집히는 것을 막는 SV sat16과 같다.
# Q8.8 실제값 범위는 -128..127.99609375이며 raw/256으로 읽는다.
def sat16(value: int) -> int:
    return max(-32768, min(32767, value))


# SV signed 나눗셈의 0 방향 절삭. Python //는 음수에서 아래 방향이므로 직접 쓰면 다르다.
# 예: -3/2의 SV 정수값=-1, Python -3//2=-2다. 평균/분산/GELU 보간 규칙을 맞춘다.
def trunc_div(numerator: int, denominator: int) -> int:
    return (abs(numerator) // denominator) * (-1 if numerator < 0 else 1)


# Q8.8 A[M,K]*B[K,N]->[M,N]. SV VMM/shared MAC 내적을 독립 Python 정수로 계산한다.
# a*b는 Q16.16이므로 모든 항을 넓게 합산한 끝에 >>8/포화한다. 중간 항별 절삭은 다른 결과다.
def qmat(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    return [[sat16(sum(a[r][k] * b[k][c] for k in range(len(b))) >> 8)
             for c in range(len(b[0]))] for r in range(len(a))]


# qmat의 >>8/포화 뒤 channel별 Q8.8 bias를 포화 덧셈한다. SV linear_bias/sat_add16 경계와 같다.
# 학습 bias는 linear QKV/Wo/FFN/LM에 있고 QK/probability*V에 적용하지 않는다.
def qmat_bias(a: list[list[int]], b: list[list[int]], bias: list[int] | None = None) -> list[list[int]]:
    """Q8.8 linear를 계산하고 선택적인 Q8.8 bias를 포화 덧셈한다."""
    result = qmat(a, b)
    if bias is None:
        return result
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if len(bias) != len(result[0]):
        raise ValueError("linear bias 길이가 출력 channel 수와 다릅니다.")
    return [[sat16(value + bias[channel]) for channel, value in enumerate(row)]
            for row in result]


# QK 내적->>>8/첫 포화->scale 곱->>>8/둘째 포화를 보존한다. SV OP_QK/scale_scores와 같다.
# 큰 입력에서 포화를 scale 뒤로 미루면 같은 회로가 아니므로 두 경계를 명시한다.
def attention_score_q8(query: list[int], key: list[int], score_scale_q8: int) -> int:
    """한 head의 Q·K 내적과 1/sqrt(head_dim) 배율을 RTL 순서로 계산한다.

    곱의 raw 표현은 Q16.16이므로 넓게 합산한 다음 >>8을 수행한다.
    VMM의 16-bit 출력 경계에서 먼저 포화하고, 이 Q8.8 결과에 다시 Q8.8
    score_scale을 곱하여 >>8/포화한다. 포화를 배율 곱 뒤로 미루면 큰 입력에서
    서로 다른 회로가 되므로 두 경계를 보존한다. KV core의 OP_QK와 동일하다.
    """
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if len(query) != len(key) or not query:
        raise ValueError("attention Q/K head의 길이는 같고 1 이상이어야 합니다.")
    # QK를 넓게 누산/>>8/첫 포화. scale 전 16bit VMM 출력 경계를 보존한다.
    dot_q8 = sat16(sum(q * k for q, k in zip(query, key)) >> 8)
    return sat16((dot_q8 * score_scale_q8) >> 8)


# causal valid 점수를 관련성 확률 비중으로 바꾸는 정수 LUT 근사. SV Softmax PU와 같은 정의다.
# 최댓값을 빼 exp(-gap)을 0.5 간격 표로 읽고 합으로 나눠 raw256=1.0 스케일로 만든다.
# LUT 마지막 값은2이며 정수 절삭으로 확률 합이256보다 작을 수 있다. torch.softmax와 bit 동일한 실수 연산은 아니다.
def softmax_q8(logits: list[int], valid: list[bool]) -> list[int]:
    # causal mask가 허용한 점수만 포함. 미래/padding은 확률에 기여하지 않는다.
    selected = [value for value, keep in zip(logits, valid) if keep]
    if not selected:
        return [0] * len(logits)
    # 최대 score를 빼 exp overflow를 줄인다. 상대 score 순서는 유지된다.
    maximum = max(selected)
    exponents: list[int] = []
    for value, keep in zip(logits, valid):
        if not keep:
            exponents.append(0)
        else:
            # score-maximum. 최대항0/나머지음수이며 exp(-gap) LUT를 선택한다.
            delta = value - maximum
            index = (-delta + 64) // 128
            exponents.append((256, 155, 94, 57, 35, 21, 13, 8, 5, 3, 2)[min(index, 10)])
    total = sum(exponents)
    return [value * 256 // total if keep and total else 0
            for value, keep in zip(exponents, valid)]


# token 한 개의 채널 평균/분산으로 정규화하는 정수 LayerNorm. SV PU trunc_div/isqrt와 같은 규칙이다.
# variance raw+1은 epsilon1/256, 16777216=256**3은 역표준편차 scale을 맞추는 상수다.
def layernorm_q8(values: list[int]) -> list[int]:
    # channel raw 평균. SV signed 절삭을 trunc_div로 맞춘다.
    mean = trunc_div(sum(values), len(values))
    # channel-평균. token 채널 중심을0으로 옮기고 분산 계산에 사용한다.
    centered = [value - mean for value in values]
    # centered raw 제곱합. Q8.8 제곱은 Q16.16이므로 다음에 scale을 맞춘다.
    square_sum = sum(value * value for value in centered)
    # 제곱 평균 /256의 Q8.8 분산에 epsilon raw1=1/256을 더한다.
    variance_q8 = trunc_div(trunc_div(square_sum, len(values)), 256) + 1
    # isqrt/나눗셈의 정수 역표준편차 근사. channel에 곱한 뒤 >>8한다.
    inv_std = 4096 if variance_q8 <= 1 else math.isqrt(16777216 // variance_q8)
    return [sat16((value * inv_std) >> 8) for value in centered]


# LayerNorm 뒤 gamma 곱/>>8/포화, beta 덧셈/포화를 순서대로 수행한다.
# gamma256=배율1,beta0=이동없음. SV S_NORM1/2 ENABLE_NORM_AFFINE과 대응한다.
def layernorm_q8_affine(values: list[int], gamma: list[int] | None = None,
                        beta: list[int] | None = None) -> list[int]:
    """LayerNorm 결과에 learned gamma/beta를 Q8.8 순서로 적용한다."""
    normalized = layernorm_q8(values)
    if gamma is None and beta is None:
        return normalized
    gamma = [256] * len(values) if gamma is None else gamma
    beta = [0] * len(values) if beta is None else beta
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if len(gamma) != len(values) or len(beta) != len(values):
        raise ValueError("LayerNorm gamma/beta 폭이 hidden 폭과 다릅니다.")
    return [sat16(sat16((normalized[index] * gamma[index]) >> 8) + beta[index])
            for index in range(len(values))]


# FFN 비선형 GELU의 고정 LUT/정수 보간. -8..8의 0.25 간격=raw64 표를 사용한다.
# 범위밖 음수는0/양수는입력. SV GELU PU와 같지만 PyTorch F.gelu 실수 전체와 bit 동일하지는 않다.
def gelu_q8(value: int) -> int:
    """GELU(x)=x*Phi(x)의 signed Q8.8 LUT 근사.

    -8..8 구간에서 0.25 간격으로 실수 GELU를 Q8.8 반올림한 65개 표를
    만들고 이웃 값 사이를 정수 선형보간한다. 범위 밖 음수는 0, 양수는 입력을
    반환한다. 같은 표/보간을 SystemVerilog PU가 사용한다.
    """
    table = GELU_LUT_Q8
    if value <= -2048:
        return 0
    if value >= 2048:
        return sat16(value)
    offset = value + 2048
    index = offset // 64
    remainder = offset % 64
    difference = table[index + 1] - table[index]
    return sat16(table[index] + trunc_div(difference * remainder, 64))


# x=-8,-7.75,...,7.75,8.0의 GELU 출력 Q8.8. 고정 상수이므로 Python/RTL이
# 라이브러리의 실수 erf 구현이나 플랫폼 부동소수점 차이에 의존하지 않는다.
GELU_LUT_Q8 = (
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    -1, -2, -4, -7, -12, -18, -26, -34, -41, -44, -39, -26, 0, 38, 89,
    148, 215, 286, 358, 430, 500, 569, 636, 702, 767, 832, 896, 960, 1024,
    1088, 1152, 1216, 1280, 1344, 1408, 1472, 1536, 1600, 1664, 1728, 1792,
    1856, 1920, 1984, 2048,
)


# JSON config/vocab/weight를 복원한다. 저장한 학습 숫자를 읽는 것이며 새로운 학습을 수행하지 않는다.
def load_checkpoint(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


# 모든 context 위치를 causal decoder로 계산해 (hidden 행렬,logit 행렬)을 반환한다.
# embedding/position->각 layer QKV/head/FFN->LM 순서. 첫 생성 문자는 prompt 마지막 행 logits[-1]에서 선택한다.
def forward_q88(model: dict[str, Any], token_ids: list[int]) -> tuple[list[list[int]], list[list[int]]]:
    # model config의 shape/수치 규칙. config와 weight가 같아야 같은 모델이다.
    cfg = model["config"]
    # embedding/layer/LM raw 숫자. inference 중 새 학습을 하지 않는다.
    weights = model["weights"]
    d = int(cfg["d_model"])
    heads = int(cfg["heads"])
    # D/H. Q/K/V slice 길이 및 QK 내적 축이다.
    head_dim = d // heads
    if len(token_ids) > int(cfg["context_length"]):
        token_ids = token_ids[-int(cfg["context_length"]):]
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if not token_ids:
        raise ValueError("최소 한 개의 입력 token이 필요합니다.")

    state: list[list[int]] = []
    for position, token_id in enumerate(token_ids):
        # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
        if token_id < 0 or token_id >= len(weights["token_embedding"]):
            raise ValueError(f"잘못된 token ID: {token_id}")
        state.append([
            sat16(weights["token_embedding"][token_id][channel] +
                  weights["position_embedding"][position][channel])
            for channel in range(d)
        ])

    # 1/sqrt(head_dim)의 Q8.8 배율. raw128=0.5이며 clock 주기가 아니다.
    score_scale = int(cfg["score_scale_q8"])
    # head는 채널별 관점,layer는 직렬 block 반복. 올바른 slice/층 가중치를 선택해 처리한다.
    for layer in weights["layers"]:
        # Query projection. 찾을 특징이며 K와의 내적으로 관련성을 계산한다.
        q = qmat_bias(state, layer["wq"], layer.get("bq"))
        # Key projection. 검색 대상 특징이며 여러 query와 비교할 수 있다.
        k = qmat_bias(state, layer["wk"], layer.get("bk"))
        # Value projection. attention 확률로 가중 합산할 내용이다.
        v = qmat_bias(state, layer["wv"], layer.get("bv"))
        # 각 token/head의 가중합 내용을 hidden 채널에 연결할 공간.
        context_rows = [[0] * d for _ in token_ids]
        # head는 채널별 관점,layer는 직렬 block 반복. 올바른 slice/층 가중치를 선택해 처리한다.
        for head in range(heads):
            start = head * head_dim
            stop = start + head_dim
            qh = [row[start:stop] for row in q]
            kh = [row[start:stop] for row in k]
            vh = [row[start:stop] for row in v]
            # query별 key 축 비중. causal 미래 위치는0으로 제외한다.
            probabilities: list[list[int]] = []
            for row in range(len(token_ids)):
                scores = []
                for other in range(len(token_ids)):
                    scores.append(attention_score_q8(qh[row], kh[other], score_scale))
                probabilities.append(softmax_q8(scores, [other <= row for other in range(len(token_ids))]))
            contexts = qmat(probabilities, vh)
            for row in range(len(token_ids)):
                context_rows[row][start:stop] = contexts[row]

        # context*Wo. 여러 head의 내용을 섞어 residual에 더한다.
        attention = qmat_bias(context_rows, layer["wo"], layer.get("bo"))
        # 입력+attention 포화 덧셈. attention 전 정보도 보존한다.
        residual1 = [[sat16(state[row][ch] + attention[row][ch]) for ch in range(d)]
                     for row in range(len(token_ids))]
        # 첫 residual Norm/선택 affine. FFN 입력/둘째 residual 기본 특징이다.
        norm1 = [layernorm_q8_affine(row, layer.get("ln1_gamma"), layer.get("ln1_beta"))
                 for row in residual1]
        # FFN 확장/activation 특징. W1 선형 뒤 비선형 ReLU/GELU를 적용한다.
        ff1 = qmat_bias(norm1, layer["w1"], layer.get("b1"))
        if cfg.get("activation", "relu") == "gelu":
            # 활성화한 FFN 특징. W2가 hidden 원래 폭으로 축소한다.
            activated = [[gelu_q8(value) for value in row] for row in ff1]
        else:
            # 활성화한 FFN 특징. W2가 hidden 원래 폭으로 축소한다.
            activated = [[max(0, value) for value in row] for row in ff1]
        # FFN 축소 linear 결과. norm1과 residual로 더한다.
        ff2 = qmat_bias(activated, layer["w2"], layer.get("b2"))
        # norm1+ff2 포화 덧셈. 뒤 Norm이 block 출력을 만든다.
        residual2 = [[sat16(norm1[row][ch] + ff2[row][ch]) for ch in range(d)]
                     for row in range(len(token_ids))]
        state = [layernorm_q8_affine(row, layer.get("ln2_gamma"), layer.get("ln2_beta"))
                 for row in residual2]

    # 어휘 후보 점수. 자체는 확률이 아니며 argmax/sampling 입력이다.
    logits = qmat_bias(state, weights["lm_head"], weights.get("lm_bias"))
    return state, logits


# 층마다 과거 keys/values 목록과 position0을 만든다. SV reset/token_count 초기화에 대응한다.
# 층마다 입력 hidden이 달라 K/V도 달라지므로 같은 token의 cache를 layer별로 구분한다.
def new_kv_cache(model: dict[str, Any]) -> dict[str, Any]:
    """새 token-by-token 추론용 K/V cache를 만든다.

    각 decoder layer에는 그 layer의 입력 hidden에서 나온 key와 value를 따로
    저장한다. 다음 token은 과거 token의 K/V를 다시 계산하지 않고 이 배열을
    attention에 재사용한다. 값은 RTL과 같은 signed Q8.8 raw integer다.
    """
    layer_count = len(model["weights"]["layers"])
    return {
        "position": 0,
        "layers": [{"keys": [], "values": []} for _ in range(layer_count)],
    }


# 새 token Q/K/V만 계산해 cache에 K/V를 추가하고 과거 key/value에 attention을 적용한다.
# SV transformer_gpt_kvcache_seq의 단일-token FSM과 대응한다. 마지막 vocabulary score vector만 반환한다.
def forward_q88_step(
    model: dict[str, Any], token_id: int, cache: dict[str, Any]
) -> list[int]:
    """토큰 하나를 처리하고 마지막 위치 vocabulary logits를 반환한다.

    KV cache는 호출자가 소유하며 이 함수가 현재 token의 layer별 key/value를
    추가한다. 전체 context forward_q88과 각 위치의 정수 계산 순서는 같다.
    context_length에 도달하면 호출자는 아래 prefill_q88로 창을 다시 채워야
    한다. 학습된 absolute position embedding을 0부터 다시 매기는 기존 모델
    규칙을 지키기 위해서다.
    """
    # model config의 shape/수치 규칙. config와 weight가 같아야 같은 모델이다.
    cfg = model["config"]
    # embedding/layer/LM raw 숫자. inference 중 새 학습을 하지 않는다.
    weights = model["weights"]
    d_model = int(cfg["d_model"])
    heads = int(cfg["heads"])
    # D/H. Q/K/V slice 길이 및 QK 내적 축이다.
    head_dim = d_model // heads
    position = int(cache["position"])
    context_length = int(cfg["context_length"])
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if position >= context_length:
        raise ValueError("KV cache가 context_length에 도달했습니다. 창을 재구성하세요.")
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if len(cache["layers"]) != len(weights["layers"]):
        raise ValueError("KV cache의 decoder layer 수가 checkpoint와 다릅니다.")
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if token_id < 0 or token_id >= len(weights["token_embedding"]):
        raise ValueError(f"잘못된 token ID: {token_id}")
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if len(weights["position_embedding"]) < context_length:
        raise ValueError("position embedding이 설정된 context 길이보다 짧습니다.")

    state = [sat16(weights["token_embedding"][token_id][channel] +
                   weights["position_embedding"][position][channel])
             for channel in range(d_model)]
    # 1/sqrt(head_dim)의 Q8.8 배율. raw128=0.5이며 clock 주기가 아니다.
    score_scale = int(cfg["score_scale_q8"])

    for layer_index, layer in enumerate(weights["layers"]):
        layer_cache = cache["layers"][layer_index]
        # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
        if len(layer_cache["keys"]) != position or len(layer_cache["values"]) != position:
            raise ValueError("KV cache token 개수가 layer 위치와 일치하지 않습니다.")

        # 새 token의 Q/K/V는 한 행 행렬곱으로 계산한다. 과거 K/V는 cache에
        # 이미 있으므로 재계산하지 않는다.
        # Query projection. 찾을 특징이며 K와의 내적으로 관련성을 계산한다.
        q = qmat_bias([state], layer["wq"], layer.get("bq"))[0]
        key = qmat_bias([state], layer["wk"], layer.get("bk"))[0]
        value = qmat_bias([state], layer["wv"], layer.get("bv"))[0]
        layer_cache["keys"].append(key)
        layer_cache["values"].append(value)

        all_keys = layer_cache["keys"]
        all_values = layer_cache["values"]
        # 현재 token의 head별 문맥을 channel 축으로 연결한다.
        context_row = [0] * d_model
        # head는 채널별 관점,layer는 직렬 block 반복. 올바른 slice/층 가중치를 선택해 처리한다.
        for head in range(heads):
            start = head * head_dim
            stop = start + head_dim
            scores = []
            for cached_key in all_keys:
                scores.append(attention_score_q8(q[start:stop], cached_key[start:stop], score_scale))
            # attention 비중. 학습은 실수 Softmax, 정수 모델은 Q8.8 LUT 근사다.
            probability = softmax_q8(scores, [True] * len(scores))
            value_head = [row[start:stop] for row in all_values]
            context_head = qmat([probability], value_head)[0]
            context_row[start:stop] = context_head

        # context*Wo. 여러 head의 내용을 섞어 residual에 더한다.
        attention = qmat_bias([context_row], layer["wo"], layer.get("bo"))[0]
        # 입력+attention 포화 덧셈. attention 전 정보도 보존한다.
        residual1 = [sat16(state[channel] + attention[channel])
                     for channel in range(d_model)]
        # 첫 residual Norm/선택 affine. FFN 입력/둘째 residual 기본 특징이다.
        norm1 = layernorm_q8_affine(residual1, layer.get("ln1_gamma"), layer.get("ln1_beta"))
        # FFN 확장/activation 특징. W1 선형 뒤 비선형 ReLU/GELU를 적용한다.
        ff1 = qmat_bias([norm1], layer["w1"], layer.get("b1"))[0]
        if cfg.get("activation", "relu") == "gelu":
            # 활성화한 FFN 특징. W2가 hidden 원래 폭으로 축소한다.
            activated = [gelu_q8(value) for value in ff1]
        else:
            # 활성화한 FFN 특징. W2가 hidden 원래 폭으로 축소한다.
            activated = [max(0, value) for value in ff1]
        # FFN 축소 linear 결과. norm1과 residual로 더한다.
        ff2 = qmat_bias([activated], layer["w2"], layer.get("b2"))[0]
        # norm1+ff2 포화 덧셈. 뒤 Norm이 block 출력을 만든다.
        residual2 = [sat16(norm1[channel] + ff2[channel])
                     for channel in range(d_model)]
        state = layernorm_q8_affine(residual2, layer.get("ln2_gamma"), layer.get("ln2_beta"))

    cache["position"] = position + 1
    return qmat_bias([state], weights["lm_head"], weights.get("lm_bias"))[0]


# prompt ID를 순서대로 step에 넣어 cache를 채우고 마지막 score를 반환한다.
# 문맥 상한을 넘으면 마지막 창을 남겨 position0부터 다시 매긴다.
def prefill_q88(
    model: dict[str, Any], token_ids: list[int]
) -> tuple[list[int], dict[str, Any]]:
    """prompt의 K/V를 cache에 쌓고 마지막 token의 logits를 반환한다."""
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if not token_ids:
        raise ValueError("최소 한 개의 입력 token이 필요합니다.")
    context_length = int(model["config"]["context_length"])
    window = token_ids[-context_length:]
    cache = new_kv_cache(model)
    # 어휘 후보 점수. 자체는 확률이 아니며 argmax/sampling 입력이다.
    logits: list[int] = []
    # prompt ID를 순서대로 넣어 absolute position과 각 층 K/V를 채운다.
    for token_id in window:
        # 어휘 후보 점수. 자체는 확률이 아니며 argmax/sampling 입력이다.
        logits = forward_q88_step(model, token_id, cache)
    return logits, cache


# 문자->ID 후 full-context score/다음 ID 선택/재입력을 반복한다.
# temperature<=0은 greedy, 양수는 top-k exp 확률 sampling이다. seed를 고정하고 vocab[id]로 문자열을 복원한다.
def generate_q88(model: dict[str, Any], prompt: str, max_new_tokens: int = 120,
                 temperature: float = 0.8, top_k: int = 8, seed: int = 20261003) -> str:
    # ID 순서 문자 목록. score index/선택 ID와 출력 문자의 대응표다.
    vocab = model["vocab"]
    # 문자->ID 사전. FPGA에는 문자열 대신 이 정수 ID를 보낸다.
    encode = {char: index for index, char in enumerate(vocab)}
    unknown = model.get("unknown_token_id", 0)
    ids = [encode.get(char, unknown) for char in prompt]
    rng = random.Random(seed)
    output = list(ids)
    for _ in range(max_new_tokens):
        _, logits = forward_q88(model, output)
        last = logits[-1]
        # score 내림차순 top-k ID. 같은 값은 안정 순서로 낮은 ID가 먼저 온다.
        ranked = sorted(range(len(last)), key=lambda index: last[index], reverse=True)[:max(1, top_k)]
        # 최대 score를 빼 exp overflow를 줄인다. 상대 score 순서는 유지된다.
        maximum = max(last[index] for index in ranked)
        if temperature <= 0:
            # 마지막 score로 고른 다음 문자 번호. vocab[next_id]가 실제 문자다.
            next_id = ranked[0]
        else:
            scores = [math.exp((last[index] - maximum) / (256.0 * temperature)) for index in ranked]
            # seed sampling 추첨 위치. 누적 exp 비중 구간에서 다음 후보를 선택한다.
            draw = rng.random() * sum(scores)
            # 마지막 score로 고른 다음 문자 번호. vocab[next_id]가 실제 문자다.
            next_id = ranked[-1]
            for index, score in zip(ranked, scores):
                draw -= score
                if draw <= 0:
                    # 마지막 score로 고른 다음 문자 번호. vocab[next_id]가 실제 문자다.
                    next_id = index
                    break
        output.append(next_id)
    return "".join(vocab[index] for index in output)


# prefill 뒤 과거 K/V를 재사용하는 같은 sampling 생성 경로다.
# context 초과 시 absolute position 규칙을 맞추려고 창을 다시 prefill한다. 경계 뒤 무제한 cache 유지가 아니다.
def generate_q88_cached(model: dict[str, Any], prompt: str, max_new_tokens: int = 120,
                        temperature: float = 0.8, top_k: int = 8,
                        seed: int = 20261003) -> str:
    """K/V cache를 재사용해 기존 정수 generator와 같은 규칙으로 생성한다.

    context_length 이후에는 모델의 기존 슬라이딩 window 의미(가장 오래된
    token 제거 후 position 0부터 재부여)를 유지하기 위해 cache를 한 번
    비우고 남은 창을 다시 prefill한다. 일반 길이에서는 과거 K/V를 재사용한다.
    """
    # ID 순서 문자 목록. score index/선택 ID와 출력 문자의 대응표다.
    vocab = model["vocab"]
    # 문자->ID 사전. FPGA에는 문자열 대신 이 정수 ID를 보낸다.
    encode = {char: index for index, char in enumerate(vocab)}
    unknown = model.get("unknown_token_id", 0)
    output = [encode.get(char, unknown) for char in prompt]
    # 입력/설정/oracle 조건 위반은 오류로 중단하여 잘못된 값을 정상 결과로 기록하지 않는다.
    if not output:
        raise ValueError("prompt는 비어 있을 수 없습니다.")
    context_length = int(model["config"]["context_length"])
    window = output[-context_length:]
    logits, cache = prefill_q88(model, window)
    rng = random.Random(seed)

    # 한 번에 다음 token 하나를 고르고 입력에 붙이는 autoregressive 반복이다.
    for generated_index in range(max_new_tokens):
        # score 내림차순 top-k ID. 같은 값은 안정 순서로 낮은 ID가 먼저 온다.
        ranked = sorted(range(len(logits)), key=lambda index: logits[index], reverse=True)[:max(1, top_k)]
        # 최대 score를 빼 exp overflow를 줄인다. 상대 score 순서는 유지된다.
        maximum = max(logits[index] for index in ranked)
        if temperature <= 0:
            # 마지막 score로 고른 다음 문자 번호. vocab[next_id]가 실제 문자다.
            next_id = ranked[0]
        else:
            scores = [math.exp((logits[index] - maximum) / (256.0 * temperature))
                      for index in ranked]
            # seed sampling 추첨 위치. 누적 exp 비중 구간에서 다음 후보를 선택한다.
            draw = rng.random() * sum(scores)
            # 마지막 score로 고른 다음 문자 번호. vocab[next_id]가 실제 문자다.
            next_id = ranked[-1]
            for index, score in zip(ranked, scores):
                draw -= score
                if draw <= 0:
                    # 마지막 score로 고른 다음 문자 번호. vocab[next_id]가 실제 문자다.
                    next_id = index
                    break
        output.append(next_id)
        if generated_index + 1 == max_new_tokens:
            break

        window.append(next_id)
        if len(window) > context_length:
            # 다음 token 계산부터 오래된 token 하나를 떨군다. 기존 full
            # forward는 길이가 context를 넘으면 맨 앞을 잘라 position을 0부터
            # 다시 부여하므로, 경계에서 cache를 새 창으로 만들어야 정확하다.
            window = window[-context_length:]
            logits, cache = prefill_q88(model, window)
        else:
            # 어휘 후보 점수. 자체는 확률이 아니며 argmax/sampling 입력이다.
            logits = forward_q88_step(model, next_id, cache)
    return "".join(vocab[index] for index in output)


# raw 정수를 row-major flatten/value&0xffff로 16진수 한 word/줄 export한다.
# raw -256은 ff00이고 SV $signed는 같은 two's-complement bit를 -256으로 읽는다.
def write_mem_files(model: dict[str, Any], output_dir: Path) -> None:
    """Q8.8 raw 값을 16비트 hex, row-major 한 단어/줄로 내보낸다."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # 중첩 row/layer list를 row-major 원소로 펼친다. SV word0은 최하위16bit다.
    def flatten(value: Any) -> list[int]:
        if isinstance(value, list):
            if value and isinstance(value[0], list):
                return [item for row in value for item in row]
            return value
        raise TypeError("mem 대상 가중치는 list여야 합니다.")

    objects: dict[str, Any] = {
        "token_embedding": model["weights"]["token_embedding"],
        "position_embedding": model["weights"]["position_embedding"],
        "lm_head": model["weights"]["lm_head"],
    }
    if "lm_bias" in model["weights"]:
        objects["lm_bias"] = model["weights"]["lm_bias"]
    for layer_id, layer in enumerate(model["weights"]["layers"]):
        for name, value in layer.items():
            objects[f"layer_{layer_id}_{name}"] = value
    for name, matrix in objects.items():
        words = flatten(matrix)
        (output_dir / f"{name}.mem").write_text(
            "".join(f"{value & 0xffff:04x}\n" for value in words), encoding="ascii"
        )


# 직접 실행할 때만 진입점을 실행한다. import한 다른 파일은 여기 함수/정의를 호출해 사용한다.
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    # 정수 inference JSON positional 경로. config/vocab/weight를 함께 읽는다.
    parser.add_argument("checkpoint", type=Path)
    # 입력 문자열->ID. prompt 마지막 score가 첫 생성 token을 예측한다.
    parser.add_argument("--prompt", default="ROMEO:")
    # generation에서는 새 token 수, DRAM 모델에서는 context token 수. 파일 목적에 따라 의미가 다르다.
    parser.add_argument("--tokens", type=int, default=120)
    # sampling 확률 평탄함. <=0 greedy, 양수에서 낮을수록 최고 score에 집중한다.
    parser.add_argument("--temperature", type=float, default=0.8)
    # 최고 score 후보 k개만 sampling. vocabulary 저장 크기를 변경하지 않는다.
    parser.add_argument("--top-k", type=int, default=8)
    # 입력 표본/random 초기화/sampling 재현 seed. 비교의 무작위 조건을 맞춘다.
    parser.add_argument("--seed", type=int, default=20261003)
    # raw Q8.8 hex 이미지 출력 폴더. SV $readmemh/ROM에 제공한다.
    parser.add_argument("--mem-dir", type=Path)
    # Python layer K/V 재사용 생성 mode. FPGA board 실행 mode와 구분한다.
    parser.add_argument("--cached", action="store_true",
                        help="decoder layer별 K/V cache를 재사용하는 Q8.8 generation")
    args = parser.parse_args()
    checkpoint = load_checkpoint(args.checkpoint)
    generator = generate_q88_cached if args.cached else generate_q88
    print(generator(checkpoint, args.prompt, args.tokens, args.temperature, args.top_k, args.seed))
    if args.mem_dir:
        write_mem_files(checkpoint, args.mem_dir)
