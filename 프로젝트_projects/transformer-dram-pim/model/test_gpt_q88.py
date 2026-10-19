# cache/full-context의 모든 후보 logit 동등성과 Q8.8 PU 수치 경계를 검사한다.
# 비슷한 글이 나온다는 비교보다 엄격하지만 모든 가능한 모델/FPGA clock의 증명은 아니다.
"""KV-cache Q8.8 기준 구현의 독립 회귀 시험."""

from __future__ import annotations

import random
import unittest

from model.gpt_core_reference import sample_weights
from model.gpt_q88 import (
    attention_score_q8,
    forward_q88,
    forward_q88_step,
    gelu_q8,
    generate_q88,
    generate_q88_cached,
    layernorm_q8,
    layernorm_q8_affine,
    new_kv_cache,
    prefill_q88,
    qmat_bias,
    softmax_q8,
)


# 작고 결정론적인 2-layer fixture. Q8.8/cache 시험이 외부 학습 파일에 의존하지 않게 한다.
def tiny_checkpoint() -> dict:
    vocab_size, d_model, context, d_ff, layers = 7, 4, 4, 8, 2
    embeddings = [[((token * 17 + channel * 11) % 61) - 30
                   for channel in range(d_model)] for token in range(vocab_size)]
    positions = [[((position * 13 + channel * 7) % 29) - 14
                  for channel in range(d_model)] for position in range(context)]
    lm_head = [[((channel * 19 + token * 5) % 37) - 18
                for token in range(vocab_size)] for channel in range(d_model)]
    return {
        "config": {
            "vocab_size": vocab_size, "context_length": context,
            "d_model": d_model, "heads": 2, "head_dim": 2,
            "d_ff": d_ff, "layers": layers, "score_scale_q8": 181,
        },
        "vocab": list("abcdefg"),
        "unknown_token_id": 0,
        "weights": {
            "token_embedding": embeddings,
            "position_embedding": positions,
            "layers": sample_weights(),
            "lm_head": lm_head,
        },
    }


# cache/full-context 동등성과 Q8.8 수치 경계 assert 모음.
class KVCacheReferenceTests(unittest.TestCase):
    # 극값 QK에서 첫 포화를 scale 전에 적용하는지 검사.
    # assert 실패는 이 경계/규칙이 기대값과 달라졌다는 뜻이다. PASS 표시만으로 숫자 검사를 대체하지 않는다.
    def test_attention_score_preserves_rtl_saturation_before_scale(self) -> None:
        # 극값 내적은 먼저 +32767/-32768로 포화되어야 한다. 배율 128은 0.5이므로
        # 최종 값은 +16383/-16384다. 먼저 배율을 적용한 구현은 이 시험을 실패한다.
        self.assertEqual(attention_score_q8([32767, 32767], [32767, 32767], 128), 16383)
        self.assertEqual(attention_score_q8([32767, 32767], [-32768, -32768], 128), -16384)
        self.assertEqual(attention_score_q8([256, 128], [256, -256], 128), 64)
        with self.assertRaises(ValueError):
            attention_score_q8([256], [256, 256], 128)

    # 큰 score gap이 LUT 마지막값2로 제한되는지 검사.
    # assert 실패는 이 경계/규칙이 기대값과 달라졌다는 뜻이다. PASS 표시만으로 숫자 검사를 대체하지 않는다.
    def test_softmax_lut_saturates_to_last_entry_for_large_score_gap(self) -> None:
        # LUT 마지막 항은 2이며, 더 큰 index도 마지막 값을 반복한다.
        self.assertEqual(softmax_q8([0, -3000], [True, True]), [254, 1])

    # bias/gamma-beta 항등 affine/GELU LUT 경계 정답 검사.
    # assert 실패는 이 경계/규칙이 기대값과 달라졌다는 뜻이다. PASS 표시만으로 숫자 검사를 대체하지 않는다.
    def test_optional_gpt_linear_bias_affine_norm_and_gelu_rules(self) -> None:
        self.assertEqual(qmat_bias([[256, -256]], [[256], [256]], [10]), [[10]])
        normalized = layernorm_q8([25, -11, 50, -64])
        self.assertEqual(layernorm_q8_affine([25, -11, 50, -64], [256]*4, [0]*4), normalized)
        self.assertEqual(gelu_q8(0), 0)
        self.assertEqual(gelu_q8(-2048), 0)
        self.assertEqual(gelu_q8(-64), -26)
        self.assertEqual(gelu_q8(2048), 2048)

    # 매 prefix cache 마지막 score와 full-context 마지막 score가 exact 같은지 검사.
    # assert 실패는 이 경계/규칙이 기대값과 달라졌다는 뜻이다. PASS 표시만으로 숫자 검사를 대체하지 않는다.
    def test_cached_logits_equal_full_causal_forward_at_every_position(self) -> None:
        model = tiny_checkpoint()
        token_ids = [1, 4, 2, 6]
        cache = new_kv_cache(model)
        for end in range(1, len(token_ids) + 1):
            cached_logits = forward_q88_step(model, token_ids[end - 1], cache)
            _, full_logits = forward_q88(model, token_ids[:end])
            self.assertEqual(cached_logits, full_logits[-1], f"prefix length={end}")
            self.assertEqual(cache["position"], end)

    # bias/affine/GELU를 켜도 cache/full-context가 같은지 검사.
    # assert 실패는 이 경계/규칙이 기대값과 달라졌다는 뜻이다. PASS 표시만으로 숫자 검사를 대체하지 않는다.
    def test_cached_logits_match_full_forward_with_gpt_linear_features(self) -> None:
        model = tiny_checkpoint()
        model["config"].update({"activation": "gelu", "linear_bias": True,
                                "layernorm_affine": True})
        for index, layer in enumerate(model["weights"]["layers"]):
            layer.update({
                "bq": [index-2, 3, -1, 2], "bk": [2, -3, 1, 0],
                "bv": [1, 2, -2, 1], "bo": [-1, 1, 2, -2],
                "b1": [((channel+index) % 5)-2 for channel in range(8)],
                "b2": [index, -index, 1, -1],
                "ln1_gamma": [256, 250, 263, 248], "ln1_beta": [1, -2, 0, 3],
                "ln2_gamma": [249, 261, 255, 264], "ln2_beta": [-1, 2, -3, 0],
            })
        model["weights"]["lm_bias"] = [((index*3) % 7)-3 for index in range(7)]
        cache = new_kv_cache(model)
        for end, token_id in enumerate([2, 5, 1, 6], start=1):
            cached_logits = forward_q88_step(model, token_id, cache)
            _, full_logits = forward_q88(model, [2, 5, 1, 6][:end])
            self.assertEqual(cached_logits, full_logits[-1], f"GPT feature prefix={end}")

    # 8개 seed random 입력/weight의 모든 prefix에서 full-ops cache 동등성 검사.
    # assert 실패는 이 경계/규칙이 기대값과 달라졌다는 뜻이다. PASS 표시만으로 숫자 검사를 대체하지 않는다.
    def test_seeded_random_full_ops_weights_keep_cache_equivalent(self) -> None:
        # 단일 hand-written fixture에만 의존하지 않도록 8개 결정론적 seed의 작은
        # weight/token 조합에서 모든 prefix의 cache 결과를 full causal 기준과 비교한다.
        for seed in range(8):
            rng = random.Random(9100 + seed)
            model = tiny_checkpoint()
            model["config"].update({"activation": "gelu", "linear_bias": True,
                                    "layernorm_affine": True})
            # embedding/layer/LM raw 숫자. inference 중 새 학습을 하지 않는다.
            weights = model["weights"]
            for matrix in (weights["token_embedding"], weights["position_embedding"],
                           weights["lm_head"]):
                for row in matrix:
                    for index in range(len(row)):
                        row[index] = rng.randint(-48, 48)
            # head는 채널별 관점,layer는 직렬 block 반복. 올바른 slice/층 가중치를 선택해 처리한다.
            for layer in weights["layers"]:
                for name in ("wq", "wk", "wv", "wo", "w1", "w2"):
                    for row in layer[name]:
                        for index in range(len(row)):
                            row[index] = rng.randint(-48, 48)
                for name in ("bq", "bk", "bv", "bo", "b1", "b2", "ln1_beta", "ln2_beta"):
                    layer[name] = [rng.randint(-8, 8) for _ in range(
                        len(layer["w1"][0]) if name == "b1" else len(layer["wq"]))]
                layer["ln1_gamma"] = [rng.randint(224, 288) for _ in layer["wq"]]
                layer["ln2_gamma"] = [rng.randint(224, 288) for _ in layer["wq"]]
            weights["lm_bias"] = [rng.randint(-8, 8) for _ in model["vocab"]]
            token_ids = [rng.randrange(len(model["vocab"])) for _ in range(4)]
            cache = new_kv_cache(model)
            for end, token_id in enumerate(token_ids, start=1):
                cached_logits = forward_q88_step(model, token_id, cache)
                full_logits = forward_q88(model, token_ids[:end])[1][-1]
                self.assertEqual(cached_logits, full_logits,
                                 f"seed={seed}, prefix={end}")

    # prompt prefill/문맥 창 재구성/긴 greedy 문자열 동등성 검사.
    # assert 실패는 이 경계/규칙이 기대값과 달라졌다는 뜻이다. PASS 표시만으로 숫자 검사를 대체하지 않는다.
    def test_prefill_and_cached_generation_match_full_recomputation(self) -> None:
        model = tiny_checkpoint()
        prompt_ids = [1, 2, 3, 4, 5]
        # Python oracle 정답. 실제 RTL 숫자와 전체 비교한다.
        expected = forward_q88(model, prompt_ids[-4:])[1][-1]
        prefilled, cache = prefill_q88(model, prompt_ids)
        self.assertEqual(prefilled, expected)
        self.assertEqual(cache["position"], 4)

        prompt = "bcdef"
        full = generate_q88(model, prompt, max_new_tokens=9,
                            temperature=0, top_k=7, seed=9)
        cached = generate_q88_cached(model, prompt, max_new_tokens=9,
                                     temperature=0, top_k=7, seed=9)
        self.assertEqual(cached, full)

    # 꽉 찬 cache에 다음 token을 잘못 쓰지 않고 오류로 거절하는지 검사.
    # assert 실패는 이 경계/규칙이 기대값과 달라졌다는 뜻이다. PASS 표시만으로 숫자 검사를 대체하지 않는다.
    def test_cache_rejects_a_token_after_context_limit(self) -> None:
        model = tiny_checkpoint()
        _, cache = prefill_q88(model, [1, 2, 3, 4])
        with self.assertRaisesRegex(ValueError, "context_length"):
            forward_q88_step(model, 5, cache)


# 직접 실행할 때만 진입점을 실행한다. import한 다른 파일은 여기 함수/정의를 호출해 사용한다.
if __name__ == "__main__":
    unittest.main()
