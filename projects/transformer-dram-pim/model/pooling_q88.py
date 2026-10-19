"""독립 pooling PU의 순수 Python Q8.8 기준과 고정 seed 검증 입력."""
from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Sequence


@dataclass(frozen=True)
class PoolingDetails:
    # raw는 실수 값이 아니라 signed Q8.8 저장 정수다. 실수로 읽을 때 /256한다.
    result_raw: int
    result_word: int
    valid_count: int
    signed_sum: int
    maximum_raw: int | None
    tree_leaves: int
    sum_width: int
    operation: str


def word_to_signed(word: int) -> int:
    # 16bit 2의 보수 bit-pattern을 Python signed 정수로 복원한다.
    # 예: ffff는 -1 raw, 즉 -1/256이지 실수 -1이 아니다.
    if not 0 <= word <= 0xFFFF:
        raise ValueError("16bit word는 0..65535여야 합니다.")
    return word - 0x10000 if word & 0x8000 else word


def signed_to_word(raw: int) -> int:
    if not -32768 <= raw <= 32767:
        raise ValueError("Q8.8 raw는 -32768..32767여야 합니다.")
    return raw & 0xFFFF


def truncate_division_zero(numerator: int, denominator: int) -> int:
    # Python의 음수 //는 바닥 내림이어서 SV signed division과 다르다.
    # float 변환도 사용하지 않고, 절댓값 나눗셈 뒤 부호를 붙여 0 방향 절삭한다.
    if denominator <= 0:
        raise ValueError("유효 개수 분모는 양수여야 합니다.")
    magnitude = abs(numerator) // denominator
    return -magnitude if numerator < 0 else magnitude


def pool_details(values: Sequence[int], valid_mask: int, operation: str = "max") -> PoolingDetails:
    # RTL packed bus에 넣기 전 signed raw 리스트를 받는다. invalid lane도
    # 16bit 입력이라는 형식 검사는 하되 실제 max/sum/count에서는 제외한다.
    if not values or any(not isinstance(raw, int) or not -32768 <= raw <= 32767 for raw in values):
        raise ValueError("빈 window는 불가하며 모든 raw는 signed 16bit여야 합니다.")
    if not isinstance(valid_mask, int) or not 0 <= valid_mask < (1 << len(values)):
        raise ValueError("valid_mask는 window 범위의 비트만 포함해야 합니다.")
    if operation not in ("max", "avg"):
        raise ValueError("operation은 max 또는 avg입니다.")
    selected = [raw for lane, raw in enumerate(values) if (valid_mask >> lane) & 1]
    signed_sum = sum(selected)
    maximum = max(selected) if selected else None
    count = len(selected)
    result = 0 if not selected else (maximum if operation == "max" else truncate_division_zero(signed_sum, count))
    # 평균은 입력 범위 안에 있으므로 포화/16bit wrap을 하지 않는다.
    assert -32768 <= result <= 32767
    tree_levels = (len(values) - 1).bit_length()
    return PoolingDetails(result, signed_to_word(result), count, signed_sum, maximum,
                          1 << tree_levels, 16 + tree_levels, operation)


def pool_q88(values: Sequence[int], valid_mask: int, operation: str = "max") -> int:
    # SV result와 대응하는 signed raw 정수 하나를 돌려준다.
    return pool_details(values, valid_mask, operation).result_raw


def make_vectors(window: int, random_cases: int = 128, seed: int = 20261005) -> list[dict]:
    # mask는 lane별 padding 제외 여부다. max/avg에 같은 edge 입력을 모두 넣어
    # runtime operation 선택과 invalid 값 제외 규칙을 독립적으로 확인한다.
    if not 1 <= window <= 64 or random_cases < 0:
        raise ValueError("검증 window는 1..64, random_cases는 0 이상입니다.")
    all_valid = (1 << window) - 1
    alternating = sum(1 << i for i in range(window) if i % 2 == 0)
    edges = [
        ("empty_with_extreme_invalid_values", [32767 if i % 2 else -32768 for i in range(window)], 0),
        ("all_zero", [0] * window, all_valid),
        ("all_maximum_sum_width", [32767] * window, all_valid),
        ("all_minimum_sum_width", [-32768] * window, all_valid),
        ("negative_values_invalid_zeros_excluded", [-1-i for i in range(window)], alternating),
        ("negative_fraction_zero_truncation", [-1 if i % 2 == 0 else -2 for i in range(window)], all_valid),
        ("positive_fraction_zero_truncation", [1 if i % 2 == 0 else 2 for i in range(window)], all_valid),
        ("opposite_extremes", [-32768 if i % 2 == 0 else 32767 for i in range(window)], all_valid),
        ("equal_maximum_tie", [-256] * window, all_valid),
        ("only_first_lane", [-32768] + [32767] * (window-1), 1),
        ("only_last_lane", [32767] * (window-1) + [-513], 1 << (window-1)),
        ("invalid_positive_must_not_win", [-512 if i % 2 == 0 else 32767 for i in range(window)], alternating),
        ("invalid_negative_must_not_enter_average", [257 if i % 2 == 0 else -32768 for i in range(window)], alternating),
        ("distinct_packed_lane_tags", [137*i-500 for i in range(window)], all_valid),
    ]
    vectors = [{"name": f"{name}_{operation}", "values_raw": values, "valid_mask": mask, "operation": operation}
               for name, values, mask in edges for operation in ("max", "avg")]
    # 작은 window는 모든 mask 조합을 검사한다. 합/개수/최대값 중 어느 하나만
    # 다른 mask를 사용하는 실수를 Python builtin sum/max 기준과 대조한다.
    if window <= 5:
        values = [-32768, 32767, -1, 257, -513][:window]
        for mask in range(1 << window):
            for operation in ("max", "avg"):
                vectors.append({"name": f"all_mask_{mask}_{operation}", "values_raw": values,
                                "valid_mask": mask, "operation": operation})
    rng = random.Random(seed + window * 1009)
    for index in range(random_cases):
        # 작은 raw도 섞어 음수 분수 평균, 큰 raw도 섞어 sign/overflow를 검사한다.
        bound = 3 if index % 4 == 0 else 32768
        values = [rng.randrange(-bound, bound) for _ in range(window)]
        mask = 0 if index % 23 == 0 else (all_valid if index % 29 == 0 else rng.randrange(1 << window))
        vectors.append({"name": f"seeded_random_{index}", "values_raw": values,
                        "valid_mask": mask, "operation": "avg" if rng.randrange(2) else "max"})
    return vectors
