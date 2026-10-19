# 의상

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/42578) · Level 2 · Python3

## 문제와 조건 / Task and conditions

옷은 1~30개이며 같은 이름이 없습니다. 이름·종류는 1~20자 소문자 또는 _입니다. 종류당 최대 하나, 전체에서 최소 하나를 입는 조합 수를 반환합니다.

There are 1–30 uniquely named garments; names/categories have 1–20 lowercase letters or underscores. Choose at most one per category and at least one overall; count the outfits.

## 풀이 흐름 / Approach

종류별 옷 수를 셉니다. 한 종류에서 고를 방법은 각각의 옷과 안 입는 경우를 합쳐 count+1개입니다. 종류별 선택을 곱한 뒤 아무것도 입지 않는 한 경우를 뺍니다.

Count clothes per category. Each category offers count+1 choices, including wearing nothing from it. Multiply these independent choices and subtract the all-empty outfit.

## 왜 맞는가 / Why it works

종류마다 최대 하나만 선택하므로 각 의상은 종류별 독립 선택과 일대일 대응합니다. 곱셈 원리로 모든 조합을 세고 금지된 공집합 하나만 제외하면 됩니다.

Every outfit corresponds uniquely to one independent choice per category. The product rule counts all combinations, and only the empty outfit must be removed.

## 비용 / Complexity

시간 O(n), 공간 O(종류 수) / O(n) time, O(number of categories) space

## 구현 / Implementation

[solution.py](solution.py)

```python
from collections import Counter

def solution(clothes):
    # 생성식 for로 이름·종류를 언패킹하고 종류만 Counter로 집계.
    counts = Counter(kind for name, kind in clothes)
    answer = 1
    for count in counts.values():
        # 해당 종류에서 하나 고르는 count가지+안 입는 1가지.
        answer *= count + 1
    return answer - 1
```

## 다른 방법: 선택 수 DP / DP over category choices

새 종류를 처리할 때 기존 의상 유지, 기존 의상에 추가, 새 종류만 입기를 나누어 누적합니다. 같은 O(n) 시간이며 곱셈식이 어떻게 나오는지 확인하기 쉽습니다.

For each category, count keeping old outfits, adding an item to them, and wearing only the new category. It has the same O(n) time and makes the product formula explicit.

[alternative.py](alternative.py)

```python
from collections import Counter

def solution(clothes):
    ways = 0
    for count in Counter(kind for _, kind in clothes).values():
        ways = ways + ways * count + count
    return ways
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    [
      [
        "yellow_hat",
        "headgear"
      ],
      [
        "blue_sunglasses",
        "eyewear"
      ],
      [
        "green_turban",
        "headgear"
      ]
    ]
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

출처: [프로그래머스 문제 42578](https://school.programmers.co.kr/learn/courses/30/lessons/42578), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 42578](https://school.programmers.co.kr/learn/courses/30/lessons/42578), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
