# 귤 고르기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/138476) · Level 2 · Python3

k개 귤을 고를 때 서로 다른 크기 수를 최소화한다.

## 조건과 입출력

입력 매개변수: `k, tangerine`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과다.

- 1 ≤ k ≤ tangerine의 길이 ≤ 100,000
- 1 ≤ tangerine의 원소 ≤ 10,000,000

## 풀이를 따라가기

크기별 개수를 센 뒤 개수가 큰 순으로 고른다. 누적 개수가 k에 도달한 시점의 종류 수를 반환한다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
from collections import Counter

def solution(k, tangerine):
    # 많이 남은 크기부터 골라 종류 수를 줄인다.
    counts = sorted(Counter(tangerine).values(), reverse=True)
    for kinds, count in enumerate(counts, 1):
        k -= count
        if k <= 0:
            return kinds
```

## 왜 맞는가

종류 수가 같은 선택 중에는 가장 많은 빈도부터 고른 선택의 합이 최대다. 그러므로 그 선택조차 k에 못 미치면 같은 수의 다른 종류 조합도 불가능하다.

시간 O(N+U log U), 공간 O(U) / Time O(N+U log U), space O(U)

주의할 점: 마지막 크기는 필요한 만큼만 골라도 한 종류다. 귤 크기 자체의 대소는 목표와 무관하다.

## 다른 방법: 빈도별 버킷 집계

기본 풀이와 같은 결과를 구하되 중간 상태와 계산 방식이 다르다.

```python
from collections import Counter

def solution(k,tangerine):
    bucket=[0]*(len(tangerine)+1)
    for count in Counter(tangerine).values(): bucket[count]+=1
    used=0
    for frequency in range(len(tangerine),0,-1):
        take=min(bucket[frequency],(k+frequency-1)//frequency)
        used+=take
        k-=take*frequency
        if k<=0: return used
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 크기별 개수를 센 뒤 개수가 큰 순으로 고른다. 누적 개수가 k에 도달한 시점의 종류 수를 반환한다. | 빈도별 버킷 집계 |
| 비용 | 시간 O(N+U log U), 공간 O(U) / Time O(N+U log U), space O(U) | 시간 O(N+U), 공간 O(N+U) / Time O(N+U), space O(N+U) |

## 검증

공식 예제 3개와 생성 입력 70개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Choose k tangerines while minimizing the number of distinct sizes.

### Conditions and input/output

Input arguments: `k, tangerine`. The return value is an integer satisfying the task described below.

- 1 ≤ k ≤ len(tangerine) ≤ 100000; 1 ≤ size ≤ 10000000

### Approach

Count each size and consume the largest frequencies first. Return the number of sizes when their total reaches k.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

For a fixed number of types, choosing the largest frequencies maximizes available fruit. If that sum is insufficient, no other selection of that many types can work.

시간 O(N+U log U), 공간 O(U) / Time O(N+U log U), space O(U)

Boundary cases: Only part of the last size may be needed, but it still counts as one type. Numeric size order is irrelevant.

### Alternative: Bucket counts by frequency

It computes the same result using different intermediate states or evaluation steps. 시간 O(N+U), 공간 O(N+U) / Time O(N+U), space O(N+U)

The main approach follows the steps described above. The alternative uses bucket counts by frequency; compare its intermediate state and cost with the main implementation before choosing it.

### Verification

Local checks covered 3 official examples and 70 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 귤 고르기](https://school.programmers.co.kr/learn/courses/30/lessons/138476) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
