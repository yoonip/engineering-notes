# 점 찍기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/140107) · Level 2 · Python3

원점에서 거리 d 이내인 음이 아닌 k배수 격자점을 셉니다.

## 조건과 입출력

입력 매개변수: `k, d`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과입니다.

- 1 ≤ k ≤ 1,000,000
- 1 ≤ d ≤ 1,000,000

## 풀이를 따라가기

x를 k씩 늘립니다. y의 최댓값은 floor(sqrt(d²−x²))이고 가능한 k배수 수는 max_y//k+1입니다. x별 개수를 더합니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
from math import isqrt

def solution(k, d):
    answer = 0
    for x in range(0, d + 1, k):
        # 실수 오차 없이 원 안의 최대 정수 y를 구한다.
        max_y = isqrt(d * d - x * x)
        # 0도 가능한 y이므로 개수에 1을 더한다.
        answer += max_y // k + 1
    return answer
```

## 정답이 되는 이유

원 내부 조건 x²+y²≤d²를 y에 대해 정리했습니다. 각 x에서 0을 포함하는 k배수를 정확히 세므로 전체 점을 중복 없이 셉니다.

시간 O(d/k+1), 공간 O(1) / Time O(d/k+1), space O(1)

주의할 점: 원 위의 점과 원점도 포함합니다. isqrt로 정수 경계를 정확히 계산합니다.

## 다른 방법: 단조 감소하는 y 포인터

```python
def solution(k,d):
    top=d//k
    answer=0
    for x in range(d//k+1):
        while k*k*(x*x+top*top)>d*d: top-=1
        answer+=top+1
    return answer
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | x를 k씩 늘립니다. y의 최댓값은 floor(sqrt(d²−x²))이고 가능한 k배수 수는 max_y//k+1입니다. x별 개수를 더합니다. | 단조 감소하는 y 포인터 |
| 비용 | 시간 O(d/k+1), 공간 O(1) / Time O(d/k+1), space O(1) | 시간 O(d/k+1), 공간 O(1) / Time O(d/k+1), space O(1) |

## 검증

공식 예제 2개와 생성 입력 374개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다. 제한 상한에 해당하는 크기·수치의 경계 검사도 저장된 테스트에 포함했습니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Count nonnegative lattice points with both coordinates multiples of k and distance at most d from the origin.

### Conditions and input/output

Input arguments: `k, d`. The return value is an integer satisfying the task described below.

- 1 ≤ k,d ≤ 1000000; coordinates are nonnegative multiples of k

### Approach

Advance x in steps of k. The largest y is floor(sqrt(d²−x²)); there are max_y//k+1 nonnegative multiples of k. Sum across x.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Rearranging x²+y²≤d² gives the y bound. Each x contributes exactly its admissible k multiples, including zero.

시간 O(d/k+1), 공간 O(1) / Time O(d/k+1), space O(1)

Boundary cases: Include the circumference and origin. Use isqrt for an exact integer boundary.

### Alternative: Monotonically decreasing y pointer

시간 O(d/k+1), 공간 O(1) / Time O(d/k+1), space O(1)

### Verification

Local checks covered 2 official examples and 374 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases. Saved tests also include a size or numeric boundary at the stated upper limit.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 점 찍기](https://school.programmers.co.kr/learn/courses/30/lessons/140107) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
