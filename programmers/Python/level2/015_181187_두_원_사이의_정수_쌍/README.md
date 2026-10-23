# 두 원 사이의 정수 쌍

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/181187) · Level 2 · Python3

두 동심원 사이에서 경계를 포함하는 정수 좌표 수를 셉니다.

## 조건과 입출력

입력 매개변수: `r1, r2`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과입니다.

- 1 ≤ r1 < r2 ≤ 1,000,000

## 풀이를 따라가기

양의 x마다 바깥원의 y 최댓값을 정수 제곱근으로 구합니다. 안쪽원 바깥에 있어야 하므로 y 최솟값은 제곱근의 올림입니다. 첫 사분면의 y=0을 포함한 수를 네 배 합니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
from math import isqrt

def solution(r1, r2):
    answer = 0
    for x in range(1, r2 + 1):
        # 바깥원 안에 들어오는 y의 정수 최댓값이다.
        high = isqrt(r2 * r2 - x * x)
        inner = max(0, r1 * r1 - x * x)
        low = isqrt(inner)
        # 안쪽원 바깥 조건은 제곱근의 올림이다.
        if low * low < inner:
            low += 1
        answer += high - low + 1
    # 양의 x·음이 아닌 y 영역을 네 번 회전하면 전체를 중복 없이 센다.
    return answer * 4
```

## 정답이 되는 이유

x>0,y≥0 구역은 90도 회전으로 전체를 중복 없이 네 부분으로 나눕니다. 각 x에서 유효 y는 연속 정수 구간이므로 양 끝 차이+1로 셉니다.

시간 O(r2), 공간 O(1)개의 정수 / Time O(r2), space O(1) integers

주의할 점: 경계는 포함합니다. 안쪽 식이 음수이면 y 최솟값은 0입니다. 부동소수점 sqrt의 반올림에 의존하지 않습니다.

## 다른 방법: 격자 좌표 전수 확인 · 작은 반지름

이 대안은 작은 입력에서 원리를 비교하는 검증용입니다. 최대 제한에 제출할 기본 풀이와 구분합니다.

```python
def solution(r1,r2):
    return sum(r1*r1 <= x*x+y*y <= r2*r2 for x in range(-r2,r2+1) for y in range(-r2,r2+1))
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 양의 x마다 바깥원의 y 최댓값을 정수 제곱근으로 구합니다. 안쪽원 바깥에 있어야 하므로 y 최솟값은 제곱근의 올림입니다. 첫 사분면의 y=0을 포함한 수를 네 배 합니다. | 격자 좌표 전수 확인 · 작은 반지름 |
| 비용 | 시간 O(r2), 공간 O(1)개의 정수 / Time O(r2), space O(1) integers | 시간 O(r2²), 공간 O(1) / Time O(r2²), space O(1) |

## 검증

공식 예제 1개와 생성 입력 171개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Count integer lattice points between two concentric circles, including both boundaries.

### Conditions and input/output

Input arguments: `r1, r2`. The return value is an integer satisfying the task described below.

- 1 ≤ r1 < r2 ≤ 1000000; both circular boundaries are included

### Approach

For each positive x, use integer square roots for the maximum outer-circle y and the ceiling of the inner-circle y. Count nonnegative y values and multiply by four.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

The region x>0,y≥0 partitions the lattice points into four disjoint rotations. Valid y values at each x form one contiguous integer interval.

시간 O(r2), 공간 O(1)개의 정수 / Time O(r2), space O(1) integers

Boundary cases: Include boundaries. A negative inner radicand gives a minimum y of zero. Avoid floating-point square-root rounding.

### Alternative: Exhaustive lattice-point counting for small radii

This alternative is for understanding and checking small inputs; use the main implementation for the full constraints. 시간 O(r2²), 공간 O(1) / Time O(r2²), space O(1)

### Verification

Local checks covered 1 official examples and 171 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 두 원 사이의 정수 쌍](https://school.programmers.co.kr/learn/courses/30/lessons/181187) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
