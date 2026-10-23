# 행렬의 곱셈

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12949) · Level 2 · Python3

## 문제와 조건 / Task and conditions

각 행렬의 행·열은 2~100이며 원소 범위는 −10~20입니다. 안쪽 차원이 같은 입력만 주어집니다. arr1×arr2를 반환합니다.

Each matrix dimension is 2–100 and entries are in [−10,20]. Inner dimensions always agree. Return arr1×arr2.

## 풀이 흐름 / Approach

두 번째 행렬을 열 단위로 바꿔 각 행·열의 같은 위치끼리 곱해 더합니다. 결과 (i,j)는 첫 행렬 i행과 둘째 행렬 j열의 내적입니다.

Transpose the second matrix into columns and sum pairwise products for each row-column pair. Entry (i,j) is the dot product of row i and column j.

## 정답이 되는 이유 / Why it works

행렬 곱의 정의 C[i,j]=Σ A[i,k]B[k,j]를 그대로 계산합니다. 전치는 원소의 위치 표현만 바꾸므로 내적에 필요한 k 순서가 유지됩니다.

The implementation directly evaluates C[i,j]=Σ A[i,k]B[k,j]. Transposition changes storage layout while preserving the k order needed for each dot product.

## 비용 / Complexity

a×b와 b×c 입력에 시간 O(abc), 출력 외 공간 O(bc) / O(abc) time, O(bc) auxiliary space besides output

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(arr1, arr2):
    # arr2의 열들을 튜플로 모아 list로 변환.
    columns = list(zip(*arr2))
    answer = []
    for row in arr1:
        # 현재 결과 행을 담는 리스트.
        result_row = []
        for column in columns:
            # sum은 생성식의 곱들을 모두 합산하는 내적 계산.
            value = sum(a * b for a, b in zip(row, column))
            result_row.append(value)
        # 완성된 한 행을 결과 행렬에 추가.
        answer.append(result_row)
    return answer
```

## 다른 방법: 삼중 반복의 누적 곱 / Triple-loop accumulation

전치 없이 A[i,k]를 고정하고 결과 행에 B[k,j]의 배수를 더합니다. 같은 O(abc) 시간이며 별도의 전치 사본이 없습니다.

Fix A[i,k] and add its multiple of row B[k] into the result. It keeps O(abc) time without an extra transposed copy.

[alternative.py](alternative.py)

```python
def solution(arr1, arr2):
    result = [[0] * len(arr2[0]) for _ in arr1]
    for i, row in enumerate(arr1):
        for k, value in enumerate(row):
            for j, other in enumerate(arr2[k]):
                result[i][j] += value * other
    return result
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
        4
      ],
      [
        3,
        2
      ],
      [
        4,
        1
      ]
    ],
    [
      [
        3,
        3
      ],
      [
        3,
        3
      ]
    ]
  ],
  "output": [
    [
      15,
      15
    ],
    [
      15,
      15
    ],
    [
      15,
      15
    ]
  ]
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

출처: [프로그래머스 문제 12949](https://school.programmers.co.kr/learn/courses/30/lessons/12949), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 12949](https://school.programmers.co.kr/learn/courses/30/lessons/12949), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
