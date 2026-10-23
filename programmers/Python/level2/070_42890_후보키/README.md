# 후보키

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/42890) · Level 2 · Python3

## 문제와 조건 / Task and conditions

행은 1~20개, 열은 1~8개이고 전체 행은 중복되지 않습니다. 값은 1~8자 소문자·숫자입니다. 유일성과 최소성을 함께 만족하는 컬럼 집합 수를 반환합니다.

There are 1–20 distinct rows and 1–8 columns; cell strings have 1–8 lowercase letters/digits. Count column sets satisfying both uniqueness and minimality.

## 풀이 흐름 / Approach

컬럼 조합을 작은 크기부터 확인합니다. 이미 찾은 후보키를 포함하는 조합은 최소성을 어기므로 건너뜁니다. 남은 조합에서 각 행의 선택 컬럼 튜플이 모두 다른지 검사합니다.

Inspect column combinations in increasing size. Skip any combination containing an existing candidate key, then test uniqueness using tuples of the selected values.

## 정답이 되는 이유 / Why it works

작은 조합부터 찾으므로 새 조합에 포함될 수 있는 더 작은 키는 이미 검사했습니다. 그 키를 포함하지 않고 행들을 모두 구별하는 조합만 채택하므로 유일성과 최소성이 함께 성립합니다.

All smaller possible keys have already been considered. Accepting only unique combinations with no existing key subset establishes both uniqueness and minimality.

## 비용 / Complexity

컬럼 c, 행 r에 대략 O(2ᶜ·r·c+4ᶜ), 공간 O(rc+2ᶜc) 상한 / Conservative O(2ᶜrc+4ᶜ) time, O(rc+2ᶜc) space

## 구현 / Implementation

[solution.py](solution.py)

```python
from itertools import combinations

def solution(relation):
    # 행 수·열 수 각각 대입.
    rows, columns = len(relation), len(relation[0])
    keys = []
    for size in range(1, columns + 1):
        # 열 번호에서 size개를 선택한 튜플 순회.
        for selected in combinations(range(columns), size):
            selected_set = set(selected)
            # 기존 후보키를 포함하면 최소성 위반.
            if any(key <= selected_set for key in keys):
                continue
            values = {tuple(row[column] for column in selected) for row in relation}
            # 모든 행의 묶음이 서로 다르면 유일성 만족.
            if len(values) == rows:
                keys.append(selected_set)
    return len(keys)
```

## 다른 방법: 비트마스크와 단일 컬럼 제거 검사 / Bitmask uniqueness and minimality

모든 조합의 유일성을 먼저 계산합니다. 유일한 조합에서 컬럼 하나를 뺀 모든 조합이 유일하지 않을 때만 키입니다. 유일성은 상위 집합으로 이어지므로 한 컬럼 제거만으로 충분합니다.

Compute uniqueness for every bitmask first. A unique mask is minimal exactly when deleting any selected column makes it non-unique, because uniqueness is upward closed.

[alternative.py](alternative.py)

```python
def solution(relation):
    c = len(relation[0])
    unique = [False] * (1 << c)
    for mask in range(1, 1 << c):
        values = {tuple(row[j] for j in range(c) if mask >> j & 1) for row in relation}
        unique[mask] = len(values) == len(relation)
    return sum(unique[mask] and all(not unique[mask ^ (1 << j)] for j in range(c) if mask >> j & 1)
               for mask in range(1, 1 << c))
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    [
      [
        "100",
        "ryan",
        "music",
        "2"
      ],
      [
        "200",
        "apeach",
        "math",
        "2"
      ],
      [
        "300",
        "tube",
        "computer",
        "3"
      ],
      [
        "400",
        "con",
        "computer",
        "4"
      ],
      [
        "500",
        "muzi",
        "music",
        "3"
      ],
      [
        "600",
        "apeach",
        "music",
        "2"
      ]
    ]
  ],
  "output": 2
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

출처: [프로그래머스 문제 42890](https://school.programmers.co.kr/learn/courses/30/lessons/42890), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 42890](https://school.programmers.co.kr/learn/courses/30/lessons/42890), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
