# 숫자 블록

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12923) · Level 2 · Python3

## 문제와 조건 / Task and conditions

1≤begin≤end≤1000000000, end−begin≤5000입니다. 블록 번호는 최대 10000000이며 자기 위치를 제외한 배수 위치를 차례로 덮습니다. 해당 구간의 최종 번호를 반환합니다.

1≤begin≤end≤1000000000 and end−begin≤5000. Block labels are capped at 10000000 and overwrite their multiples except their own position. Return final labels in the interval.

## 풀이 흐름 / Approach

수 v를 덮는 블록 번호는 v의 약수 중 자기 자신을 제외하고 10000000 이하인 최댓값입니다. 작은 약수를 찾으면 짝 약수 v//약수가 더 크므로 먼저 확인합니다. 짝이 상한을 넘으면 작은 쪽을 후보로 남깁니다.

The final block at v is the largest proper divisor of v not exceeding 10000000. For each small divisor, inspect its larger paired divisor first; if that exceeds the cap, retain the smaller divisor as a candidate.

## 정답이 되는 이유 / Why it works

블록 b는 자기 위치가 아닌 2b,3b,…를 덮고 큰 번호가 나중에 덮습니다. 따라서 답은 제한 안의 최대 진약수입니다. 약수 쌍을 제곱근까지 검사하면 모든 후보를 다룹니다.

Block b covers 2b,3b,…, and larger labels overwrite later. Thus the answer is the largest allowed proper divisor. Testing divisor pairs up to the square root covers every candidate.

## 비용 / Complexity

구간 길이 q에 시간 O(q√end), 공간 O(q) / O(q√end) time, O(q) output space

## 구현 / Implementation

[solution.py](solution.py)

```python
from math import isqrt

def solution(begin, end):
    answer = []
    # range는 끝 제외이므로 end+1로 마지막 위치까지 포함.
    for value in range(begin, end + 1):
        if value == 1:
            # 초기값 0 유지.
            answer.append(0)
            continue
        block = 1
        for divisor in range(2, isqrt(value) + 1):
            # 나누어떨어지면 약수 쌍 발견.
            if value % divisor == 0:
                partner = value // divisor
                # 실제 존재하는 블록 번호의 최대값 천만 이하인지 검사.
                if partner <= 10000000:
                    block = partner
                    break
                # 이 후보를 놓치면 소수의 큰 배수에서 틀림.
                block = divisor
        answer.append(block)
    return answer
```

## 다른 방법: 작은 범위의 직접 덮어쓰기 / Direct block painting on a small range

각 블록 번호의 두 번째 배수부터 직접 덮습니다. 문제의 설치 규칙을 그대로 따르는 독립 검증이며 큰 end에는 사용하지 않습니다.

Paint multiples starting at twice each block label. This independently follows the installation rule and is only suitable for small end values.

[alternative_reference.py](alternative_reference.py)

```python
def solution(begin, end):
    answer = [0] * (end - begin + 1)
    for block in range(1, min(10000000, end // 2) + 1):
        first = max(2 * block, ((begin + block - 1) // block) * block)
        for position in range(first, end + 1, block):
            answer[position - begin] = block
    return answer
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    1,
    10
  ],
  "output": [
    0,
    1,
    1,
    2,
    1,
    3,
    1,
    4,
    3,
    5
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

출처: [프로그래머스 문제 12923](https://school.programmers.co.kr/learn/courses/30/lessons/12923), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 12923](https://school.programmers.co.kr/learn/courses/30/lessons/12923), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
