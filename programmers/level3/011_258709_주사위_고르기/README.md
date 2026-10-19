# 주사위 고르기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/258709) · Level 3 · Python3

## 문제와 조건 / Task and conditions

주사위는 짝수 2~10개이고 각 6면의 값은 1~100입니다. 절반씩 나눠 굴린 합에서 A가 엄격히 크게 이길 확률이 최대인 1기반 번호들을 오름차순으로 반환합니다.

There are an even 2–10 dice, each with six face values 1–100. Split them equally and maximize the probability that A’s sum is strictly larger. Return the chosen one-based indices sorted.

## 풀이 흐름 / Approach

A의 주사위 절반 조합을 모두 고릅니다. 선택 주사위들의 합별 빈도를 구하고 B의 누적 빈도를 만들어 A의 합보다 작은 B의 경우 수를 셉니다. 무승부는 승리에 포함하지 않습니다.

Enumerate half-size selections for A. Compute sum distributions and a prefix count for B, then count B outcomes strictly below each A sum. Ties do not count as wins.

## 왜 맞는가 / Why it works

각 선택의 전체 굴림 경우 수는 같아 승리 횟수만 비교하면 됩니다. A 합의 빈도에 그보다 작은 B 합의 누적 빈도를 곱해 합하면 모든 승리 쌍을 정확히 한 번 셉니다.

All selections have the same outcome denominator, so maximizing wins suffices. Multiplying each A-sum frequency by the count of smaller B sums counts every winning outcome pair exactly once.

## 비용 / Complexity

조합 수 C(n,n/2), 합 범위 S≤500; 시간 O(C(n,n/2)·nS), 캐시 공간 O(2ⁿS) 상한 / O(C(n,n/2)nS) time, O(2ⁿS) cached-space bound

## 구현 / Implementation

[solution.py](solution.py)

```python
from collections import Counter
from itertools import combinations
from functools import lru_cache

def solution(dice):
    # len은 주사위 개수.
    n = len(dice)

    @lru_cache(None)
    def distribution(indices):
        # 빈 튜플이면 주사위를 고르지 않은 상태.
        if not indices:
            return Counter({0: 1})
        previous = distribution(indices[:-1])
        # 캐시된 previous는 수정하지 않음.
        counts = Counter()
        for total, count in previous.items():
            # 마지막 주사위의 여섯 면을 순회.
            for face in dice[indices[-1]]:
                counts[total + face] += count
        return counts

    best = -1
    answer = []
    # A가 가져갈 절반의 모든 조합 순회.
    for selected in combinations(range(n), n // 2):
        other = tuple(i for i in range(n) if i not in selected)
        # A·B의 합별 경우의 수를 언패킹으로 저장.
        left, right = distribution(selected), distribution(other)
        cumulative = [0]
        # 면 최댓값 100·최대 5개이므로 합은 500 이하.
        for value in range(501):
            cumulative.append(cumulative[-1] + right[value])
        # A의 각 합 경우의 수 × 그보다 작은 B 합 경우의 수.
        wins = sum(count * cumulative[value] for value, count in left.items())
        if wins > best:
            best = wins
            # combinations 순서가 오름차순을 보장.
            answer = [i + 1 for i in selected]
    return answer
```

## 다른 방법: 합 목록 정렬과 이진 탐색 / Sorted roll sums and binary search

각 주사위 조합의 6^(n/2)개 합을 실제로 만들고 B를 정렬합니다. 각 A 합마다 bisect_left로 작은 B 개수를 구합니다. 빈도 압축보다 메모리는 많지만 독립적인 구현입니다.

Enumerate all 6^(n/2) sums and sort B’s list. For each A sum, bisect_left counts smaller B sums. It uses more memory than compressed frequencies but supplies an independent implementation.

[alternative.py](alternative.py)

```python
from bisect import bisect_left
from itertools import combinations, product

def solution(dice):
    n, best, answer = len(dice), -1, []
    for chosen in combinations(range(n), n // 2):
        other = [i for i in range(n) if i not in chosen]
        a = [sum(faces) for faces in product(*(dice[i] for i in chosen))]
        b = sorted(sum(faces) for faces in product(*(dice[i] for i in other)))
        wins = sum(bisect_left(b, value) for value in a)
        if wins > best:
            best, answer = wins, [i + 1 for i in chosen]
    return answer
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    [
      [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      [
        3,
        3,
        3,
        3,
        4,
        4
      ],
      [
        1,
        3,
        3,
        4,
        4,
        4
      ],
      [
        1,
        1,
        4,
        4,
        5,
        5
      ]
    ]
  ],
  "output": [
    1,
    4
  ]
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 13개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 13 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 13개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 13 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 258709](https://school.programmers.co.kr/learn/courses/30/lessons/258709), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 258709](https://school.programmers.co.kr/learn/courses/30/lessons/258709), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
