# 전력망을 둘로 나누기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/86971) · Level 2 · Python3

트리 전선을 하나 끊어 두 연결 부분의 송전탑 수 차이를 최소화합니다.

## 조건과 입출력

입력 매개변수: `n, wires`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과입니다.

- n은 2 이상 100 이하인 자연수입니다.
- 1 ≤ v1 < v2 ≤ n 입니다.

## 풀이를 따라가기

DFS로 각 자식 부분 트리 크기를 구합니다. 그 자식 간선을 끊으면 크기는 size와 n−size이므로 abs(n−2size)를 후보로 봅니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(n, wires):
    graph = [[] for _ in range(n + 1)]
    for a, b in wires:
        graph[a].append(b)
        graph[b].append(a)
    answer = n
    def dfs(node, parent):
        nonlocal answer
        size = 1
        for neighbor in graph[node]:
            if neighbor == parent:
                continue
            # 자식 아래에 연결된 송전탑 수를 구한다.
            child_size = dfs(neighbor, node)
            # 이 간선을 끊으면 자식 부분과 나머지로 갈라진다.
            answer = min(answer, abs(n - 2 * child_size))
            size += child_size
        return size
    dfs(1, 0)
    return answer
```

## 정답이 되는 이유

트리에서 간선을 끊으면 자식 부분 트리와 나머지가 정확히 분리됩니다. 모든 부모·자식 간선을 한 번씩 계산하므로 가능한 절단을 전부 비교합니다.

시간 O(n), 공간 O(n) / Time and space O(n)

주의할 점: 임의 그래프가 아니라 트리라는 조건이 중요합니다. DFS에서 부모 간선으로 되돌아가지 않습니다.

## 다른 방법: 간선마다 실제 제거 후 BFS

```python
def solution(n,wires):
    answer=n
    for removed in range(len(wires)):
        graph=[[] for _ in range(n+1)]
        for i,(a,b) in enumerate(wires):
            if i!=removed:
                graph[a].append(b)
                graph[b].append(a)
        seen={1}
        stack=[1]
        while stack:
            for other in graph[stack.pop()]:
                if other not in seen:
                    seen.add(other)
                    stack.append(other)
        answer=min(answer,abs(n-2*len(seen)))
    return answer
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | DFS로 각 자식 부분 트리 크기를 구합니다. 그 자식 간선을 끊으면 크기는 size와 n−size이므로 abs(n−2size)를 후보로 봅니다. | 간선마다 실제 제거 후 BFS |
| 비용 | 시간 O(n), 공간 O(n) / Time and space O(n) | 시간 O(n²), 공간 O(n) / Time O(n²), space O(n) |

## 검증

공식 예제 3개와 생성 입력 38개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Remove one tree edge to minimize the difference between the two component sizes.

### Conditions and input/output

Input arguments: `n, wires`. The return value is an integer satisfying the task described below.

- 2 ≤ n ≤ 100; len(wires)=n−1; input is a tree

### Approach

Compute subtree sizes with DFS. Cutting a child edge produces sizes size and n−size, giving candidate abs(n−2size).

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Removing a tree edge separates exactly the child subtree from the remainder. Processing every child edge covers every possible cut.

시간 O(n), 공간 O(n) / Time and space O(n)

Boundary cases: The tree assumption is essential. Skip the parent edge during DFS.

### Alternative: Remove each edge and BFS the remaining component

시간 O(n²), 공간 O(n) / Time O(n²), space O(n)

### Verification

Local checks covered 3 official examples and 38 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 전력망을 둘로 나누기](https://school.programmers.co.kr/learn/courses/30/lessons/86971) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
