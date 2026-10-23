# 카펫

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/42842) · Level 2 · Python3

## 문제와 조건 / Task and conditions

brown은 8~5000, yellow는 1~2000000입니다. 갈색 한 줄이 노란 내부를 둘러싸며 가로≥세로인 [가로,세로]를 반환합니다.

brown is 8–5000 and yellow is 1–2000000. A one-cell brown border surrounds the yellow interior. Return [width,height] with width≥height.

## 풀이 흐름 / Approach

전체 넓이 brown+yellow의 약수 쌍을 찾습니다. 바깥 한 줄을 제외한 안쪽 넓이가 yellow인지 확인합니다. 가로가 세로보다 길거나 같으므로 세로는 전체 넓이의 제곱근까지만 봅니다.

Enumerate factor pairs of brown+yellow. Removing the one-cell border must leave exactly yellow interior cells. Since width is at least height, test heights only up to the square root.

## 정답이 되는 이유 / Why it works

정답의 가로·세로는 전체 넓이의 약수 쌍이며 내부 넓이는 (w−2)(h−2)입니다. 모든 가능한 세로를 검사하므로 조건을 만족하는 정답 쌍을 놓치지 않습니다.

The answer is a factor pair of the total area with interior (w−2)(h−2). Enumerating every possible height covers every valid rectangle.

## 비용 / Complexity

시간 O(√(brown+yellow)), 공간 O(1) / O(√(brown+yellow)) time, O(1) space

## 구현 / Implementation

[solution.py](solution.py)

```python
from math import isqrt

def solution(brown, yellow):
    # 전체 카펫 넓이 계산.
    area = brown + yellow
    for height in range(3, isqrt(area) + 1):
        # 전체 넓이를 나눌 수 있는 세로 길이인지 검사.
        if area % height == 0:
            width = area // height
            # 테두리 한 칸씩을 뺀 내부 넓이 검사.
            if (width - 2) * (height - 2) == yellow:
                return [width, height]
```

## 다른 방법: 둘레와 이차방정식 / Perimeter and an integer quadratic

brown=2w+2h−4에서 w+h를 구하고 wh=전체 넓이와 함께 이차방정식을 풉니다. isqrt로 판별식을 처리해 부동소수점 오차를 피합니다.

Use brown=2w+2h−4 to obtain w+h, then solve the quadratic with wh equal to the total area. Integer square roots avoid floating-point rounding.

[alternative.py](alternative.py)

```python
from math import isqrt

def solution(brown, yellow):
    total_side = (brown + 4) // 2
    difference = isqrt(total_side * total_side - 4 * (brown + yellow))
    return [(total_side + difference) // 2, (total_side - difference) // 2]
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    10,
    2
  ],
  "output": [
    4,
    3
  ]
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

출처: [프로그래머스 문제 42842](https://school.programmers.co.kr/learn/courses/30/lessons/42842), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 42842](https://school.programmers.co.kr/learn/courses/30/lessons/42842), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
