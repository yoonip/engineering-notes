# 숫자 변환하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/154538) · Level 2 · Python3

x에 n 더하기·2배·3배를 적용해 y로 만드는 최소 연산 횟수를 구한다.

## 조건과 입출력

입력 매개변수: `x, y, n`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과다.

- 1 ≤ x ≤ y ≤ 1,000,000
- 1 ≤ n < y

## 풀이를 따라가기

현재 정수를 정점으로 보고 세 연산을 간선으로 만든다. y를 넘는 값은 버리고 BFS로 처음 y에 도달하는 거리를 반환한다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
from collections import deque

def solution(x, y, n):
    distance = [-1] * (y + 1)
    distance[x] = 0
    queue = deque([x])
    while queue:
        value = queue.popleft()
        if value == y:
            return distance[value]
        # 한 번에 가능한 세 연산 결과를 확인한다.
        for next_value in (value + n, value * 2, value * 3):
            # 값은 증가하므로 목표를 넘은 상태는 볼 필요가 없다.
            if next_value <= y and distance[next_value] == -1:
                distance[next_value] = distance[value] + 1
                queue.append(next_value)
    return -1
```

## 왜 맞는가

연산은 모두 비용 1이며 값을 증가시킨다. y 초과 상태는 되돌아올 수 없고, BFS의 첫 도달 거리가 최소다.

시간 O(y), 공간 O(y) / Time and space O(y)

주의할 점: x=y이면 0이다. 이미 방문한 수는 다시 큐에 넣지 않는다.

## 다른 방법: 역방향 최단 거리 DP

기본 풀이와 같은 결과를 구하되 중간 상태와 계산 방식이 다르다.

```python
def solution(x,y,n):
    inf=y+1
    dp=[inf]*(y-x+1)
    dp[y-x]=0
    for value in range(y,x-1,-1):
        if dp[value-x]==inf: continue
        previous=[value-n]
        if value%2==0: previous.append(value//2)
        if value%3==0: previous.append(value//3)
        for old in previous:
            if old>=x: dp[old-x]=min(dp[old-x],dp[value-x]+1)
    return dp[0] if dp[0]!=inf else -1
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 현재 정수를 정점으로 보고 세 연산을 간선으로 만든다. y를 넘는 값은 버리고 BFS로 처음 y에 도달하는 거리를 반환한다. | 역방향 최단 거리 DP |
| 비용 | 시간 O(y), 공간 O(y) / Time and space O(y) | 시간 O(y−x+1), 공간 O(y−x+1) / Time and space O(y−x+1) |

## 검증

공식 예제 3개와 생성 입력 594개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다. 제한 상한에 해당하는 크기·수치의 경계 검사도 저장된 테스트에 포함했다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Find the fewest additions of n, doublings and triplings that turn x into y.

### Conditions and input/output

Input arguments: `x, y, n`. The return value is an integer satisfying the task described below.

- 1 ≤ x ≤ y ≤ 1000000; 1 ≤ n < y

### Approach

Use integers as vertices and the three operations as edges. Discard values above y and return the first BFS distance to y.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Every operation costs one and increases the value. Overshooting y is irreversible, and the first BFS arrival is shortest.

시간 O(y), 공간 O(y) / Time and space O(y)

Boundary cases: Return zero when x equals y. Enqueue each reachable integer only once.

### Alternative: Backward dynamic programming from y

It computes the same result using different intermediate states or evaluation steps. 시간 O(y−x+1), 공간 O(y−x+1) / Time and space O(y−x+1)

The main approach follows the steps described above. The alternative uses backward dynamic programming from y; compare its intermediate state and cost with the main implementation before choosing it.

### Verification

Local checks covered 3 official examples and 594 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases. Saved tests also include a size or numeric boundary at the stated upper limit.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 숫자 변환하기](https://school.programmers.co.kr/learn/courses/30/lessons/154538) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
