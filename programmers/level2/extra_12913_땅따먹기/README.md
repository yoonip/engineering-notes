# 땅따먹기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12913) · Level 2 · Python3

## 문제와 조건 / Task and conditions

행은 1~100000개, 열은 4개, 점수는 1~100입니다. 행마다 하나를 고르되 같은 열을 연속 선택하지 않을 때 최대 점수를 반환합니다.

There are 1–100000 rows, four columns and scores in [1,100]. Choose one cell per row without repeating a column consecutively; return the maximum sum.

## 풀이 흐름 / Approach

현재 행의 각 칸에 도달한 최댓값 네 개만 유지합니다. 같은 열을 연속으로 밟을 수 없으므로 새 칸에는 직전 행의 다른 세 열 중 최댓값을 더합니다.

Maintain only four best scores for the current row. Since consecutive selections cannot share a column, add the best of the other three previous columns.

## 왜 맞는가 / Why it works

현재 열이 정해지면 이전 경로의 영향은 직전 열과 최대 점수뿐입니다. 가능한 세 이전 열을 모두 비교하는 DP가 모든 유효 경로의 최댓값을 보존합니다.

Once the current column is fixed, a prefix matters only through its previous column and best score. Comparing all three legal predecessor columns preserves the optimal score.

## 비용 / Complexity

행 r에 시간 O(r), 공간 O(1) / O(r) time, O(1) space

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(land):
    # 직전 행의 0~3열에 도착한 최대 점수 네 개를 저장하는 동적 계획법(DP) 상태.
    a = b = c = d = 0
    for first, second, third, fourth in land:
        # 오른쪽 네 식을 전부 이전 값으로 계산한 뒤 동시에 갱신.
        a, b, c, d = (
            first + max(b, c, d),
            # 쉼표는 튜플 원소 구분.
            second + max(a, c, d),
            third + max(a, b, d),
            # 고정된 네 계산으로 내부 반복 비용 절감.
            fourth + max(a, b, c),
        )
    return max(a, b, c, d)
```

## 다른 방법: 전체 경로 DFS / Enumerate all legal column paths

다른 열로 이동하는 모든 경로를 직접 탐색합니다. 시간 O(4·3ʳ⁻¹)이라 몇 행짜리 작은 입력에서 DP 정답을 확인하는 용도입니다.

Enumerate every path that changes columns. The O(4·3^(r−1)) time limits this direct oracle to a few rows.

[alternative_reference.py](alternative_reference.py)

```python
def solution(land):
    def visit(row, previous):
        if row == len(land):
            return 0
        return max(land[row][col] + visit(row + 1, col) for col in range(4) if col != previous)
    return visit(0, -1)
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    [
      [
        1,
        2,
        3,
        5
      ],
      [
        5,
        6,
        7,
        8
      ],
      [
        4,
        3,
        2,
        1
      ]
    ]
  ],
  "output": 16
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

출처: [프로그래머스 문제 12913](https://school.programmers.co.kr/learn/courses/30/lessons/12913), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 12913](https://school.programmers.co.kr/learn/courses/30/lessons/12913), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

큰 입력 검사: 10만 행에서 열 4·3 교대 / Alternate columns 4 and 3 across one hundred thousand rows

```bash
python verify_stress.py
```
