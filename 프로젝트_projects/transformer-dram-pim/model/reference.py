# 최초 단일-head Transformer의 독립 정수 정답(reference/oracle) 계산기다.
# rtl/transformer_decoder_pim_comb.sv 및 PU의 수학에 대응하며 학습/보드 통신을 실행하지 않는다.
"""SystemVerilog Q8.8 경로를 별도로 계산해 비교하는 정수 기준 모델."""

from __future__ import annotations

from math import isqrt

TOKENS = 4
D_MODEL = 4
D_FF = 8
EXP_LUT_Q8 = (256, 155, 94, 57, 35, 21, 13, 8, 5, 3, 2)


# signed16 -32768..32767 포화. wrap으로 부호가 뒤집히는 것을 막는 SV sat16과 같다.
# Q8.8 실제값 범위는 -128..127.99609375이며 raw/256으로 읽는다.
def sat16(value: int) -> int:
    return max(-32768, min(32767, value))


# SV signed 나눗셈의 0 방향 절삭. Python //는 음수에서 아래 방향이므로 직접 쓰면 다르다.
# 예: -3/2의 SV 정수값=-1, Python -3//2=-2다. 평균/분산/GELU 보간 규칙을 맞춘다.
def trunc_div(numerator: int, denominator: int) -> int:
    """SystemVerilog의 0 방향 절삭 규칙에 맞춰 signed 정수 나눗셈을 수행한다."""
    return abs(numerator) // denominator * (-1 if numerator < 0 else 1)


# Q8.8 A[M,K]*B[K,N]->[M,N]. SV VMM/shared MAC 내적을 독립 Python 정수로 계산한다.
# a*b는 Q16.16이므로 모든 항을 넓게 합산한 끝에 >>8/포화한다. 중간 항별 절삭은 다른 결과다.
def qmat(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    return [
        [sat16(sum(a[r][k] * b[k][c] for k in range(len(b))) >> 8) for c in range(len(b[0]))]
        for r in range(len(a))
    ]


# causal valid 점수를 관련성 확률 비중으로 바꾸는 정수 LUT 근사. SV Softmax PU와 같은 정의다.
# 최댓값을 빼 exp(-gap)을 0.5 간격 표로 읽고 합으로 나눠 raw256=1.0 스케일로 만든다.
# LUT 마지막 값은2이며 정수 절삭으로 확률 합이256보다 작을 수 있다. torch.softmax와 bit 동일한 실수 연산은 아니다.
def softmax_q8(logits: list[int], valid: list[bool]) -> list[int]:
    # causal mask가 허용한 점수만 포함. 미래/padding은 확률에 기여하지 않는다.
    selected = [value for value, is_valid in zip(logits, valid) if is_valid]
    if not selected:
        return [0] * len(logits)
    # 최대 score를 빼 exp overflow를 줄인다. 상대 score 순서는 유지된다.
    maximum = max(selected)
    exponents: list[int] = []
    for value, is_valid in zip(logits, valid):
        if not is_valid:
            exponents.append(0)
            continue
        # score-maximum. 최대항0/나머지음수이며 exp(-gap) LUT를 선택한다.
        delta = value - maximum
        # RTL과 같은 0.5 간격 Softmax 조회표 구간 반올림을 적용한다.
        index = (-delta + 64) // 128
        exponents.append(EXP_LUT_Q8[min(index, len(EXP_LUT_Q8) - 1)])
    total = sum(exponents)
    return [(value * 256 // total) if is_valid and total else 0
            for value, is_valid in zip(exponents, valid)]


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
    if variance_q8 <= 1:
        inv_std_q8 = 4096
    else:
        inv_std_q8 = isqrt(16777216 // variance_q8)
    return [sat16((value * inv_std_q8) >> 8) for value in centered]


# 최초 시험 hidden/identity QKVWo/FFN 표를 만든다. identity raw256=1.0이다.
def build_inputs() -> tuple[list[list[int]], list[list[int]], list[list[int]], list[list[int]],
                            list[list[int]], list[list[int]], list[list[int]]]:
    x = [
        [64, -32, 96, 128],
        [128, 64, -64, 32],
        [-32, 128, 64, -64],
        [96, -96, 32, 64],
    ]
    identity = [[256 if r == c else 0 for c in range(D_MODEL)] for r in range(D_MODEL)]
    w1 = [[256 if c == r else 0 for c in range(D_FF)] for r in range(D_MODEL)]
    w2 = [[256 if c == r else 0 for c in range(D_MODEL)] for r in range(D_FF)]
    return x, identity, identity, identity, identity, w1, w2


# 최초 single-head attention/FFN/post-norm 정수 수학. SV decoder_pim_comb과 같은 입력으로 계산한다.
def transformer_block(x: list[list[int]], wq: list[list[int]], wk: list[list[int]],
                      wv: list[list[int]], wo: list[list[int]], w1: list[list[int]],
                      w2: list[list[int]]) -> list[list[int]]:
    # 입력 hidden state에 학습 행렬 Wq/Wk/Wv를 곱해 어텐션의 세 관점을 만든다.
    # Query projection. 찾을 특징이며 K와의 내적으로 관련성을 계산한다.
    q = qmat(x, wq)
    # Key projection. 검색 대상 특징이며 여러 query와 비교할 수 있다.
    k = qmat(x, wk)
    # Value projection. attention 확률로 가중 합산할 내용이다.
    v = qmat(x, wv)

    scores: list[list[int]] = []
    # query별 key 축 비중. causal 미래 위치는0으로 제외한다.
    probabilities: list[list[int]] = []
    for r in range(TOKENS):
        # QK^T 점수를 만들고 D=4일 때 1/sqrt(D)=1/2를 적용한다.
        # 이후 토큰을 가리는 causal mask를 Softmax 입력에 전달한다.
        # VMM의 16-bit 출력에서 먼저 포화한 뒤 Q8.8 배율128(=0.5)을 적용한다.
        # 극값에서 먼저 >>9하고 마지막에만 포화하면 RTL의 중간 경계와 달라진다.
        raw = [sat16(sum(q[r][d] * k[c][d] for d in range(D_MODEL)) >> 8)
               for c in range(TOKENS)]
        scores.append([sat16((value * 128) >> 8) for value in raw])
        probabilities.append(softmax_q8(scores[-1], [c <= r for c in range(TOKENS)]))

    # 어텐션 확률로 V를 합쳐 문맥을 만들고 출력 투영을 적용한다.
    context = qmat(probabilities, v)
    # context*Wo. 여러 head의 내용을 섞어 residual에 더한다.
    attention = qmat(context, wo)
    # 첫 residual/LN 뒤 FFN(ReLU 포함)을 계산한 다음 두 번째 residual/LN을 수행한다.
    # 입력+attention 포화 덧셈. attention 전 정보도 보존한다.
    residual1 = [[sat16(x[r][d] + attention[r][d]) for d in range(D_MODEL)]
                 for r in range(TOKENS)]
    # 첫 residual Norm/선택 affine. FFN 입력/둘째 residual 기본 특징이다.
    norm1 = [layernorm_q8(row) for row in residual1]
    # FFN 확장/activation 특징. W1 선형 뒤 비선형 ReLU/GELU를 적용한다.
    ff1 = qmat(norm1, w1)
    relu = [[max(0, value) for value in row] for row in ff1]
    # FFN 축소 linear 결과. norm1과 residual로 더한다.
    ff2 = qmat(relu, w2)
    # norm1+ff2 포화 덧셈. 뒤 Norm이 block 출력을 만든다.
    residual2 = [[sat16(norm1[r][d] + ff2[r][d]) for d in range(D_MODEL)]
                 for r in range(TOKENS)]
    return [layernorm_q8(row) for row in residual2]


# fixture를 transformer_block에 전달하여 RTL과 비교할 전체 hidden 정답을 만든다.
def reference_output() -> list[list[int]]:
    return transformer_block(*build_inputs())


# 직접 실행할 때만 진입점을 실행한다. import한 다른 파일은 여기 함수/정의를 호출해 사용한다.
if __name__ == "__main__":
    for row in reference_output():
        print(*row)
