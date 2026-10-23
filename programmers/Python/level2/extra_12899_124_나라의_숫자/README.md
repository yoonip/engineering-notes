# 124 나라의 숫자

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12899) · Level 2 · Python3

## 문제와 조건 / Task and conditions

1≤n≤50000000입니다. 1,2,4만 자릿수로 쓰는 수 체계에서 n을 표현한 문자열을 반환합니다.

1≤n≤50000000. Return n in the numeral system using only digits 1,2,4.

## 풀이 흐름 / Approach

각 자릿수에 0이 없는 3진법입니다. n−1을 3으로 나눈 나머지 0·1·2를 문자 1·2·4로 대응시키고 몫에서 같은 과정을 반복합니다.

This is bijective base three, with no zero digit. Divide n−1 by three, map remainders 0,1,2 to 1,2,4, and repeat on the quotient.

## 정답이 되는 이유 / Why it works

끝자리 1·2·4는 차례대로 세 개씩 반복됩니다. 1을 뺀 뒤 나누면 3의 배수일 때 필요한 자리 빌림까지 함께 처리되어 각 양의 정수와 표현이 일대일 대응합니다.

The last digits 1,2,4 cycle in groups of three. Subtracting one before division correctly handles borrowing at multiples of three, giving a bijection with positive integers.

## 비용 / Complexity

시간·출력 공간 O(log₃n) / O(log₃n) time and output space

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(n):
    digits = []
    while n > 0:
        # 1을 빼서 1·2·4를 0·1·2 인덱스로 대응시키는 0 없는 3진법 처리.
        n, remainder = divmod(n - 1, 3)
        digits.append('124'[remainder])
    return ''.join(reversed(digits))
```

## 다른 방법: 자릿수별 구간 순위 / Rank within fixed-length blocks

한 자리 3개, 두 자리 9개처럼 길이별 구간을 먼저 찾습니다. 그 구간의 0기반 순위를 일반 3진수로 바꾸고 0·1·2를 1·2·4로 치환합니다.

Find the length block of sizes 3,9,27,…, then express the zero-based rank within it in ordinary base three and map digits to 1,2,4.

[alternative.py](alternative.py)

```python
def solution(n):
    length, block = 1, 3
    while n > block:
        n -= block
        length += 1
        block *= 3
    rank, result = n - 1, ['1'] * length
    for i in range(length - 1, -1, -1):
        rank, digit = divmod(rank, 3)
        result[i] = '124'[digit]
    return ''.join(result)
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    1
  ],
  "output": "1"
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 32개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 32 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 32개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 32 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 12899](https://school.programmers.co.kr/learn/courses/30/lessons/12899), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 12899](https://school.programmers.co.kr/learn/courses/30/lessons/12899), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
