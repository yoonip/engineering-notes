# 당구 연습

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/169198) · Level 2 · Python3

벽을 한 번 맞힌 뒤 목표 공에 도달하는 최소 이동 거리의 제곱을 구한다.

## 조건과 입출력

입력 매개변수: `m, n, startX, startY, balls`. 반환값은 수치 배열이며 아래 풀이의 조건을 만족하는 결과다.

- 3 ≤ m, n ≤ 1,000
- 2 ≤ balls의 길이 ≤ 1,000

## 풀이를 따라가기

목표 공을 네 벽 너머로 대칭 이동한다. 시작점에서 대칭점까지 직선 거리의 제곱을 계산한다. 벽보다 공을 먼저 맞히는 일직선 후보는 제외한다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(m, n, startX, startY, balls):
    answer = []
    for x, y in balls:
        distances = []
        # 왼쪽 벽보다 공을 먼저 맞히는 일직선 경로는 제외한다.
        if not (startY == y and x < startX):
            distances.append((startX + x) ** 2 + (startY - y) ** 2)
        if not (startY == y and x > startX):
            distances.append((2 * m - startX - x) ** 2 + (startY - y) ** 2)
        if not (startX == x and y < startY):
            distances.append((startX - x) ** 2 + (startY + y) ** 2)
        if not (startX == x and y > startY):
            distances.append((startX - x) ** 2 + (2 * n - startY - y) ** 2)
        # 가능한 네 벽 반사 경로 중 최솟값을 고른다.
        answer.append(min(distances))
    return answer
```

## 왜 맞는가

반사 전후 각도가 같은 경로는 벽을 기준으로 펼치면 직선이 된다. 벽까지의 경로에서 목표 공을 먼저 맞히는 경우만 제거하면 네 벽 후보가 모든 한 번 반사 경로를 포함한다.

시간 O(B), 공간 O(B) / Time and output space O(B)

주의할 점: 최소 거리가 아니라 거리 제곱을 반환한다. 수평·수직 정렬에서 벽을 먼저 맞히는지 방향을 확인한다.

## 다른 방법: 정확한 유리수 반사점 계산

```python
from fractions import Fraction

def solution(m,n,startX,startY,balls):
    answer=[]
    for x,y in balls:
        candidates=[]
        for mx,my,axis,bound in ((-x,y,0,0),(2*m-x,y,0,m),(x,-y,1,0),(x,2*n-y,1,n)):
            origin=(startX,startY)
            mirror=(mx,my)
            t=Fraction(bound-origin[axis],mirror[axis]-origin[axis])
            bounce=(origin[0]+t*(mx-startX),origin[1]+t*(my-startY))
            # 실제 공이 시작점과 반사점 사이에 놓였으면 벽을 맞히기 전에 충돌한다.
            vx,vy=bounce[0]-startX,bounce[1]-startY
            cross=(x-startX)*vy-(y-startY)*vx
            dot=(x-startX)*vx+(y-startY)*vy
            if cross==0 and 0<dot<vx*vx+vy*vy:
                continue
            candidates.append((mx-startX)**2+(my-startY)**2)
        answer.append(min(candidates))
    return answer
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 목표 공을 네 벽 너머로 대칭 이동한다. 시작점에서 대칭점까지 직선 거리의 제곱을 계산한다. 벽보다 공을 먼저 맞히는 일직선 후보는 제외한다. | 정확한 유리수 반사점 계산 |
| 비용 | 시간 O(B), 공간 O(B) / Time and output space O(B) | 시간 O(B), 공간 O(B) / Time and space O(B) |

## 검증

공식 예제 1개와 생성 입력 70개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Find the minimum squared path length reaching each target ball after one wall reflection.

### Conditions and input/output

Input arguments: `m, n, startX, startY, balls`. The return value is a numeric list satisfying the task described below.

- 3 ≤ m,n ≤ 1000; 0 < startX < m; 0 < startY < n
- 2 ≤ len(balls) ≤ 1000; targets are strictly inside the table and differ from the start

### Approach

Mirror each target across all four walls and compute squared straight-line distances. Exclude collinear cases that hit the ball before the wall.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Unfolding a reflection turns the equal-angle path into a straight line. After excluding premature ball hits, the four mirrored candidates cover all one-wall paths.

시간 O(B), 공간 O(B) / Time and output space O(B)

Boundary cases: Return squared distance, not distance. For horizontal or vertical alignment, check the direction of the premature collision.

### Alternative: Compute reflection points using exact fractions

시간 O(B), 공간 O(B) / Time and space O(B)

### Verification

Local checks covered 1 official examples and 70 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 당구 연습](https://school.programmers.co.kr/learn/courses/30/lessons/169198) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
