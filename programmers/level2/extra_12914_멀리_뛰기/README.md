# 멀리 뛰기

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12914) · Level 2 · Python3

## 문제와 조건 / Task and conditions

1≤n≤2000입니다. 매번 1칸 또는 2칸 뛰어 n칸 가는 방법 수를 1234567로 나눈 나머지로 반환합니다.

1≤n≤2000. Count sequences of one- or two-step jumps totaling n, modulo 1234567.

## 풀이 흐름 / Approach

마지막 이동이 1칸이면 n−1칸까지의 방법, 2칸이면 n−2칸까지의 방법에서 옵니다. 두 경우는 겹치지 않으므로 더합니다.

A final one-step jump extends a route to n−1, and a final two-step jump extends one to n−2. These disjoint cases are added.

## 정답이 되는 이유 / Why it works

모든 이동열의 마지막 점프는 1 또는 2로 유일하게 구분됩니다. 따라서 f(n)=f(n−1)+f(n−2), f(0)=f(1)=1이며 두 변수로 이 점화식을 계산합니다.

Every route has exactly one final jump of length one or two. Hence f(n)=f(n−1)+f(n−2), with f(0)=f(1)=1, which two rolling variables compute.

## 비용 / Complexity

시간 O(n), 공간 O(1) / O(n) time, O(1) space

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(n):
    # 0칸은 아무것도 안 하는 한 가지, 1칸은 한 번 뛰는 한 가지.
    previous, current = 1, 1
    for _ in range(2, n + 1):
        # %는 나머지.
        previous, current = current, (previous + current) % 1234567
    return current
```

## 다른 방법: 2칸 점프 수별 조합 / Count by the number of double jumps

2칸 점프가 k개면 총 점프 n−k개 중 k자리를 고릅니다. Σ C(n−k,k)를 계산하는 수식 대조입니다. 큰 정수 조합 연산 비용이 있어 주 풀이보다 느릴 수 있습니다.

With k double jumps, choose their k positions among n−k total jumps. Summing C(n−k,k) provides a combinatorial cross-check, with large-integer combination overhead.

[alternative.py](alternative.py)

```python
from math import comb

def solution(n):
    return sum(comb(n - doubles, doubles) for doubles in range(n // 2 + 1)) % 1234567
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    4
  ],
  "output": 5
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

출처: [프로그래머스 문제 12914](https://school.programmers.co.kr/learn/courses/30/lessons/12914), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 12914](https://school.programmers.co.kr/learn/courses/30/lessons/12914), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
