# 산 모양 타일링

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/258705) · Level 3 · Python3

## 문제와 조건 / Task and conditions

1≤n≤100000, tops 길이는 n이며 각 값은 0 또는 1입니다. 삼각형과 마름모로 도형을 채우는 경우 수를 10007로 나눈 나머지로 반환합니다.

1≤n≤100000 and tops has n binary values. Count tilings by triangles and rhombi modulo 10007.

## 풀이 흐름 / Approach

오른쪽 끝 삼각형이 왼쪽과 마름모로 묶였는지에 따라 두 상태를 둡니다. 윗부분 삼각형 유무에 따라 새 끝을 단독으로 두는 방법이 달라집니다. 두 상태만 갱신하며 10007로 나눕니다.

Track two states according to whether the rightmost triangle is paired with its left neighbor as a rhombus. A top triangle changes the number of ways to leave the new end free. Update the two states modulo 10007.

## 정답이 되는 이유 / Why it works

새 오른쪽 삼각형을 왼쪽과 묶는 경우는 이전 두 상태에서 각각 하나씩입니다. 단독으로 두면 이전 끝이 묶였는지와 top 유무에 따라 1+top 또는 2+top개로 나뉩니다. 이 경우들은 서로 겹치지 않고 모든 타일 배치를 포함합니다.

Pairing the new rightmost triangle with its left contributes once from each old state. Leaving it free contributes 1+top or 2+top depending on the old end. These cases are disjoint and exhaustive.

## 비용 / Complexity

시간 O(n), 공간 O(1) / O(n) time, O(1) space

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(n, tops):
    # 문제에서 요구한 나머지 기준 저장.
    modulus = 10007
    joined, free = 0, 1
    # 위쪽 삼각형의 유무 0 또는 1을 왼쪽부터 순회.
    for top in tops:
        next_joined = (joined + free) % modulus
        # 이전 끝이 묶였으면 1+top개, 단독이면 왼쪽과 묶는 방법까지 2+top개로 확장.
        next_free = ((1 + top) * joined + (2 + top) * free) % modulus
        joined, free = next_joined, next_free
    return (joined + free) % modulus
```

## 다른 방법: 삼각형 인접 그래프의 매칭 계수 / Count matchings of the triangle adjacency graph

삼각형 하나는 단독 타일, 붙은 두 삼각형은 마름모입니다. 따라서 작은 도형에서는 인접 그래프의 모든 매칭을 세어 DP와 독립적으로 확인할 수 있습니다. 삼각형 수에 지수적으로 증가합니다.

A single triangle is one tile and two adjacent triangles form a rhombus. Thus all matchings of the small triangle adjacency graph independently verify the DP. Complexity is exponential in the number of triangles.

[alternative_reference.py](alternative_reference.py)

```python
from functools import lru_cache

def solution(n, tops):
    # 아래쪽 지그재그 삼각형은 길이 2n+1의 경로를 이룬다.
    count = 2 * n + 1
    edges = [(i, i + 1) for i in range(count - 1)]
    for i, top in enumerate(tops):
        if top:
            edges.append((2 * i + 1, count))
            count += 1
    adjacent = [0] * count
    for a, b in edges:
        adjacent[a] |= 1 << b
        adjacent[b] |= 1 << a
    @lru_cache(None)
    def ways(mask):
        if not mask:
            return 1
        first = mask & -mask
        i = first.bit_length() - 1
        rest = mask ^ first
        result = ways(rest)
        neighbors = adjacent[i] & rest
        while neighbors:
            bit = neighbors & -neighbors
            neighbors ^= bit
            result += ways(rest ^ bit)
        return result % 10007
    return ways((1 << count) - 1)
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    4,
    [
      1,
      1,
      0,
      1
    ]
  ],
  "output": 149
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 31개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 31 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 31개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 31 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 258705](https://school.programmers.co.kr/learn/courses/30/lessons/258705), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 258705](https://school.programmers.co.kr/learn/courses/30/lessons/258705), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
