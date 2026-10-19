# 시소 짝꿍

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/152996) · Level 2 · Python3

좌석 거리 2·3·4에서 토크가 같아질 수 있는 사람 쌍을 센다.

## 조건과 입출력

입력 매개변수: `weights`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과다.

- 2 ≤ weights의 길이 ≤ 100,000
- 100 ≤ weights[i] ≤ 1,000

## 풀이를 따라가기

같은 무게는 c(c−1)/2로 센다. 다른 무게는 작은 쪽 기준 2:1·3:2·4:3 비율만 확인하고 빈도를 곱한다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
from collections import Counter

def solution(weights):
    counts = Counter(weights)
    answer = 0
    for weight, count in counts.items():
        # 같은 무게끼리는 순서 없는 두 사람을 고른다.
        answer += count * (count - 1) // 2
        # 약분한 거리비 중 큰 무게 방향만 확인해 중복을 막는다.
        for numerator, denominator in ((2, 1), (3, 2), (4, 3)):
            if weight * numerator % denominator == 0:
                partner = weight * numerator // denominator
                answer += count * counts[partner]
    return answer
```

## 왜 맞는가

토크는 무게×거리다. 가능한 거리비를 약분하면 위 세 비율과 1:1뿐이며 큰 무게를 한 방향으로만 찾아 중복을 막는다.

평균 시간 O(N+U), 공간 O(U) / Expected time O(N+U), space O(U); U=서로 다른 무게 수 / distinct weights

주의할 점: 부동소수점 비율 대신 나머지와 정수 나눗셈을 쓴다. 같은 사람을 자신과 짝짓지 않는다.

## 다른 방법: 사람 쌍과 거리 조합 전수 확인

이 대안은 작은 입력에서 원리를 비교하는 검증용이다. 최대 제한에 제출할 기본 풀이와 구분한다.

```python
from itertools import combinations

def solution(weights):
    return sum(any(a*x==b*y for x in (2,3,4) for y in (2,3,4)) for a,b in combinations(weights,2))
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 같은 무게는 c(c−1)/2로 센다. 다른 무게는 작은 쪽 기준 2:1·3:2·4:3 비율만 확인하고 빈도를 곱한다. | 사람 쌍과 거리 조합 전수 확인 |
| 비용 | 평균 시간 O(N+U), 공간 O(U) / Expected time O(N+U), space O(U); U=서로 다른 무게 수 / distinct weights | 시간 O(N²), 공간 O(1) / Time O(N²), space O(1) |

## 검증

공식 예제 1개와 생성 입력 71개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다. 제한 상한에 해당하는 크기·수치의 경계 검사도 저장된 테스트에 포함했다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Count pairs whose torques can balance using seat distances 2, 3 and 4.

### Conditions and input/output

Input arguments: `weights`. The return value is an integer satisfying the task described below.

- 2 ≤ len(weights) ≤ 100000; integer force 100 … 1000 N
- seat distances: 2,3,4 m

### Approach

Count equal weights as c(c−1)/2. For unequal weights, check ratios 2:1, 3:2 and 4:3 from the smaller weight and multiply frequencies.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Torque is weight times distance. Reducing all available distance ratios gives exactly these three and 1:1; one-direction lookup avoids double counting.

평균 시간 O(N+U), 공간 O(U) / Expected time O(N+U), space O(U); U=서로 다른 무게 수 / distinct weights

Boundary cases: Use divisibility and integer division rather than floating-point ratios. Never pair a person with themselves.

### Alternative: Check every person pair and distance combination

This alternative is for understanding and checking small inputs; use the main implementation for the full constraints. 시간 O(N²), 공간 O(1) / Time O(N²), space O(1)

The main approach follows the steps described above. The alternative uses check every person pair and distance combination; compare its intermediate state and cost with the main implementation before choosing it.

### Verification

Local checks covered 1 official examples and 71 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases. Saved tests also include a size or numeric boundary at the stated upper limit.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 시소 짝꿍](https://school.programmers.co.kr/learn/courses/30/lessons/152996) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
