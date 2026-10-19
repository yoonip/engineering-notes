# 제안서 수치 형식을 명시적으로 정의한 software 변환기다. 현재 Transformer RTL 산술은 Q8.8이다.
# E8M7=[sign1][exp8 bias127][fraction7], normal hidden1, subnormal/Inf/NaN/nearest-even을 정의한다.
"""프로젝트에서 비교 기준으로 정의한 16-bit E8M7 부동소수점 변환기.

비트 배치: [sign:1][exponent:8][fraction:7], exponent bias=127.
exponent=0은 signed zero/subnormal, exponent=255는 infinity/NaN으로 처리한다.
normal fraction은 암묵적인 leading 1을 포함한다. 인코딩은 round-to-nearest,
ties-to-even이며 overflow는 infinity로 보낸다. 이는 원 제안서에 빠져 있던
규칙을 채운 software numeric-format definition이다. 이 파일은 E8M7 RTL 연산기가
아니며, 현재 Transformer RTL의 산술 기준은 검증된 signed Q8.8이다.
"""

from __future__ import annotations

import math

SIGN_SHIFT = 15
EXP_SHIFT = 7
FRAC_MASK = 0x7F
EXP_MASK = 0xFF
BIAS = 127


# sign/exp/fraction을 E8M7 nearest-even bit로 저장하며 subnormal/특수값/overflow까지 규칙을 정의한다.
def encode_e8m7(value: float) -> int:
    """Python float를 위에서 정의한 E8M7 16-bit word로 round한다."""
    value = float(value)
    sign = int(math.copysign(1.0, value) < 0.0)
    sign_word = sign << SIGN_SHIFT
    magnitude = abs(value)

    if math.isnan(magnitude):
        return sign_word | (0xFF << EXP_SHIFT) | 0x40  # quiet NaN
    if math.isinf(magnitude):
        return sign_word | (0xFF << EXP_SHIFT)
    if magnitude == 0.0:
        return sign_word

    # IEEE-like subnormal: 값 = fraction * 2^-133.
    min_normal = math.ldexp(1.0, -126)
    if magnitude < min_normal:
        fraction = round(math.ldexp(magnitude, 133))
        if fraction <= 0:
            return sign_word
        if fraction >= 128:
            return sign_word | (1 << EXP_SHIFT)  # 반올림으로 min-normal 승격
        return sign_word | int(fraction)

    exponent = math.floor(math.log2(magnitude))
    significand = math.ldexp(magnitude, -exponent)  # [1, 2)
    fraction = round((significand - 1.0) * 128)
    if fraction == 128:
        exponent += 1
        fraction = 0

    exponent_field = exponent + BIAS
    if exponent_field >= 0xFF:
        return sign_word | (0xFF << EXP_SHIFT)
    if exponent_field <= 0:
        # 경계 근처에서 log2 반올림 오차가 생겨도 subnormal 정의로 재계산한다.
        fraction = round(math.ldexp(magnitude, 133))
        if fraction <= 0:
            return sign_word
        if fraction >= 128:
            return sign_word | (1 << EXP_SHIFT)
        return sign_word | int(fraction)
    return sign_word | (int(exponent_field) << EXP_SHIFT) | (int(fraction) & FRAC_MASK)


# 16bit field를 Python float로 복원. normal은 숨은1, subnormal은 fraction*2^-133이다.
def decode_e8m7(word: int) -> float:
    """16-bit E8M7 word를 Python double 근사값으로 해석한다."""
    word &= 0xFFFF
    sign = -1.0 if (word >> SIGN_SHIFT) & 1 else 1.0
    exponent = (word >> EXP_SHIFT) & EXP_MASK
    fraction = word & FRAC_MASK

    if exponent == 0xFF:
        return math.copysign(math.nan, sign) if fraction else math.copysign(math.inf, sign)
    if exponent == 0:
        if fraction == 0:
            return math.copysign(0.0, sign)
        return sign * math.ldexp(float(fraction), -133)
    significand = 1.0 + fraction / 128.0
    return sign * math.ldexp(significand, exponent - BIAS)


# E8M7 저장 후 읽은 근사값. 원본 실수와의 표현 오차 비교용이다.
def roundtrip_e8m7(value: float) -> float:
    """E8M7로 반올림한 뒤 실수 근사값으로 복원한다."""
    return decode_e8m7(encode_e8m7(value))
