# 줄 서는 방법

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12936) · Level 2 · Python3

## 문제와 조건 / Task and conditions

1≤n≤20,1≤k≤n!입니다. 1~n의 모든 순열을 사전순으로 놓았을 때 1기반 k번째 배열을 반환합니다.

1≤n≤20 and 1≤k≤n!. Return the one-based k-th lexicographic permutation of 1 through n.

## 풀이 흐름 / Approach

맨 앞 숫자가 같은 순열은 (n−1)!개씩 묶입니다. k를 0기반으로 바꾸고 묶음 크기로 나눈 몫으로 다음 숫자를 고릅니다. 나머지는 그 묶음 안에서의 순서입니다.

Permutations sharing their first element form blocks of (n−1)!. Convert k to zero-based indexing, use the quotient to select the next element, and carry the remainder into that block.

## 정답이 되는 이유 / Why it works

사전순에서 선택 가능한 숫자마다 같은 크기의 순열 구간이 연속합니다. 몫·나머지로 정확한 구간을 고르는 과정을 반복하므로 k번째 순열을 유일하게 복원합니다.

Lexicographic permutations are partitioned into equal contiguous blocks by their next element. Repeated quotient/remainder selection uniquely reconstructs the k-th permutation.

## 비용 / Complexity

리스트 삭제 포함 시간 O(n²), 공간 O(n) / O(n²) time with list deletions, O(n) space

## 구현 / Implementation

[solution.py](solution.py)

```python
from math import factorial

def solution(n, k):
    # 아직 배치하지 않은 번호를 오름차순으로 보관.
    available = list(range(1, n + 1))
    answer = []
    k -= 1
    block = factorial(n)
    # 남은 사람 수를 n부터 1까지 줄임.
    for remaining in range(n, 0, -1):
        block //= remaining
        # 몫은 선택할 번호 위치, 나머지는 그 묶음 안 순번.
        index, k = divmod(k, block)
        answer.append(available.pop(index))
    return answer
```

## 다른 방법: 사전순 순열 직접 생성 / Enumerate lexicographic permutations

작은 n에서는 permutations의 k번째 항을 직접 고를 수 있습니다. 시간 O(k·n)이라 n이 큰 제출용이 아닌 기준 구현입니다.

For small n, directly select the k-th lexicographic permutation. O(kn) time makes it a reference implementation rather than the large-input submission.

[alternative_reference.py](alternative_reference.py)

```python
from itertools import islice, permutations

def solution(n, k):
    return list(next(islice(permutations(range(1, n + 1)), k - 1, None)))
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    3,
    5
  ],
  "output": [
    3,
    1,
    2
  ]
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 29개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 29 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 29개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 29 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 12936](https://school.programmers.co.kr/learn/courses/30/lessons/12936), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 12936](https://school.programmers.co.kr/learn/courses/30/lessons/12936), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
