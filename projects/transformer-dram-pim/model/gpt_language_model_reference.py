# ID->embedding+position->decoder->vocabulary logits의 소형 oracle.
# RTL comb/seq 언어 모델과 대응한다. 다음 ID를 골라 vocab[id]로 바꾸어야 출력 문자가 된다.
"""토큰 임베딩부터 어휘 logits까지의 Q8.8 GPT-style 기준 모델."""

from __future__ import annotations

from model.gpt_core_reference import D_MODEL, TOKENS, decoder_stack, sample_weights
from model.reference import qmat, sat16

VOCAB_SIZE = 8
TOKEN_IDS = [1, 4, 2]


# 소형 TB와 동일 embedding/position/LM head 표. ID->logit 경로를 독립 검증한다.
def sample_tables() -> tuple[list[list[int]], list[list[int]], list[list[int]]]:
    """RTL 테스트벤치와 똑같은 token/position table과 vocab head를 반환한다."""
    token_embedding = [
        [((vocab * 7 + channel * 11) % 65) - 32 for channel in range(D_MODEL)]
        for vocab in range(VOCAB_SIZE)
    ]
    position_embedding = [
        [((token * 5 + channel * 3) % 21) - 10 for channel in range(D_MODEL)]
        for token in range(TOKENS)
    ]
    # [hidden channel][vocabulary index] 방향의 출력 projection weight.
    lm_head = [
        [((channel * 3 + vocab * 7) % 31) - 15 for vocab in range(VOCAB_SIZE)]
        for channel in range(D_MODEL)
    ]
    return token_embedding, position_embedding, lm_head


# ID lookup/위치 덧셈/decoder/LM head로 다음 후보 점수를 만든다. 소형 RTL oracle다.
def language_model_logits(token_ids: list[int] | None = None) -> list[list[int]]:
    ids = TOKEN_IDS if token_ids is None else token_ids
    token_embedding, position_embedding, lm_head = sample_tables()
    embedded = [
        [sat16(token_embedding[ids[token]][channel] + position_embedding[token][channel])
         for channel in range(D_MODEL)]
        for token in range(TOKENS)
    ]
    hidden = decoder_stack(embedded)
    return qmat(hidden, lm_head)


# 직접 실행할 때만 진입점을 실행한다. import한 다른 파일은 여기 함수/정의를 호출해 사용한다.
if __name__ == "__main__":
    for token, row in enumerate(language_model_logits()):
        print(f"LOGITS token={token} " + " ".join(map(str, row)))
