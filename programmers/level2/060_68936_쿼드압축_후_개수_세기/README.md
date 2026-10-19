# 쿼드압축 후 개수 세기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/68936) · Level 2 · Python3

같은 값으로 채워진 정사각형을 압축했을 때 남는 0·1 블록 수를 셉니다.

## 조건과 입출력

입력 매개변수: `arr`. 반환값은 수치 배열이며 아래 풀이의 조건을 만족하는 결과입니다.

- arr의 행의 개수는 1 이상 1024 이하이며, 2의 거듭 제곱수 형태를 하고 있습니다. 즉, arr의 행의 개수는 1, 2, 4, 8, ..., 1024 중 하나입니다.

## 풀이를 따라가기

정사각형 전체가 한 값이면 그 값의 블록 하나를 셉니다. 섞여 있으면 네 같은 크기 사각형으로 나누어 반복합니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(arr):
    answer = [0, 0]
    def compress(row, column, size):
        value = arr[row][column]
        # 전부 같은 값이면 이 구역 하나로 압축하고 종료한다.
        if all(arr[r][c] == value for r in range(row, row + size) for c in range(column, column + size)):
            answer[value] += 1
            return
        # 섞인 구역만 같은 크기의 네 부분으로 나눈다.
        half = size // 2
        compress(row, column, half)
        compress(row, column + half, half)
        compress(row + half, column, half)
        compress(row + half, column + half, half)
    compress(0, 0, len(arr))
    return answer
```

## 정답이 되는 이유

균일한 구역은 정의상 하나로 압축되고 비균일 구역은 네 부분을 반드시 따로 압축합니다. 크기가 절반씩 줄어 1칸에서 끝나므로 모든 블록을 정확히 셉니다.

최악 시간 O(N² log N), 공간 O(log N) 재귀 / Worst-case time O(N² log N), recursion space O(log N)

주의할 점: 행렬 크기는 2의 거듭제곱입니다. 균일한 큰 블록을 찾으면 더 작은 블록을 중복해서 세지 않습니다.

## 다른 방법: 2차원 누적합으로 균일성 상수 시간 판정

```python
def solution(arr):
    n=len(arr)
    prefix=[[0]*(n+1) for _ in range(n+1)]
    for r in range(n):
        running=0
        for c in range(n):
            running+=arr[r][c]
            prefix[r+1][c+1]=prefix[r][c+1]+running
    answer=[0,0]
    def compress(r,c,size):
        total=prefix[r+size][c+size]-prefix[r][c+size]-prefix[r+size][c]+prefix[r][c]
        if total==0: answer[0]+=1; return
        if total==size*size: answer[1]+=1; return
        half=size//2
        for dr,dc in ((0,0),(0,half),(half,0),(half,half)): compress(r+dr,c+dc,half)
    compress(0,0,n)
    return answer
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 정사각형 전체가 한 값이면 그 값의 블록 하나를 셉니다. 섞여 있으면 네 같은 크기 사각형으로 나누어 반복합니다. | 2차원 누적합으로 균일성 상수 시간 판정 |
| 비용 | 최악 시간 O(N² log N), 공간 O(log N) 재귀 / Worst-case time O(N² log N), recursion space O(log N) | 시간 O(N²), 공간 O(N²) / Time and space O(N²) |

## 검증

공식 예제 2개와 생성 입력 50개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다. 제한 상한에 해당하는 크기·수치의 경계 검사도 저장된 테스트에 포함했습니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Count zero and one blocks after recursively compressing uniform squares.

### Conditions and input/output

Input arguments: `arr`. The return value is a numeric list satisfying the task described below.

- square binary matrix; side length is a power of two from 1 to 1024

### Approach

Count one block if a square is uniform. Otherwise recurse into its four equal quadrants.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

A uniform square compresses to one block; a nonuniform square must be treated through its four quadrants. Halving terminates at single cells and counts every final block exactly.

최악 시간 O(N² log N), 공간 O(log N) 재귀 / Worst-case time O(N² log N), recursion space O(log N)

Boundary cases: The side length is a power of two. Once a uniform square is counted, do not count its subblocks again.

### Alternative: Use 2D prefix sums for constant-time uniformity tests

시간 O(N²), 공간 O(N²) / Time and space O(N²)

### Verification

Local checks covered 2 official examples and 50 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases. Saved tests also include a size or numeric boundary at the stated upper limit.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 쿼드압축 후 개수 세기](https://school.programmers.co.kr/learn/courses/30/lessons/68936) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
