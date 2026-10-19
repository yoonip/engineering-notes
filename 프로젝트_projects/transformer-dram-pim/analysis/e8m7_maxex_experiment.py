"""MAX-EX의 정렬 손실을 정확한 Fraction 내적과 비교해 JSON 증거를 만든다.

이 실험은 E8M7 내적 커널만 평가한다. 학습 checkpoint의 hidden/LM 가중치를
샘플로 쓰지만 GPT 전체를 E8M7로 바꾸거나 bias·Softmax·LayerNorm을 시험하지 않는다.
"""

from __future__ import annotations

import argparse
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
import sys

# python analysis/e8m7_maxex_experiment.py로 직접 실행할 때도 프로젝트 package를
# 읽을 수 있도록 루트를 추가한다. -m 실행과 수치 규칙/표본은 동일하다.
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from model.e8m7_maxex import (
    decode_fields, decode_e8m7_fraction, edge_vectors, early_align_dot,
    exact_dot_e8m7, fraction_to_e8m7, maxex_dot_details,
    rounded_product_tree_dot, scale_power_of_two,
)
from model.gpt_q88 import forward_q88, load_checkpoint

def fraction_json(value: Fraction | None) -> dict | None:
    """분자/분모가 정확한 값이다. decimal은 읽기 편하도록 만든 30자리 근사다."""
    if value is None:
        return None
    with localcontext() as context:
        context.prec = 30
        approximate = str(Decimal(value.numerator) / Decimal(value.denominator))
    return {"numerator": str(value.numerator), "denominator": str(value.denominator),
            "decimal_approx": approximate}


def word_json(word: int) -> dict:
    fields = decode_fields(word)
    return {"word": word, "hex": f"{word:04x}", "kind": fields.kind,
            "sign": fields.sign,
            "finite_value": fraction_json(decode_e8m7_fraction(word))
            if fields.kind not in {"inf", "nan"} else None}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generate_vectors(seed: int, samples: int, checkpoint: Path) -> tuple[list[dict], dict]:
    rng = random.Random(seed)
    vectors = [{**vector, "family": "directed"} for vector in edge_vectors()]
    for family, count, exponent_range in (
        ("seeded_normal", samples, (-32, 32)),
        ("seeded_all_finite", samples // 2, None),
    ):
        for index in range(count):
            def words() -> list[int]:
                return [(rng.randrange(2) << 15) |
                        ((rng.randrange(255) if exponent_range is None else
                          rng.randint(*exponent_range) + 127) << 7) |
                        rng.randrange(128) for _ in range(16)]
            vectors.append({"name": f"{family}_{index}", "family": family,
                            "a_words": words(), "b_words": words()})
    for index in range(samples // 4):
        exponent = rng.randint(35, 90)
        large = fraction_to_e8m7(1 << exponent)
        small = fraction_to_e8m7(scale_power_of_two(rng.randint(128, 255), rng.randint(-10, 10) - 7))
        multiplier = fraction_to_e8m7(scale_power_of_two(rng.randint(128, 255), rng.randint(-4, 4) - 7))
        vectors.append({"name": f"cancellation_stress_{index}", "family": "cancellation_stress",
                        "a_words": [large, large | 0x8000, small] + [0] * 13,
                        "b_words": [0x3F80, 0x3F80, multiplier] + [0] * 13})
    model = load_checkpoint(checkpoint)
    vocab = model["vocab"]
    lm_head = model["weights"]["lm_head"]
    if int(model["config"]["d_model"]) != 16 or len(lm_head) != 16:
        raise ValueError("checkpoint projection 실험은 D_MODEL=16을 요구합니다.")
    for prompt in ("R", "RO", "RORI"):
        ids = [vocab.index(character) for character in prompt]
        hidden, _ = forward_q88(model, ids)
        for column in range(len(lm_head[0])):
            vectors.append({"name": f"LM_{prompt}_candidate_{column}", "family": "trained_lm_projection",
                            "prompt": prompt, "candidate_id": column, "candidate_character": vocab[column],
                            "a_words": [fraction_to_e8m7(Fraction(raw, 256)) for raw in hidden[-1]],
                            "b_words": [fraction_to_e8m7(Fraction(lm_head[row][column], 256)) for row in range(16)]})
    provenance = {"checkpoint": str(checkpoint), "checkpoint_sha256": sha256(checkpoint),
                  "prompts": ["R", "RO", "RORI"], "projection_lanes": 16,
                  "projection_columns": len(lm_head[0]), "bias_included": False,
                  "description_ko": "Q8.8 GPT의 최종 hidden과 LM 열을 각각 E8M7로 RNE 변환한 독립 내적 샘플. 전체 GPT 정확도 비교가 아닙니다."}
    return vectors, provenance


def evaluate(vector: dict) -> dict:
    a, b = vector["a_words"], vector["b_words"]
    exact_word = exact_dot_e8m7(a, b)
    methods = {}
    for guard in (0, 16, 32, 512):
        details = maxex_dot_details(a, b, guard)
        loss = abs(details.reconstructed - details.exact) if details.exact is not None else None
        methods[f"guard{guard}"] = {
            **word_json(details.result_word), "matches_exact_word": details.result_word == exact_word,
            "max_exponent": details.max_exponent, "accumulator": str(details.accumulator),
            "accumulator_width": details.accumulator_width,
            "alignment_shifts": list(details.alignment_shifts),
            "aligned_magnitudes": [str(value) for value in details.aligned_magnitudes],
            "reconstructed": fraction_json(details.reconstructed),
            "unrounded_matches_exact": details.reconstructed == details.exact if details.exact is not None else None,
            "absolute_alignment_loss": fraction_json(loss),
            "relative_alignment_loss": fraction_json(loss / abs(details.exact))
            if loss is not None and details.exact else None,
        }
    for name, function in (("early_align", early_align_dot), ("rounded_product_tree", rounded_product_tree_dot)):
        word = function(a, b)
        methods[name] = {**word_json(word), "matches_exact_word": word == exact_word}
    # 비교 방식의 최종 오차도 같은 정확한 E8M7 기준값에 대해 계산한다.
    # NaN/Inf를 큰 유한수로 대신하지 않는다. 두 결과가 유한할 때만 Fraction 오차가 정의된다.
    target_fields = decode_fields(exact_word)
    target_finite = target_fields.kind not in {"inf", "nan"}
    target_value = decode_e8m7_fraction(exact_word) if target_finite else None
    # ULP(unit in last place)는 기준값 위치의 최소 표현 간격이다. zero/subnormal은2^-133이다.
    target_unit = scale_power_of_two(1, target_fields.unbiased_exponent - 7) if target_finite else None
    for value in methods.values():
        finite_pair = target_finite and value["kind"] not in {"inf", "nan"}
        output_error = abs(decode_e8m7_fraction(value["word"]) - target_value) if finite_pair else None
        value["absolute_final_error_vs_exact_rounded"] = fraction_json(output_error)
        value["final_error_in_exact_output_ulp"] = fraction_json(output_error / target_unit) if finite_pair else None
    exact = maxex_dot_details(a, b, 512).exact
    # G512의 일치가 단순히 최종 Inf 비트 일치인 경우도 있으므로 반올림 전 Fraction까지 검사한다.
    if exact is not None:
        assert methods["guard512"]["unrounded_matches_exact"]
        assert methods["guard512"]["matches_exact_word"]
    return {**vector, "lanes": len(a), "exact_result": word_json(exact_word),
            "exact_unrounded": fraction_json(exact), "methods": methods}


def summarize(rows: list[dict]) -> dict:
    names = ("guard0", "guard16", "guard32", "guard512", "early_align", "rounded_product_tree")
    result = {"samples": len(rows), "finite_input_samples": sum(row["exact_unrounded"] is not None for row in rows),
              "methods": {}}
    for name in names:
        values = [row["methods"][name] for row in rows]
        summary = {"exact_word_matches": sum(value["matches_exact_word"] for value in values),
                   "exact_word_differences": sum(not value["matches_exact_word"] for value in values),
                   "output_kinds": dict(Counter(value["kind"] for value in values))}
        final_errors = [Fraction(int(value["final_error_in_exact_output_ulp"]["numerator"]),
                                 int(value["final_error_in_exact_output_ulp"]["denominator"]))
                        for value in values if value["final_error_in_exact_output_ulp"] is not None]
        summary.update({"finite_final_error_pairs": len(final_errors),
                        "max_final_error_in_exact_output_ulp": fraction_json(max(final_errors, default=Fraction(0))),
                        "mean_final_error_in_exact_output_ulp": fraction_json(sum(final_errors, Fraction(0)) / len(final_errors))
                        if final_errors else None})
        if name.startswith("guard"):
            finite = [value for value in values if value["unrounded_matches_exact"] is not None]
            losses = [Fraction(int(value["absolute_alignment_loss"]["numerator"]),
                               int(value["absolute_alignment_loss"]["denominator"])) for value in finite]
            summary.update({"unrounded_exact_matches": sum(value["unrounded_matches_exact"] for value in finite),
                            "nonzero_alignment_loss_samples": sum(loss != 0 for loss in losses),
                            "max_absolute_alignment_loss": fraction_json(max(losses, default=Fraction(0)))})
        result["methods"][name] = summary
    result["guard32_improves_word_match_vs16"] = sum(not row["methods"]["guard16"]["matches_exact_word"] and row["methods"]["guard32"]["matches_exact_word"] for row in rows)
    result["guard32_worsens_word_match_vs16"] = sum(row["methods"]["guard16"]["matches_exact_word"] and not row["methods"]["guard32"]["matches_exact_word"] for row in rows)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "build/reports/e8m7_maxex_experiment.json")
    parser.add_argument("--seed", type=int, default=20261004)
    parser.add_argument("--samples", type=int, default=256)
    parser.add_argument("--checkpoint", type=Path, default=ROOT / "output/tiny_gpt_full_ops_qat/tiny_gpt_qat_q88.json")
    args = parser.parse_args()
    if args.samples < 4:
        parser.error("samples는 4 이상이어야 합니다.")
    vectors, provenance = generate_vectors(args.seed, args.samples, args.checkpoint)
    rows = [evaluate(vector) for vector in vectors]
    families = sorted({row["family"] for row in rows})
    output = {"passed": True, "mode": "independent_e8m7_maxex_numerical_experiment",
              "connected_to_q88_transformer": False, "physical_board_measured": False,
              "physical_dram_pim_measured": False, "seed": args.seed,
              "definition_ko": "16bit full product + MAX-EX magnitude 절삭 + signed 넓은 트리 + 최종 E8M7 RNE",
              "comparison_assumptions_ko": {"exact": "Fraction 곱/합 후 최종 한 번 RNE, float 중간변환 없음",
                  "early_align": "곱마다 E8M7 RNE 후 8bit 공통 지수 정렬(G0), 마지막 RNE",
                  "rounded_product_tree": "곱마다 RNE하고 균형 트리의 매 덧셈에서도 RNE; 벤더 명령 표준을 주장하지 않음",
                  "guard512": "유한 product 지수 폭 최대506보다 넓어 정렬 손실 없음; 실제 FPGA 자원은 G16/G32만 측정"},
              "checkpoint_provenance": provenance,
              "source_sha256": {path: sha256(ROOT / path) for path in (
                  "model/e8m7_maxex.py", "model/test_e8m7_maxex.py", "analysis/e8m7_maxex_experiment.py")},
              "summary": summarize(rows),
              "families": {family: summarize([row for row in rows if row["family"] == family]) for family in families},
              "vectors": rows}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({"passed": True, "output": str(args.output), "summary": output["summary"],
                      "family_samples": {family: output["families"][family]["samples"] for family in families}}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
