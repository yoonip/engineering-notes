# 가장 큰 수

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/42746) · Level 2 · Python3

## 문제와 조건 / Task and conditions

정수는 1~100000개이고 각각 0~1000입니다. 모든 수를 한 번씩 이어 붙인 최댓값을 문자열로 반환합니다.

There are 1–100000 integers in [0,1000]. Concatenate every value once and return the largest result as a string.

## 풀이 흐름 / Approach

숫자를 문자열로 바꾸고 이어 붙였을 때 큰 순서를 먼저 배치합니다. 문제의 각 숫자는 최대 네 자리이므로 반복한 문자열 키로 비교할 수 있습니다. 모든 값이 0이면 결과도 0 하나입니다.

Convert numbers to strings and order them so that earlier concatenations are larger. Under the problem’s at-most-four-digit bound, repeated-string keys determine this order. Collapse an all-zero result to one zero.

## 정답이 되는 이유 / Why it works

인접한 a,b에서 ab가 ba보다 작다면 순서를 바꾸는 것이 전체 수를 키웁니다. ab≥ba인 순서로 정렬하면 이런 역전이 없어 최댓값을 얻습니다.

If adjacent strings satisfy ab<ba, swapping them increases the whole concatenation. Sorting by ab versus ba removes every such inversion and yields the maximum.

## 비용 / Complexity

최대 자릿수 d에 시간 O(nd log n), 공간 O(nd) / O(nd log n) time, O(nd) space

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(numbers):
    # map은 각 원소에 str을 적용해 문자열 변환, list는 목록으로 저장.
    parts = list(map(str, numbers))
    parts.sort(key=lambda value: value * 4, reverse=True)
    # 가장 앞이 0이면 모든 수가 0.
    if parts[0] == '0':
        return '0'
    return ''.join(parts)
```

## 다른 방법: 연결 결과 직접 비교 / Direct concatenation comparator

a+b와 b+a를 직접 비교합니다. 반복 횟수가 입력의 자릿수 상한에 의존하지 않아 더 일반적이지만 Python 비교 함수 호출 비용이 있습니다.

Compare a+b with b+a directly. This is independent of any fixed digit limit, although Python comparator calls add overhead.

[alternative.py](alternative.py)

```python
from functools import cmp_to_key

def solution(numbers):
    parts = list(map(str, numbers))
    def compare(a, b):
        return (a + b < b + a) - (a + b > b + a)
    parts.sort(key=cmp_to_key(compare))
    return '0' if parts[0] == '0' else ''.join(parts)
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    [
      6,
      10,
      2
    ]
  ],
  "output": "6210"
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

출처: [프로그래머스 문제 42746](https://school.programmers.co.kr/learn/courses/30/lessons/42746), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 42746](https://school.programmers.co.kr/learn/courses/30/lessons/42746), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
