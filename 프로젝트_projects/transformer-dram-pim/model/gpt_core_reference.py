# 여러 head/층의 소형 decoder 정수 oracle. sample_*는 시험 fixture이며 학습 checkpoint가 아니다.
# RTL decoder_mha/decoder_stack과 같은 흐름이며 hidden 출력 자체는 문자가 아닌 내부 특징이다.
"""Multi-head, multi-layer decoder core의 독립 Q8.8 기준 모델.

이 파일은 RTL 연산 순서를 Python 정수로 다시 구현한다. 테스트는 각 head의
causal Softmax, 문맥 결합, FFN, LayerNorm과 여러 층 연결을 RTL 출력과 비교한다.
언어 모델 학습용 PyTorch 모델과는 별개인 비트 기준(reference) 구현이다.
"""

from __future__ import annotations

from model.reference import layernorm_q8, qmat, sat16, softmax_q8

TOKENS = 3
D_MODEL = 4
HEADS = 2
HEAD_DIM = D_MODEL // HEADS
D_FF = 8
LAYERS = 2
SCORE_SCALE_Q8 = 181  # round(256 / sqrt(2))


# RTL 시험과 같은 결정론적 층별 가중치를 만든다. corpus 학습 결과가 아닌 test fixture다.
def sample_weights() -> list[dict[str, list[list[int]]]]:
    """RTL 테스트벤치와 동일한 재현 가능한 2층 가중치 행렬을 만든다."""
    layers: list[dict[str, list[list[int]]]] = []
    # head는 채널별 관점,layer는 직렬 block 반복. 올바른 slice/층 가중치를 선택해 처리한다.
    for layer in range(LAYERS):
        wq, wk, wv, wo = [], [], [], []
        for r in range(D_MODEL):
            qrow, krow, vrow, orow = [], [], [], []
            for c in range(D_MODEL):
                qrow.append(240 + 4 * layer if r == c else ((r * 13 + c * 7 + layer * 3) % 17) - 8)
                krow.append(200 - 3 * layer if r == c else ((r * 5 + c * 11 + layer * 2) % 13) - 6)
                vrow.append(256 if r == c else ((r * 7 + c * 3 + layer) % 11) - 5)
                orow.append(224 + 2 * layer if r == c else ((r * 9 + c * 2 + layer * 5) % 15) - 7)
            wq.append(qrow)
            wk.append(krow)
            wv.append(vrow)
            wo.append(orow)

        w1 = []
        for r in range(D_MODEL):
            w1.append([
                256 if r == c else ((r * 7 + c * 5 + layer) % 9) - 4
                for c in range(D_FF)
            ])
        w2 = []
        for r in range(D_FF):
            w2.append([
                256 if r == c else ((r * 3 + c * 11 + layer) % 7) - 3
                for c in range(D_MODEL)
            ])
        layers.append({"wq": wq, "wk": wk, "wv": wv, "wo": wo, "w1": w1, "w2": w2})
    return layers


# 소형 시험 hidden vector. raw Q8.8 숫자이고 원문 prompt token ID가 아니다.
def sample_input() -> list[list[int]]:
    """세 토큰의 hidden vector. 숫자는 Q8.8 raw integer다."""
    return [
        [64, -32, 96, 128],
        [128, 64, -64, 32],
        [-32, 128, 64, -64],
    ]


# head별 causal attention/context 연결/residual/post-norm/FFN-ReLU 한 층의 정수 계산.
# SV transformer_decoder_mha_pim_comb에 대응하며 다음 층의 입력 hidden을 만든다.
def decoder_block(
    x: list[list[int]], weights: dict[str, list[list[int]]]
) -> list[list[int]]:
    """한 블록: multi-head causal attention과 FFN을 계산한다."""
    # Query projection. 찾을 특징이며 K와의 내적으로 관련성을 계산한다.
    q = qmat(x, weights["wq"])
    # Key projection. 검색 대상 특징이며 여러 query와 비교할 수 있다.
    k = qmat(x, weights["wk"])
    # Value projection. attention 확률로 가중 합산할 내용이다.
    v = qmat(x, weights["wv"])

    # head별 context를 전체 hidden 채널로 연결한 [T,D].
    all_context_rows = [[0] * D_MODEL for _ in range(TOKENS)]
    # head는 채널별 관점,layer는 직렬 block 반복. 올바른 slice/층 가중치를 선택해 처리한다.
    for head in range(HEADS):
        start = head * HEAD_DIM
        stop = start + HEAD_DIM
        qh = [row[start:stop] for row in q]
        kh = [row[start:stop] for row in k]
        vh = [row[start:stop] for row in v]

        # query별 key 축 비중. causal 미래 위치는0으로 제외한다.
        probabilities = []
        for token in range(TOKENS):
            # RTL은 먼저 QK^T를 Q8.8로 자른 뒤 1/sqrt(head_dim)을 곱한다.
            scores = []
            for other in range(TOKENS):
                raw = sat16(sum(qh[token][d] * kh[other][d] for d in range(HEAD_DIM)) >> 8)
                # x*256의 raw 격자 값. 정수화/포화 후 /256하면 격자 위 근사 실수다.
                scaled = sat16((raw * SCORE_SCALE_Q8) >> 8)
                scores.append(scaled)
            probabilities.append(softmax_q8(scores, [other <= token for other in range(TOKENS)]))

        context = qmat(probabilities, vh)
        for token in range(TOKENS):
            all_context_rows[token][start:stop] = context[token]

    # context*Wo. 여러 head의 내용을 섞어 residual에 더한다.
    attention = qmat(all_context_rows, weights["wo"])
    # 입력+attention 포화 덧셈. attention 전 정보도 보존한다.
    residual1 = [
        [sat16(x[token][d] + attention[token][d]) for d in range(D_MODEL)]
        for token in range(TOKENS)
    ]
    # 첫 residual Norm/선택 affine. FFN 입력/둘째 residual 기본 특징이다.
    norm1 = [layernorm_q8(row) for row in residual1]
    # FFN 확장/activation 특징. W1 선형 뒤 비선형 ReLU/GELU를 적용한다.
    ff1 = qmat(norm1, weights["w1"])
    relu = [[max(0, value) for value in row] for row in ff1]
    # FFN 축소 linear 결과. norm1과 residual로 더한다.
    ff2 = qmat(relu, weights["w2"])
    # norm1+ff2 포화 덧셈. 뒤 Norm이 block 출력을 만든다.
    residual2 = [
        [sat16(norm1[token][d] + ff2[token][d]) for d in range(D_MODEL)]
        for token in range(TOKENS)
    ]
    return [layernorm_q8(row) for row in residual2]


# block 결과를 다음 block 입력으로 연결한다. SV stack generate와 같은 층 흐름이다.
def decoder_stack(x: list[list[int]] | None = None) -> list[list[int]]:
    """각 block 결과를 다음 block 입력으로 사용하는 2-layer decoder stack."""
    state = sample_input() if x is None else [row.copy() for row in x]
    for weights in sample_weights():
        state = decoder_block(state, weights)
    return state


# 직접 실행할 때만 진입점을 실행한다. import한 다른 파일은 여기 함수/정의를 호출해 사용한다.
if __name__ == "__main__":
    for token, row in enumerate(decoder_stack()):
        print(f"OUTPUT token={token} " + " ".join(map(str, row)))
