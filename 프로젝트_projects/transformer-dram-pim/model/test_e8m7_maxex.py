"""E8M7 MAX-EX의 수치 정의/손실/반올림을 확인하는 독립 회귀시험.

MAX-EX와 이상적 Fraction 내적이 항상 같다는 주장을 시험하지 않는다.
같아야 할 입력과 달라지는 반례를 각각 명시하여 오차를 정상 PASS로 숨기지 않는다.
"""

from fractions import Fraction
import random
import unittest

from model.e8m7 import decode_e8m7, encode_e8m7
from model.e8m7_maxex import (
    CANONICAL_NAN, decode_fields, decode_e8m7_fraction, fraction_to_e8m7,
    scale_power_of_two, maxex_dot, maxex_dot_details, exact_dot_e8m7,
    early_align_dot, rounded_product_tree_dot, edge_vectors,
)


class MaxExTests(unittest.TestCase):
    def test_all_finite_word_roundtrips_without_float_intermediate(self):
        # 65,280개 유한 단어를 모두 조사한다. -0만 Fraction 외부 부호 정보를 보존한다.
        count = 0
        for word in range(65536):
            fields = decode_fields(word)
            if fields.kind in {"nan", "inf"}:
                continue
            value = decode_e8m7_fraction(word)
            self.assertEqual(fraction_to_e8m7(value, negative_zero=word == 0x8000), word)
            # 기존 float 변환기는 표준 형식의 값 자체에는 정확한 double 표현을 갖는다.
            self.assertEqual(encode_e8m7(decode_e8m7(word)), word)
            count += 1
        self.assertEqual(count, 65280)

    def test_every_adjacent_finite_midpoint_ties_to_even(self):
        # 정상/비정상 경계를 포함한 양수 유한 인접값의 모든 중간값과 음수 대응을 검사한다.
        for lower in range(0x7F7F):
            upper = lower + 1
            midpoint = (decode_e8m7_fraction(lower) + decode_e8m7_fraction(upper)) / 2
            chosen = lower if lower % 2 == 0 else upper
            self.assertEqual(fraction_to_e8m7(midpoint), chosen)
            self.assertEqual(fraction_to_e8m7(-midpoint), chosen | 0x8000)

    def test_fraction_converter_exact_boundaries(self):
        self.assertEqual(fraction_to_e8m7(Fraction(257, 256)), 0x3F80)
        self.assertEqual(fraction_to_e8m7(Fraction(259, 256)), 0x3F82)
        self.assertEqual(fraction_to_e8m7(scale_power_of_two(1, -134)), 0)
        self.assertEqual(fraction_to_e8m7(scale_power_of_two(-1, -134)), 0x8000)
        self.assertEqual(fraction_to_e8m7(scale_power_of_two(Fraction(255, 2), -133)), 0x0080)
        threshold = scale_power_of_two(Fraction(511, 2), 120)
        self.assertEqual(fraction_to_e8m7(threshold), 0x7F80)
        self.assertEqual(fraction_to_e8m7(threshold - scale_power_of_two(1, -133)), 0x7F7F)
        self.assertEqual(fraction_to_e8m7(-threshold), 0xFF80)
        with self.assertRaises(TypeError):
            fraction_to_e8m7(1.0)

    def test_zero_and_nan_infinity_contract(self):
        self.assertEqual(maxex_dot([0x8000], [0x3F80]), 0)
        for a, b, expected in [
            ([0x7F81], [0x3F80], CANONICAL_NAN),
            ([0xFFC1], [0x3F80], CANONICAL_NAN),
            ([0x7F80], [0], CANONICAL_NAN),
            ([0xFF80], [0x8000], CANONICAL_NAN),
            ([0x7F80, 0xFF80], [0x3F80, 0x3F80], CANONICAL_NAN),
            ([0xFF80], [0xBF80], 0x7F80),
            ([0xFF80], [0x3F80], 0xFF80),
        ]:
            self.assertEqual(maxex_dot(a, b), expected)
            self.assertEqual(exact_dot_e8m7(a, b), expected)

    def test_negative_underflow_keeps_sign_but_cancellation_is_positive_zero(self):
        self.assertEqual(maxex_dot([0x8001], [0x0001]), 0x8000)
        self.assertEqual(exact_dot_e8m7([0x8001], [0x0001]), 0x8000)
        self.assertEqual(maxex_dot([0x3F80, 0xBF80], [0x3F80, 0x3F80]), 0)

    def test_odd_lane_tree_and_accumulator_capacity(self):
        self.assertEqual(maxex_dot([0x3F80, 0x4000, 0x4040], [0x3F80] * 3), 0x40C0)
        for lanes in [1, 3, 16, 17]:
            for guard in [0, 16, 32]:
                details = maxex_dot_details([0x7F7F] * lanes, [0x7F7F] * lanes, guard)
                self.assertEqual(details.accumulator_width, 16 + guard + (lanes - 1).bit_length() + 1)
                self.assertEqual(len(details.max_tree[0]), 1 << (lanes - 1).bit_length())
                self.assertEqual(details.accumulator, lanes * 65025 * (1 << guard))
                self.assertEqual(details.result_word, 0x7F80)

    def test_alignment_truncates_magnitude_before_sign(self):
        small_negative = fraction_to_e8m7(scale_power_of_two(-1, -100))
        details = maxex_dot_details([0x3F80, small_negative], [0x3F80] * 2, 0)
        self.assertEqual(details.aligned_magnitudes, (16384, 0))
        self.assertEqual(details.accumulator, 16384)

    def test_guard32_recovers_value_that_guard16_loses(self):
        vector = next(v for v in edge_vectors() if v['name'] == 'guard32가_1을_복원')
        a, b = vector['a_words'], vector['b_words']
        self.assertEqual(maxex_dot(a, b, 16), 0)
        self.assertEqual(maxex_dot(a, b, 32), 0x3F80)
        self.assertEqual(exact_dot_e8m7(a, b), 0x3F80)

    def test_guard0_truncation_can_break_exact_cancellation(self):
        # 129*129는 홀수다. +P/2,+P/2,-P를 공통 정수 눈금으로 절삭하면 -1이 남는다.
        vector = next(v for v in edge_vectors() if v['name'] == 'guard0_절삭이_상쇄를_깨뜨림')
        a, b = vector['a_words'], vector['b_words']
        self.assertEqual(exact_dot_e8m7(a, b), 0)
        self.assertEqual(maxex_dot_details(a, b, 0).accumulator, -1)
        self.assertNotEqual(maxex_dot(a, b, 0), 0)
        self.assertEqual(maxex_dot(a, b, 16), 0)
        self.assertEqual(maxex_dot(a, b, 32), 0)

    def test_narrow_guards_can_break_exact_zero_after_large_pair_cancellation(self):
        # +2^G,-2^G는 서로 사라지지만 MAX 지수는 높인다. 남은 +X/2,+X/2,-X를
        # 공통눈금으로 절삭하면 정확한 Fraction 합0과 달리 S=-1이 남을 수 있다.
        for guard in (16, 32):
            large = fraction_to_e8m7(1 << guard)
            a = [large, large | 0x8000, 0x3F01, 0x3F01, 0xBF81] + [0] * 11
            b = [0x3F80, 0x3F80, 0x3F81, 0x3F81, 0x3F81] + [0] * 11
            details = maxex_dot_details(a, b, guard)
            self.assertEqual(details.exact, 0)
            self.assertEqual(exact_dot_e8m7(a, b), 0)
            self.assertEqual(details.accumulator, -1)
            self.assertEqual(details.result_word, 0xB880)
            self.assertEqual(maxex_dot(a, b, 512), 0)

    def test_guard32_still_has_loss_and_other_tree_can_preserve_cancellation(self):
        vector = next(v for v in edge_vectors() if v['name'] == 'guard32도_작은항을_잃음')
        a, b = vector['a_words'], vector['b_words']
        self.assertEqual(maxex_dot(a, b, 32), 0)
        self.assertEqual(early_align_dot(a, b), 0)
        self.assertEqual(rounded_product_tree_dot(a, b), 0x3F80)
        self.assertEqual(exact_dot_e8m7(a, b), 0x3F80)

    def test_full_product_not_rounded_to_infinity_before_cancellation(self):
        vector = next(v for v in edge_vectors() if v['name'] == '유한_거대곱_상쇄_후_1')
        a, b = vector['a_words'], vector['b_words']
        self.assertEqual(maxex_dot(a, b), 0)
        self.assertEqual(exact_dot_e8m7(a, b), 0x3F80)
        self.assertEqual(rounded_product_tree_dot(a, b), CANONICAL_NAN)

    def test_tiny_term_can_change_overflow_rounding_decision(self):
        vector = next(v for v in edge_vectors() if v['name'] == 'overflow_tie보다_미세하게_작음')
        a, b = vector['a_words'], vector['b_words']
        self.assertEqual(maxex_dot(a, b, 16), 0x7F80)
        self.assertEqual(maxex_dot(a, b, 32), 0x7F80)
        self.assertEqual(exact_dot_e8m7(a, b), 0x7F7F)
        self.assertEqual(maxex_dot(a, b, 506), 0x7F7F)

    def test_guard506_guarantees_no_finite_alignment_loss(self):
        # 가능한 제품 지수 폭은 254-(-252)=506. G가 이 폭 이상이면 모든 integer bit를 보존한다.
        rng = random.Random(20261004)
        for _ in range(64):
            a = [(rng.randrange(2) << 15) | (rng.randrange(255) << 7) | rng.randrange(128) for _ in range(16)]
            b = [(rng.randrange(2) << 15) | (rng.randrange(255) << 7) | rng.randrange(128) for _ in range(16)]
            for guard in (506, 512):
                details = maxex_dot_details(a, b, guard)
                self.assertEqual(details.reconstructed, details.exact)
                self.assertEqual(details.result_word, exact_dot_e8m7(a, b))

    def test_guard512_restores_extreme_finite_cancellation(self):
        vector = next(v for v in edge_vectors() if v['name'] == '유한_거대곱_상쇄_후_1')
        a, b = vector['a_words'], vector['b_words']
        self.assertEqual(maxex_dot(a, b, 16), 0)
        self.assertEqual(maxex_dot(a, b, 32), 0)
        self.assertEqual(maxex_dot(a, b, 512), 0x3F80)
        self.assertEqual(maxex_dot(a, b, 512), exact_dot_e8m7(a, b))

    def test_guard32_is_exact_when_product_exponent_spread_is_at_most32(self):
        rng = random.Random(17)
        for _ in range(128):
            def words():
                return [(rng.randrange(2) << 15) | ((rng.randrange(-8, 9) + 127) << 7) | rng.randrange(128) for _ in range(16)]
            details = maxex_dot_details(words(), words(), 32)
            self.assertEqual(details.reconstructed, details.exact)

    def test_input_errors_are_not_silently_wrapped(self):
        for a, b, guard in [([], [], 16), ([0], [], 16), ([65536], [0], 16), ([0], [0], -1)]:
            with self.assertRaises(ValueError):
                maxex_dot(a, b, guard)
        with self.assertRaises(ValueError):
            decode_e8m7_fraction(0x7F80)


if __name__ == '__main__':
    unittest.main()
