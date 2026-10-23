# n^2 배열 자르기

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/87390) · Level 2 · Python3

n×n 규칙 배열을 펼친 뒤 필요한 인덱스 구간만 반환합니다.

## 조건과 입출력

입력 매개변수: `n, left, right`. 반환값은 수치 배열이며 아래 풀이의 조건을 만족하는 결과입니다.

- 1 ≤ n ≤ 10^7
- 0 ≤ left ≤ right < n^2

## 풀이를 따라가기

전체 배열을 만들지 않습니다. 펼친 인덱스를 divmod(index,n)으로 행·열로 바꾸고 max(row,column)+1을 계산합니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(n, left, right):
    answer = []
    for index in range(left, right + 1):
        # 전체 배열 없이 펼친 위치를 행·열로 바꾼다.
        row, column = divmod(index, n)
        # 행과 열을 모두 포함한 첫 정사각형 단계가 이 칸의 값이다.
        answer.append(max(row, column) + 1)
    return answer
```

## 정답이 되는 이유

칸 (r,c)는 r과 c를 모두 덮는 첫 정사각형 단계 max(r,c)+1에서 채워집니다. 따라서 각 원소를 독립적으로 바로 구할 수 있습니다.

시간 O(K), 출력 공간 O(K) / Time and output space O(K); K=right−left+1

주의할 점: left와 right는 0부터 세는 인덱스입니다. n² 크기를 할당하면 최대 입력에서 메모리를 감당할 수 없습니다.

## 다른 방법: 정사각형 테두리를 실제로 채우기 · 작은 n

이 대안은 작은 입력에서 원리를 비교하는 검증용입니다. 최대 제한에 제출할 기본 풀이와 구분합니다.

```python
def solution(n,left,right):
    if n>500: raise ValueError('작은 배열의 규칙 확인용: n≤500')
    board=[[0]*n for _ in range(n)]
    for side in range(1,n+1):
        for row in range(side): board[row][side-1]=side
        for col in range(side-1): board[side-1][col]=side
    flat=[value for row in board for value in row]
    return flat[left:right+1]
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 전체 배열을 만들지 않습니다. 펼친 인덱스를 divmod(index,n)으로 행·열로 바꾸고 max(row,column)+1을 계산합니다. | 정사각형 테두리를 실제로 채우기 · 작은 n |
| 비용 | 시간 O(K), 출력 공간 O(K) / Time and output space O(K); K=right−left+1 | 시간 O(n²), 공간 O(n²) / Time and space O(n²) |

## 검증

공식 예제 2개와 생성 입력 60개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다. 제한 상한에 해당하는 크기·수치의 경계 검사도 저장된 테스트에 포함했습니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Return only the requested flat-index interval of the patterned n-by-n array.

### Conditions and input/output

Input arguments: `n, left, right`. The return value is a numeric list satisfying the task described below.

- 1 ≤ n ≤ 10^7; 0 ≤ left ≤ right < n^2; right−left < 10^5

### Approach

Avoid constructing the full array. Convert each flat index to row and column with divmod, then return max(row,column)+1.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Cell (r,c) is first filled by the square stage covering both coordinates, namely max(r,c)+1. Each requested value is therefore available directly.

시간 O(K), 출력 공간 O(K) / Time and output space O(K); K=right−left+1

Boundary cases: left and right are zero-based. Allocating n² entries is infeasible at the maximum n.

### Alternative: Materialize square borders for small n

This alternative is for understanding and checking small inputs; use the main implementation for the full constraints. 시간 O(n²), 공간 O(n²) / Time and space O(n²)

### Verification

Local checks covered 2 official examples and 60 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases. Saved tests also include a size or numeric boundary at the stated upper limit.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: n^2 배열 자르기](https://school.programmers.co.kr/learn/courses/30/lessons/87390) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
