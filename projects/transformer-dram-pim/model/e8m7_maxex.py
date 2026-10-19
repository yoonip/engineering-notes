"""E8M7 MAX-EX 내적의 독립 정수/Fraction 기준 모델.

이 연구용 커널은 현재 Q8.8 GPT의 산술을 바꾸지 않는다. Transformer의
Q/K/V, FFN, LM head에 반복되는 '벡터×가중치' 내적을 부동소수점으로
구현할 경우를 별도로 시험한다. 비트 형식은 model.e8m7과 동일하지만
Fraction 변환/내적에는 Python float를 중간값으로 쓰지 않는다.

유한 피연산자: 값 = (-1)^sign * m * 2^(u-7).
normal은 m=128+fraction, u=exponent-127; subnormal은 m=fraction,u=-126.
곱: P=m_a*m_b(16비트), E=u_a+u_b, 값=(-1)^sign*P*2^(E-14).
MAX-EX: M=max(E), A_i=(P_i<<G)>>(M-E_i)를 magnitude로 절삭한 후 부호를
붙인다. 넓은 균형 트리 합 S의 값은 S*2^(M-14-G)이고 마지막에 한 번 RNE한다.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Callable, Sequence

from model.e8m7 import BIAS, EXP_MASK, EXP_SHIFT, FRAC_MASK, SIGN_SHIFT

CANONICAL_NAN = 0x7FC0
POSITIVE_INFINITY = 0x7F80
NEGATIVE_INFINITY = 0xFF80
INACTIVE_EXPONENT = -512  # 유효 곱 지수 -252..254 밖: RTL의 signed10 sentinel.


@dataclass(frozen=True)
class DecodedWord:
    """필드를 분해한 결과. m은 부호 없는 8비트 크기이며 sign은 별도다."""
    word: int
    sign: int
    exponent_field: int
    fraction: int
    significand: int
    unbiased_exponent: int
    kind: str


@dataclass(frozen=True)
class MaxExDetails:
    """RTL 내부 단계를 읽을 때 비교할 값. 특수값에는 exact/reconstructed=None."""
    result_word: int
    max_exponent: int | None
    accumulator: int
    accumulator_width: int
    aligned_magnitudes: tuple[int, ...]
    alignment_shifts: tuple[int, ...]
    reconstructed: Fraction | None
    exact: Fraction | None
    product_magnitudes: tuple[int, ...]
    product_exponents: tuple[int, ...]
    product_signs: tuple[int, ...]
    max_tree: tuple[tuple[int, ...], ...]
    sum_tree: tuple[tuple[int, ...], ...]


def decode_fields(word: int) -> DecodedWord:
    """16비트 필드와 유효 significand를 분리한다. 잘못된 포트 값은 거절한다."""
    if not isinstance(word, int) or not 0 <= word <= 0xFFFF:
        raise ValueError("E8M7 단어는 0..65535 정수여야 합니다.")
    sign = word >> SIGN_SHIFT
    exponent = (word >> EXP_SHIFT) & EXP_MASK
    fraction = word & FRAC_MASK
    if exponent == 255:
        return DecodedWord(word, sign, exponent, fraction, 0, 0,
                           "nan" if fraction else "inf")
    if exponent == 0:
        return DecodedWord(word, sign, exponent, fraction, fraction, -126,
                           "subnormal" if fraction else "zero")
    return DecodedWord(word, sign, exponent, fraction, 128 + fraction,
                       exponent - BIAS, "normal")


def scale_power_of_two(value: int | Fraction, exponent: int) -> Fraction:
    """정확한 이진 배율. 큰 지수나 작은 subnormal도 float overflow 없이 표현한다."""
    fraction = Fraction(value)
    return fraction * (1 << exponent) if exponent >= 0 else fraction / (1 << -exponent)


def decode_e8m7_fraction(word: int) -> Fraction:
    """유한 E8M7을 정확한 유리수로 복원한다. ±0의 수치 값은 모두 Fraction(0)."""
    fields = decode_fields(word)
    if fields.kind in {"nan", "inf"}:
        raise ValueError("NaN/Inf는 유한 Fraction으로 복원할 수 없습니다.")
    value = scale_power_of_two(fields.significand, fields.unbiased_exponent - 7)
    return -value if fields.sign else value


def _floor_log2_positive(value: Fraction) -> int:
    """bit_length 후 정수 비교로 floor(log2)를 구한다. 경계에서도 log2 float 오차가 없다."""
    numerator, denominator = value.numerator, value.denominator
    exponent = numerator.bit_length() - denominator.bit_length()
    below = numerator < (denominator << exponent) if exponent >= 0 else (numerator << -exponent) < denominator
    return exponent - 1 if below else exponent


def _round_positive_integer(value: Fraction) -> int:
    """가장 가까운 정수, 정확히 중간이면 짝수. 나머지 비교가 guard/round/sticky에 대응한다."""
    quotient, remainder = divmod(value.numerator, value.denominator)
    twice = remainder * 2
    return quotient + int(twice > value.denominator or (twice == value.denominator and quotient & 1))


def fraction_to_e8m7(value: Fraction | int, negative_zero: bool = False) -> int:
    """유리수를 16비트 E8M7로 한 번 RNE한다. float 입력/중간변환을 사용하지 않는다.

    overflow는 부호 있는 Inf, 작은 음수의 underflow는 -0이다. Fraction은
    -0를 구분하지 않으므로 standalone zero 변환에만 negative_zero를 받는다.
    내적의 정확한 상쇄/전체 zero는 정의에 따라 항상 +0이다.
    """
    if not isinstance(value, (Fraction, int)):
        raise TypeError("정확한 Fraction 또는 정수만 변환할 수 있습니다.")
    value = Fraction(value)
    if value == 0:
        return 0x8000 if negative_zero else 0
    sign_word = 0x8000 if value < 0 else 0
    magnitude = abs(value)
    # subnormal 간격은 2^-133이다. 반올림한 128은 최소 normal로 승격한다.
    if magnitude < scale_power_of_two(1, -126):
        fraction = _round_positive_integer(scale_power_of_two(magnitude, 133))
        return sign_word | (0x0080 if fraction >= 128 else fraction)
    exponent = _floor_log2_positive(magnitude)
    mantissa = _round_positive_integer(scale_power_of_two(magnitude, 7 - exponent))
    if mantissa == 256:
        mantissa, exponent = 128, exponent + 1
    if exponent > 127:
        return sign_word | POSITIVE_INFINITY
    return sign_word | ((exponent + BIAS) << EXP_SHIFT) | (mantissa - 128)


def _validate_inputs(a_words: Sequence[int], b_words: Sequence[int], guard_bits: int = 0) -> int:
    if not a_words or len(a_words) != len(b_words):
        raise ValueError("두 벡터 길이는 동일하고 1 이상이어야 합니다.")
    if not isinstance(guard_bits, int) or guard_bits < 0:
        raise ValueError("GUARD_BITS는 0 이상 정수여야 합니다.")
    for word in (*a_words, *b_words):
        decode_fields(word)
    return len(a_words)


def _products(a_words: Sequence[int], b_words: Sequence[int]) -> tuple[list[int], list[int], list[int], int | None]:
    """곱을 아직 E8M7로 반올림하지 않는다. 유한 곱의 최종 overflow는 누산 뒤 판단한다."""
    magnitudes, exponents, signs = [], [], []
    positive_inf = negative_inf = invalid = False
    for a_word, b_word in zip(a_words, b_words):
        a, b = decode_fields(a_word), decode_fields(b_word)
        sign = a.sign ^ b.sign
        if a.kind == "nan" or b.kind == "nan":
            invalid = True
        elif a.kind == "inf" or b.kind == "inf":
            if a.kind == "zero" or b.kind == "zero":
                invalid = True
            elif sign:
                negative_inf = True
            else:
                positive_inf = True
        finite = a.kind not in {"nan", "inf"} and b.kind not in {"nan", "inf"}
        magnitudes.append(a.significand * b.significand if finite else 0)
        exponents.append(a.unbiased_exponent + b.unbiased_exponent if finite else INACTIVE_EXPONENT)
        signs.append(sign)
    special = CANONICAL_NAN if invalid or (positive_inf and negative_inf) else \
        POSITIVE_INFINITY if positive_inf else NEGATIVE_INFINITY if negative_inf else None
    return magnitudes, exponents, signs, special


def balanced_tree(values: Sequence[int], operation: Callable[[int, int], int], padding: int) -> tuple[tuple[int, ...], ...]:
    """다음 2의 거듭제곱까지 pad하고 두 개씩 결합한다. RTL의 균형 max/adder tree와 같다."""
    count = 1 << (len(values) - 1).bit_length()
    level = tuple(values) + (padding,) * (count - len(values))
    levels = [level]
    while len(level) > 1:
        level = tuple(operation(level[i], level[i + 1]) for i in range(0, len(level), 2))
        levels.append(level)
    return tuple(levels)


def maxex_dot_details(a_words: Sequence[int], b_words: Sequence[int], guard_bits: int = 16) -> MaxExDetails:
    """모든 정렬/누산 중간값과 최종 비트를 반환한다. 정렬 절삭과 마지막 RNE는 별도다."""
    lanes = _validate_inputs(a_words, b_words, guard_bits)
    width = 16 + guard_bits + (lanes - 1).bit_length() + 1
    products, exponents, signs, special = _products(a_words, b_words)
    maximum_tree = balanced_tree([e if p else INACTIVE_EXPONENT for p, e in zip(products, exponents)], max, INACTIVE_EXPONENT)
    if special is not None:
        return MaxExDetails(special, None, 0, width, (0,) * lanes, (0,) * lanes,
                            None, None, tuple(products), tuple(exponents), tuple(signs), maximum_tree, ())
    exact = sum((scale_power_of_two(-p if sign else p, e - 14)
                 for p, e, sign in zip(products, exponents, signs)), Fraction(0))
    maximum = maximum_tree[-1][0]
    if maximum == INACTIVE_EXPONENT:
        zeros = (0,) * lanes
        return MaxExDetails(0, None, 0, width, zeros, zeros, Fraction(0), exact,
                            tuple(products), tuple(exponents), tuple(signs), maximum_tree,
                            balanced_tree(zeros, lambda x, y: x + y, 0))
    shifts = tuple(maximum - e if p else 0 for p, e in zip(products, exponents))
    # 음수에 산술 >>를 직접 적용하면 -1 쪽으로 내려가므로 먼저 양수 크기를 이동한다.
    aligned = tuple((p << guard_bits) >> shift for p, shift in zip(products, shifts))
    signed = tuple(-p if sign else p for p, sign in zip(aligned, signs))
    sum_tree = balanced_tree(signed, lambda x, y: x + y, 0)
    accumulator = sum_tree[-1][0]
    assert -(1 << (width - 1)) <= accumulator < (1 << (width - 1)), "규정 누산 폭을 넘었습니다."
    reconstructed = scale_power_of_two(accumulator, maximum - 14 - guard_bits)
    return MaxExDetails(fraction_to_e8m7(reconstructed), maximum, accumulator, width,
                        aligned, shifts, reconstructed, exact, tuple(products), tuple(exponents),
                        tuple(signs), maximum_tree, sum_tree)


def maxex_dot(a_words: Sequence[int], b_words: Sequence[int], guard_bits: int = 16) -> int:
    """RTL 대조에 쓰는 최소 API: 입력 16비트 단어 배열 두 개에서 결과 단어 하나."""
    return maxex_dot_details(a_words, b_words, guard_bits).result_word


def exact_dot_e8m7(a_words: Sequence[int], b_words: Sequence[int]) -> int:
    """유한 곱/합을 Fraction으로 정확히 계산하고 최종 한 번 RNE하는 이상적 내적 기준."""
    _validate_inputs(a_words, b_words)
    products, exponents, signs, special = _products(a_words, b_words)
    if special is not None:
        return special
    total = sum((scale_power_of_two(-p if sign else p, e - 14)
                 for p, e, sign in zip(products, exponents, signs)), Fraction(0))
    return fraction_to_e8m7(total)


def _sum_word_specials(words: Sequence[int]) -> int | None:
    """조기 반올림 비교 모델의 NaN/Inf 합 규칙. 실제 벤더 BF16 명령의 모델로 주장하지 않는다."""
    fields = [decode_fields(word) for word in words]
    if any(word.kind == "nan" for word in fields):
        return CANONICAL_NAN
    positives = any(word.kind == "inf" and not word.sign for word in fields)
    negatives = any(word.kind == "inf" and word.sign for word in fields)
    return CANONICAL_NAN if positives and negatives else POSITIVE_INFINITY if positives else NEGATIVE_INFINITY if negatives else None


def rounded_product_words(a_words: Sequence[int], b_words: Sequence[int]) -> tuple[int, ...]:
    """비교용으로 곱마다 E8M7 RNE한다. MAX-EX 본 경로는 이 조기 반올림을 하지 않는다."""
    _validate_inputs(a_words, b_words)
    words = []
    for a, b in zip(a_words, b_words):
        p, e, sign, special = _products([a], [b])
        words.append(special if special is not None else fraction_to_e8m7(scale_power_of_two(-p[0] if sign[0] else p[0], e[0] - 14)))
    return tuple(words)


def early_align_dot(a_words: Sequence[int], b_words: Sequence[int], guard_bits: int = 0) -> int:
    """비교 가정: 곱마다 E8M7로 RNE한 뒤 8bit significand를 공통 지수로 조기 정렬한다.

    GUARD=0이면 common-grid에서 작은 항이 먼저 사라진다. 이 비교기를 실제 GPU,
    PIM 제품 또는 표준 BF16 dot 명령이라고 부르지 않는다. 비교 가정을 명시한다.
    """
    _validate_inputs(a_words, b_words, guard_bits)
    words = rounded_product_words(a_words, b_words)
    special = _sum_word_specials(words)
    if special is not None:
        return special
    fields = [decode_fields(word) for word in words]
    selected = [word.unbiased_exponent for word in fields if word.significand]
    if not selected:
        return 0
    maximum = max(selected)
    aligned = [((word.significand << guard_bits) >> (maximum - word.unbiased_exponent)) if word.significand else 0 for word in fields]
    total = sum(-value if word.sign else value for value, word in zip(aligned, fields))
    return fraction_to_e8m7(scale_power_of_two(total, maximum - 7 - guard_bits))


def rounded_product_tree_dot(a_words: Sequence[int], b_words: Sequence[int]) -> int:
    """또 다른 비교: 곱을 먼저 RNE하고 균형 덧셈 트리의 매 단계에도 E8M7 RNE한다."""
    words = rounded_product_words(a_words, b_words)
    def add(a: int, b: int) -> int:
        special = _sum_word_specials((a, b))
        return special if special is not None else fraction_to_e8m7(decode_e8m7_fraction(a) + decode_e8m7_fraction(b))
    return balanced_tree(words, add, 0)[-1][0]


def edge_vectors() -> list[dict]:
    """RTL driver와 실험이 공유할 경계 벡터. 같은 vector에 guard16/32 기준을 적용한다."""
    def padded(name: str, pairs: list[tuple[int, int]], lanes: int = 16) -> dict:
        pairs = pairs + [(0, 0)] * (lanes - len(pairs))
        return {"name": name, "a_words": [a for a, _ in pairs], "b_words": [b for _, b in pairs]}
    one, half, minimum = 0x3F80, 0x3F00, 1
    p40, p80 = fraction_to_e8m7(1 << 40), fraction_to_e8m7(1 << 80)
    return [
        padded("전체_positive_zero", []),
        padded("전체_signed_zero", [(0x8000, one)] * 16),
        padded("16개_1의_합", [(one, one)] * 16),
        padded("16개_음수1의_합", [(0xBF80, one)] * 16),
        padded("최소_subnormal_보존", [(minimum, one)]),
        padded("최대_subnormal_보존", [(0x007F, one)]),
        padded("최소_normal_보존", [(0x0080, one)]),
        padded("양수_underflow_tie_zero", [(minimum, half)]),
        padded("음수_underflow_signed_zero", [(0x8001, half)]),
        padded("최소_subnormal_제곱", [(minimum, minimum)]),
        padded("subnormal에서_normal_RNE승격", [(0x007F, one), (minimum, half)]),
        padded("1근처_RNE_even_down", [(one, one), (fraction_to_e8m7(Fraction(1, 256)), one)]),
        padded("1근처_RNE_even_up", [(one, one), (fraction_to_e8m7(Fraction(3, 256)), one)]),
        padded("정확한_상쇄_plus_zero", [(one, one), (0xBF80, one)]),
        padded("guard0_절삭이_상쇄를_깨뜨림", [(0x3F01, 0x3F81), (0x3F01, 0x3F81), (0xBF81, 0x3F81)]),
        padded("guard32가_1을_복원", [(p40, one), (p40 | 0x8000, one), (one, one)]),
        padded("guard32도_작은항을_잃음", [(p80, one), (p80 | 0x8000, one), (one, one)]),
        padded("유한_거대곱_상쇄_후_1", [(0x7F7F, 0x7F7F), (0xFF7F, 0x7F7F), (one, one)]),
        padded("overflow_RNE_중간값", [(0x7F7F, one), (fraction_to_e8m7(1 << 119), one)]),
        padded("overflow_tie보다_미세하게_작음", [(0x7F7F, one), (fraction_to_e8m7(1 << 119), one), (0x8001, one)]),
        padded("NaN_payload_정규화", [(0x7F81, one)]),
        padded("음수_NaN_payload_정규화", [(0xFFC1, one)]),
        padded("Inf_times_zero_invalid", [(0x7F80, 0)]),
        padded("양음_Inf_혼합_invalid", [(0x7F80, one), (0xFF80, one)]),
        padded("양수_Inf", [(0xFF80, 0xBF80)]),
        padded("음수_Inf", [(0xFF80, one)]),
        padded("홀수3lane_트리_padding", [(one, one), (0x4000, one), (0x4040, one)], 3),
    ]
