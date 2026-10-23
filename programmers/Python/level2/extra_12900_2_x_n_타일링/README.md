# 2 x n 타일링

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12900) · Level 2 · Python3

## 문제와 조건 / Task and conditions

1≤n≤60000입니다. 2×n 판을 1×2 또는 2×1 도미노로 채우는 경우 수를 1000000007로 나눈 나머지로 반환합니다.

1≤n≤60000. Count domino tilings of a 2×n board modulo 1000000007.

## 풀이 흐름 / Approach

맨 오른쪽이 세로 도미노 하나로 끝나면 n−1 폭, 가로 도미노 둘로 끝나면 n−2 폭의 문제로 줄어듭니다. 두 경우의 수를 더해 순서대로 계산합니다.

The right end is either one vertical domino, leaving width n−1, or two horizontal dominoes, leaving width n−2. Add these counts iteratively.

## 정답이 되는 이유 / Why it works

2행의 마지막 열은 위 두 형태로만 채울 수 있고 서로 겹치지 않습니다. 따라서 f(n)=f(n−1)+f(n−2), f(0)=f(1)=1입니다.

The final column of a two-row board has exactly these two disjoint cases. Thus f(n)=f(n−1)+f(n−2) with f(0)=f(1)=1.

## 비용 / Complexity

시간 O(n), 공간 O(1) / O(n) time, O(1) space

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(n):
    # 너비 0은 빈 배치 한 가지, 너비 1은 세로 타일 한 가지.
    previous, current = 1, 1
    for _ in range(2, n + 1):
        # 세로 타일 한 장·가로 타일 두 장으로 끝나는 경우의 합.
        previous, current = current, (previous + current) % 1000000007
    return current
```

## 다른 방법: 피보나치 행렬 거듭제곱 / Fibonacci matrix exponentiation

점화식을 [[1,1],[1,0]] 행렬로 나타내고 제곱 분할로 n번 적용합니다. 시간 O(log n), 공간 O(1)이며 매우 큰 n에 유리합니다.

Represent the recurrence with [[1,1],[1,0]] and apply binary exponentiation. It takes O(log n) time and constant matrix space, useful for very large n.

[alternative.py](alternative.py)

```python
def solution(n):
    modulus = 1000000007
    def multiply(a, b):
        return [[sum(a[i][k] * b[k][j] for k in range(2)) % modulus for j in range(2)] for i in range(2)]
    result, matrix = [[1, 0], [0, 1]], [[1, 1], [1, 0]]
    while n:
        if n & 1:
            result = multiply(result, matrix)
        matrix = multiply(matrix, matrix)
        n //= 2
    return result[0][0]
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

원본 채점 기록과 별도로 로컬 검증 29개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 29 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 29개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 29 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 12900](https://school.programmers.co.kr/learn/courses/30/lessons/12900), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 12900](https://school.programmers.co.kr/learn/courses/30/lessons/12900), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
