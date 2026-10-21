# 행렬 테두리 회전하기

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/77485) · Level 2 · Python3

직사각형 테두리를 시계방향으로 한 칸씩 돌리고 이동한 최솟값을 구합니다.

## 조건과 입출력

입력 매개변수: `rows, columns, queries`. 반환값은 수치 배열이며 아래 풀이의 조건을 만족하는 결과입니다.

- rows는 2 이상 100 이하인 자연수입니다.
- columns는 2 이상 100 이하인 자연수입니다.
- queries의 행의 개수(회전의 개수)는 1 이상 10,000 이하입니다.
- 1 ≤ x1 < x2 ≤ rows, 1 ≤ y1 < y2 ≤ columns입니다.

## 풀이를 따라가기

테두리를 시계방향 경로로 나열합니다. 기존 값을 별도 배열에 복사하고 각 칸에 바로 앞 경로의 값을 넣습니다. 복사한 값의 최솟값을 답에 추가합니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(rows, columns, queries):
    board = [[r * columns + c + 1 for c in range(columns)] for r in range(rows)]
    answer = []
    for query in queries:
        top, left, bottom, right = [value - 1 for value in query]
        path = [(top, c) for c in range(left, right)]
        path.extend((r, right) for r in range(top, bottom))
        path.extend((bottom, c) for c in range(right, left, -1))
        path.extend((r, left) for r in range(bottom, top, -1))
        # 먼저 값을 복사해 회전 중 덮어쓰기 영향을 없앤다.
        values = [board[r][c] for r, c in path]
        for index, (r, c) in enumerate(path):
            # 시계방향 경로에서 바로 이전 칸의 값이 들어온다.
            board[r][c] = values[index - 1]
        answer.append(min(values))
    return answer
```

## 정답이 되는 이유

경로가 모든 테두리 칸을 중복 없이 포함합니다. 값 배열을 먼저 보관하므로 덮어쓰기 없이 순환 순열을 정확히 적용합니다.

시간 O(RC+ΣP), 공간 O(RC+최대 P) / Time O(RC+ΣP), space O(RC+max P); P=테두리 길이 / perimeter length

주의할 점: 좌표는 입력에서 1부터 셉니다. 다음 회전은 이전 회전이 반영된 행렬에 적용합니다.

## 다른 방법: 임시 값 하나로 네 변 제자리 교환

```python
def solution(rows,columns,queries):
    board=[[r*columns+c+1 for c in range(columns)] for r in range(rows)]
    answer=[]
    for a,b,x,y in queries:
        a,b,x,y=a-1,b-1,x-1,y-1
        carried=board[a][b]
        smallest=carried
        for r,c in ([(a,c) for c in range(b+1,y+1)] + [(r,y) for r in range(a+1,x+1)] + [(x,c) for c in range(y-1,b-1,-1)] + [(r,b) for r in range(x-1,a-1,-1)]):
            board[r][c],carried=carried,board[r][c]
            smallest=min(smallest,carried)
        answer.append(smallest)
    return answer
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 테두리를 시계방향 경로로 나열합니다. 기존 값을 별도 배열에 복사하고 각 칸에 바로 앞 경로의 값을 넣습니다. 복사한 값의 최솟값을 답에 추가합니다. | 임시 값 하나로 네 변 제자리 교환 |
| 비용 | 시간 O(RC+ΣP), 공간 O(RC+최대 P) / Time O(RC+ΣP), space O(RC+max P); P=테두리 길이 / perimeter length | 시간 O(RC+ΣP), 공간 O(RC) / Time O(RC+ΣP), space O(RC) |

## 검증

공식 예제 3개와 생성 입력 60개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Rotate each queried rectangle border one step clockwise and report the minimum moved value.

### Conditions and input/output

Input arguments: `rows, columns, queries`. The return value is a numeric list satisfying the task described below.

- 2 ≤ rows,columns ≤ 100; 1 ≤ len(queries) ≤ 10000
- query=[x1,y1,x2,y2]; 1 ≤ x1 < x2 ≤ rows; 1 ≤ y1 < y2 ≤ columns

### Approach

List border cells in clockwise order, copy their values, then assign each cell its predecessor’s old value. Record the minimum copied value.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

The path includes every border cell once. Copying first prevents overwrite corruption and implements the circular permutation exactly.

시간 O(RC+ΣP), 공간 O(RC+최대 P) / Time O(RC+ΣP), space O(RC+max P); P=테두리 길이 / perimeter length

Boundary cases: Input coordinates are one-based. Every rotation uses the matrix resulting from earlier queries.

### Alternative: In-place four-edge rotation with one carried value

시간 O(RC+ΣP), 공간 O(RC) / Time O(RC+ΣP), space O(RC)

### Verification

Local checks covered 3 official examples and 60 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 행렬 테두리 회전하기](https://school.programmers.co.kr/learn/courses/30/lessons/77485) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
