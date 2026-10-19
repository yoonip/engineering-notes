# E8M7의 알려진 bit pattern/경계/반올림 회귀시험. assert가 규칙 변경/오류를 감지한다.
"""명시적으로 정의한 E8M7 변환 규칙의 경계 시험."""

from __future__ import annotations

import math
import unittest

from model.e8m7 import decode_e8m7, encode_e8m7, roundtrip_e8m7


# 알려진 bit/경계/반올림 assert를 모은 unittest 시험 클래스.
class E8M7Tests(unittest.TestCase):
    # ±0/1/-2/±Inf/NaN의 E8M7 bit pattern/부호 검사.
    # assert 실패는 이 경계/규칙이 기대값과 달라졌다는 뜻이다. PASS 표시만으로 숫자 검사를 대체하지 않는다.
    def test_signed_zero_one_two_and_special_values(self) -> None:
        self.assertEqual(encode_e8m7(0.0), 0x0000)
        self.assertEqual(encode_e8m7(-0.0), 0x8000)
        self.assertEqual(encode_e8m7(1.0), 0x3F80)
        self.assertEqual(encode_e8m7(-2.0), 0xC000)
        self.assertEqual(decode_e8m7(0x7F80), math.inf)
        self.assertEqual(decode_e8m7(0xFF80), -math.inf)
        self.assertTrue(math.isnan(decode_e8m7(0x7FC0)))
        self.assertTrue(math.isnan(decode_e8m7(0xFFC0)))

    # 최소 normal/subnormal,최대 유한값,overflow->Inf 검사.
    # assert 실패는 이 경계/규칙이 기대값과 달라졌다는 뜻이다. PASS 표시만으로 숫자 검사를 대체하지 않는다.
    def test_normal_subnormal_and_overflow_boundaries(self) -> None:
        min_normal = math.ldexp(1.0, -126)
        min_subnormal = math.ldexp(1.0, -133)
        max_finite = (2.0 - 1.0/128.0) * math.ldexp(1.0, 127)
        self.assertEqual(encode_e8m7(min_normal), 0x0080)
        self.assertEqual(encode_e8m7(min_subnormal), 0x0001)
        self.assertEqual(decode_e8m7(0x0001), min_subnormal)
        self.assertEqual(encode_e8m7(max_finite), 0x7F7F)
        self.assertEqual(encode_e8m7(max_finite * 2), 0x7F80)

    # 정확히 중간인 수에서 마지막 bit 짝수를 고르는 nearest-even 검사.
    # assert 실패는 이 경계/규칙이 기대값과 달라졌다는 뜻이다. PASS 표시만으로 숫자 검사를 대체하지 않는다.
    def test_round_to_nearest_ties_to_even(self) -> None:
        self.assertEqual(encode_e8m7(1.0 + 1.0/256.0), 0x3F80)
        self.assertEqual(encode_e8m7(1.0 + 3.0/256.0), 0x3F82)
        self.assertAlmostEqual(roundtrip_e8m7(-3.25), -3.25)


# 직접 실행할 때만 진입점을 실행한다. import한 다른 파일은 여기 함수/정의를 호출해 사용한다.
if __name__ == "__main__":
    unittest.main()
