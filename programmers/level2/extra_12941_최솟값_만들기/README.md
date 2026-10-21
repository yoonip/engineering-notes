# 최솟값 만들기

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12941) · Level 2 · Python3

## 문제와 조건 / Task and conditions

두 배열 길이는 같은 1~1000이며 값은 1~1000입니다. 각 원소를 한 번씩 짝지어 곱한 합의 최솟값을 반환합니다.

Both arrays have equal length 1–1000 and entries in [1,1000]. Pair each entry exactly once and minimize the sum of products.

## 풀이 흐름 / Approach

한 배열은 오름차순, 다른 배열은 내림차순으로 정렬해 같은 위치끼리 곱합니다. 큰 수에 작은 수를 대응시켜 큰 곱이 여러 번 겹치는 것을 피합니다.

Sort one array ascending and the other descending, then multiply corresponding entries. Pairing large values with small ones minimizes the sum.

## 정답이 되는 이유 / Why it works

a≤b, x≤y일 때 ax+by−(ay+bx)=(b−a)(y−x)≥0입니다. 같은 방향의 짝을 반대로 교환하면 합이 늘지 않으므로 반대 정렬이 최솟값입니다.

For a≤b and x≤y, ax+by−(ay+bx)=(b−a)(y−x)≥0. Replacing aligned pairs by opposite pairs never increases the sum, proving opposite sorting optimal.

## 비용 / Complexity

시간 O(n log n), 공간 O(n) / O(n log n) time, O(n) space

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(A, B):
    # A의 작은 값부터 사용.
    small_first = sorted(A)
    large_first = sorted(B, reverse=True)
    return sum(a * b for a, b in zip(small_first, large_first))
```

## 다른 방법: 모든 대응 순열 / Enumerate all pairings

두 번째 배열의 모든 순열을 비교하면 정의 그대로 최솟값을 구합니다. 시간 O(n!n)이라 작은 배열에서 교환 논증을 검증하는 용도입니다.

Try every permutation of the second array and take the smallest sum. O(n!n) time limits this direct optimality oracle to small arrays.

[alternative_reference.py](alternative_reference.py)

```python
from itertools import permutations

def solution(A, B):
    return min(sum(a * b for a, b in zip(A, order)) for order in permutations(B))
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    [
      1,
      4,
      2
    ],
    [
      5,
      4,
      4
    ]
  ],
  "output": 29
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 30개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 30 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 30개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 30 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 12941](https://school.programmers.co.kr/learn/courses/30/lessons/12941), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 12941](https://school.programmers.co.kr/learn/courses/30/lessons/12941), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
