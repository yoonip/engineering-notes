# 교점에 별 만들기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/87377) · Level 2 · Python3

직선 쌍의 정수 교점을 찾아 가장 작은 직사각형 문자 그림으로 표시한다.

## 조건과 입출력

입력 매개변수: `line`. 반환값은 문자열 배열이며 아래 풀이의 조건을 만족하는 결과다.

- line의 세로(행) 길이는 2 이상 1,000 이하인 자연수입니다.
- A, B, C는 -100,000 이상 100,000 이하인 정수입니다.
- 별이 한 개 이상 그려지는 입력만 주어집니다.

## 풀이를 따라가기

두 직선의 행렬식이 0이면 건너뛴다. 크라메르 공식의 x·y 분자가 분모로 나누어떨어지는 교점만 집합에 넣는다. x 최소·최대와 y 최소·최대로 화면을 만든다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
from itertools import combinations

def solution(line):
    points = set()
    for first, second in combinations(line, 2):
        a, b, e = first
        c, d, f = second
        denominator = a * d - b * c
        # 평행한 직선 쌍은 유일한 교점이 없다.
        if denominator == 0:
            continue
        nx, ny = b * f - e * d, e * c - a * f
        # 나머지가 둘 다 0이어야 교점 좌표가 정수다.
        if nx % denominator == 0 and ny % denominator == 0:
            points.add((nx // denominator, ny // denominator))
    min_x = min(x for x, y in points)
    max_x = max(x for x, y in points)
    min_y = min(y for x, y in points)
    max_y = max(y for x, y in points)
    board = [['.'] * (max_x - min_x + 1) for _ in range(max_y - min_y + 1)]
    for x, y in points:
        # 화면 행은 아래로 증가하므로 y축 방향을 뒤집는다.
        board[max_y - y][x - min_x] = '*'
    return [''.join(row) for row in board]
```

## 왜 맞는가

행렬식이 0이 아니면 교점은 유일하다. 분자의 나머지가 0이라는 조건이 정수 좌표의 필요충분조건이며 집합으로 여러 직선이 만나는 중복점을 없앤다.

시간 O(L²+A), 공간 O(L²+A) / Time and space O(L²+A); A=출력 직사각형 면적 / output area

주의할 점: 부동소수점으로 정수인지 판별하지 않는다. 화면에서는 y가 큰 행이 위에 오므로 max_y−y로 뒤집는다.

## 다른 방법: 유리수 가우스 소거로 교점 계산

```python
from itertools import combinations
from fractions import Fraction

def solution(line):
    points=set()
    for first,second in combinations(line,2):
        rows=[[Fraction(a),Fraction(b),Fraction(-c)] for a,b,c in (first,second)]
        if rows[0][0]==0: rows.reverse()
        if rows[0][0]==0: continue
        pivot=rows[0][0]
        rows[0]=[v/pivot for v in rows[0]]
        factor=rows[1][0]
        rows[1]=[a-factor*b for a,b in zip(rows[1],rows[0])]
        if rows[1][1]==0: continue
        y=rows[1][2]/rows[1][1]
        x=rows[0][2]-rows[0][1]*y
        if x.denominator==y.denominator==1: points.add((int(x),int(y)))
    lo_x,hi_x=min(x for x,y in points),max(x for x,y in points)
    lo_y,hi_y=min(y for x,y in points),max(y for x,y in points)
    return [''.join('*' if (x,y) in points else '.' for x in range(lo_x,hi_x+1)) for y in range(hi_y,lo_y-1,-1)]
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 두 직선의 행렬식이 0이면 건너뛴다. 크라메르 공식의 x·y 분자가 분모로 나누어떨어지는 교점만 집합에 넣는다. x 최소·최대와 y 최소·최대로 화면을 만든다. | 유리수 가우스 소거로 교점 계산 |
| 비용 | 시간 O(L²+A), 공간 O(L²+A) / Time and space O(L²+A); A=출력 직사각형 면적 / output area | 시간 O(L²+A), 공간 O(L²+A), 유리수 연산 비용 추가 / Time and space O(L²+A), with rational-arithmetic overhead |

## 검증

공식 예제 4개와 생성 입력 40개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Find integer intersections of line pairs and render their smallest bounding character rectangle.

### Conditions and input/output

Input arguments: `line`. The return value is a list of strings satisfying the task described below.

- 2 ≤ len(line) ≤ 1000; coefficients are integers from −100000 to 100000
- A and B are not both zero; no coincident line pair
- at least one integer intersection; output fits within 1000×1000

### Approach

Skip pairs with zero determinant. Keep intersections only when both Cramer numerators divide exactly by the determinant. Render the bounding box of the deduplicated points.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

A nonzero determinant gives one unique intersection. Exact divisibility characterizes integer coordinates, and a set removes repeated intersections.

시간 O(L²+A), 공간 O(L²+A) / Time and space O(L²+A); A=출력 직사각형 면적 / output area

Boundary cases: Do not test integrality with floating point. Render larger y values higher using max_y−y.

### Alternative: Rational Gaussian elimination for each intersection

시간 O(L²+A), 공간 O(L²+A), 유리수 연산 비용 추가 / Time and space O(L²+A), with rational-arithmetic overhead

### Verification

Local checks covered 4 official examples and 40 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 교점에 별 만들기](https://school.programmers.co.kr/learn/courses/30/lessons/87377) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
