# 바이러스 파이프

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/468373) · Level 2 · Python3

같은 종류의 파이프를 열어 감염을 퍼뜨리는 행동을 최대 k번 선택합니다.

## 조건과 입출력

입력 매개변수: `n, infection, edges, k`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과입니다.

- 2 ≤ n ≤ 100
- 1 ≤ infection ≤ n
- 1 ≤ x < y ≤ n
- 1 ≤ type ≤ 3
- 1 ≤ k ≤ 10

## 풀이를 따라가기

종류별 연결 요소를 비트마스크로 저장합니다. 한 종류를 열면 현재 감염과 닿은 요소 전체를 합칩니다. 세 종류의 선택을 깊이 우선 탐색합니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(n, infection, edges, k):
    graph = [[[] for _ in range(n)] for _ in range(3)]
    for x, y, kind in edges:
        graph[kind - 1][x - 1].append(y - 1)
        graph[kind - 1][y - 1].append(x - 1)

    groups = [[] for _ in range(3)]
    for kind in range(3):
        visited = [False] * n
        for start in range(n):
            if visited[start]:
                continue
            visited[start] = True
            stack = [start]
            component = 0
            while stack:
                node = stack.pop()
                # 노드 번호에 해당하는 비트로 연결 요소를 표현한다.
                component |= 1 << node
                for neighbor in graph[kind][node]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        stack.append(neighbor)
            groups[kind].append(component)

    answer = 1

    def dfs(mask, remaining):
        nonlocal answer
        answer = max(answer, bin(mask).count('1'))
        if remaining == 0 or answer == n:
            return
        for components in groups:
            next_mask = mask
            for component in components:
                # 현재 감염과 닿은 연결 요소는 통째로 감염된다.
                if mask & component:
                    next_mask |= component
            # 감염이 늘지 않는 행동은 생략한다.
            if next_mask != mask:
                dfs(next_mask, remaining - 1)

    dfs(1 << (infection - 1), k)
    return answer
```

## 정답이 되는 이유

같은 종류로 연결된 정점은 파이프가 열린 동안 모두 감염됩니다. 연결 요소 사이에는 그 종류의 경로가 없으므로 이 합집합이 한 행동의 정확한 결과입니다.

시간 O(n·3^k), 공간 O(n+k)개의 큰 정수 / Time O(n·3^k), space O(n+k) big integers; 비트 연산 비용은 정수 폭에 비례 / bit-operation cost grows with n

주의할 점: 감염 집합이 그대로인 행동은 생략해도 최대 k번 조건을 해치지 않습니다. 종류를 열어 둔 채 다른 종류를 동시에 열면 안 됩니다.

## 다른 방법: 감염 집합의 너비 우선 탐색

```python
def solution(n, infection, edges, k):
    graph = [[[] for _ in range(n)] for _ in range(3)]
    for a, b, kind in edges:
        graph[kind-1][a-1].append(b-1)
        graph[kind-1][b-1].append(a-1)
    frontier = {1 << (infection-1)}
    for _ in range(k):
        following = set()
        for mask in frontier:
            for kind in range(3):
                reached = mask
                stack = [v for v in range(n) if mask >> v & 1]
                while stack:
                    v = stack.pop()
                    for w in graph[kind][v]:
                        if not reached >> w & 1:
                            reached |= 1 << w
                            stack.append(w)
                following.add(reached)
        # 같은 감염 집합은 이후의 선택도 같으므로 한 번만 남긴다.
        frontier = following
    return max(mask.bit_count() for mask in frontier)
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 종류별 연결 요소를 비트마스크로 저장합니다. 한 종류를 열면 현재 감염과 닿은 요소 전체를 합칩니다. 세 종류의 선택을 깊이 우선 탐색합니다. | 감염 집합의 너비 우선 탐색 |
| 비용 | 시간 O(n·3^k), 공간 O(n+k)개의 큰 정수 / Time O(n·3^k), space O(n+k) big integers; 비트 연산 비용은 정수 폭에 비례 / bit-operation cost grows with n | 시간 O(3^k(n+E)), 공간 O(3^k+n+E) / Time O(3^k(n+E)), space O(3^k+n+E) |

## 검증

공식 예제 2개와 생성 입력 60개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Choose up to k pipe-type activations to maximize the number of infected nodes.

### Conditions and input/output

Input arguments: `n, infection, edges, k`. The return value is an integer satisfying the task described below.

- 2 ≤ n ≤ 100; len(edges)=n−1; 1 ≤ infection ≤ n
- 1 ≤ type ≤ 3; 1 ≤ k ≤ 10; input is a tree

### Approach

Store each type’s connected components as bitmasks. Activating a type infects every component touching the current infected set. Explore the three choices with depth-first search.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Infection reaches every node in a touching same-type component and cannot cross between such components. Their union is exactly the result of one activation.

시간 O(n·3^k), 공간 O(n+k)개의 큰 정수 / Time O(n·3^k), space O(n+k) big integers; 비트 연산 비용은 정수 폭에 비례 / bit-operation cost grows with n

Boundary cases: A no-change activation can be skipped because at most k actions are allowed. Different pipe types are never open simultaneously.

### Alternative: Breadth-first search over infected sets

시간 O(3^k(n+E)), 공간 O(3^k+n+E) / Time O(3^k(n+E)), space O(3^k+n+E)

### Verification

Local checks covered 2 official examples and 60 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 바이러스 파이프](https://school.programmers.co.kr/learn/courses/30/lessons/468373) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
