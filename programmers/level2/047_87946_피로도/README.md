# 피로도

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/87946) · Level 2 · Python3

피로도 조건을 만족하며 탐험할 수 있는 최대 던전 수를 구합니다.

## 조건과 입출력

입력 매개변수: `k, dungeons`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과입니다.

- k는 1 이상 5,000 이하인 자연수입니다.
- dungeons의 세로(행) 길이(즉, 던전의 개수)는 1 이상 8 이하입니다.
- "최소 필요 피로도"와 "소모 피로도"는 1 이상 1,000 이하인 자연수입니다.

## 풀이를 따라가기

던전 방문 순서를 모든 순열로 만듭니다. 순서대로 현재 피로도가 요구량 이상이면 비용을 빼고 개수를 셉니다. 순열별 최대를 고릅니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
from itertools import permutations

def solution(k, dungeons):
    answer = 0
    # 최대 8개 던전의 모든 방문 순서를 비교한다.
    for order in permutations(dungeons):
        remaining, count = k, 0
        for required, cost in order:
            # 입장 조건을 못 맞추면 해당 순서의 진행은 여기까지다.
            if remaining < required:
                break
            remaining -= cost
            count += 1
        answer = max(answer, count)
    return answer
```

## 정답이 되는 이유

어떤 실제 방문 순서도 나머지 던전을 뒤에 붙인 전체 순열의 접두 부분입니다. 모든 순열을 확인하면 가능한 최대 방문도 포함합니다.

시간 O(N!·N), 공간 O(N) / Time O(N!·N), space O(N)

주의할 점: 입장 요구량과 소모량은 서로 다릅니다. 같은 정보의 던전이 있어도 서로 다른 던전으로 셉니다.

## 다른 방법: 방문 집합 비트마스크 DP

```python
def solution(k,dungeons):
    n=len(dungeons)
    remaining=[-1]*(1<<n)
    remaining[0]=k
    answer=0
    for mask in range(1<<n):
        if remaining[mask]<0: continue
        answer=max(answer,mask.bit_count())
        for i,(required,cost) in enumerate(dungeons):
            if not mask>>i&1 and remaining[mask]>=required:
                remaining[mask|1<<i]=remaining[mask]-cost
    return answer
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 던전 방문 순서를 모든 순열로 만듭니다. 순서대로 현재 피로도가 요구량 이상이면 비용을 빼고 개수를 셉니다. 순열별 최대를 고릅니다. | 방문 집합 비트마스크 DP |
| 비용 | 시간 O(N!·N), 공간 O(N) / Time O(N!·N), space O(N) | 시간 O(N·2^N), 공간 O(2^N) / Time O(N·2^N), space O(2^N) |

## 검증

공식 예제 1개와 생성 입력 40개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Maximize the number of dungeons explored under entry-fatigue requirements.

### Conditions and input/output

Input arguments: `k, dungeons`. The return value is an integer satisfying the task described below.

- 1 ≤ k ≤ 5000; 1 ≤ len(dungeons) ≤ 8
- 1 ≤ consumed fatigue ≤ required fatigue ≤ 1000

### Approach

Enumerate dungeon permutations. Traverse each order while current fatigue meets the next requirement, subtracting its cost and counting visits.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Any feasible partial visit order is a prefix of a full permutation. Enumerating all permutations therefore includes an optimum.

시간 O(N!·N), 공간 O(N) / Time O(N!·N), space O(N)

Boundary cases: Entry requirement and consumed fatigue are distinct. Identical dungeon records still represent different dungeons.

### Alternative: Bitmask DP over visited subsets

시간 O(N·2^N), 공간 O(2^N) / Time O(N·2^N), space O(2^N)

### Verification

Local checks covered 1 official examples and 40 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 피로도](https://school.programmers.co.kr/learn/courses/30/lessons/87946) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
