# 도넛과 막대 그래프

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/258711) · Level 2 · Python3

추가 정점과 원래 도넛·막대·8자 그래프의 수를 구합니다.

## 조건과 입출력

입력 매개변수: `edges`. 반환값은 수치 배열이며 아래 풀이의 조건을 만족하는 결과입니다.

- 1 ≤ edges의 길이 ≤ 1,000,000
- 1 ≤ a, b ≤ 1,000,000
- 도넛 모양 그래프, 막대 모양 그래프, 8자 모양 그래프의 수의 합은 2이상입니다.

## 풀이를 따라가기

정점별 진입·진출 차수를 셉니다. 진입 0·진출 2 이상은 추가 정점, 진출 0인 사용 정점은 막대 끝, 진출 2·진입 2 이상은 8자 중심입니다. 전체 수에서 막대와 8자를 빼 도넛을 구합니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(edges):
    size = max(max(a, b) for a, b in edges) + 1
    incoming = [0] * size
    outgoing = [0] * size
    for a, b in edges:
        outgoing[a] += 1
        incoming[b] += 1
    created = sticks = eights = 0
    for node in range(1, size):
        # 추가 정점은 들어오는 간선이 없고 두 개 이상으로 갈라진다.
        if incoming[node] == 0 and outgoing[node] >= 2:
            created = node
        # 막대 그래프마다 끝점이 하나씩 있다.
        elif outgoing[node] == 0 and incoming[node] > 0:
            sticks += 1
        elif outgoing[node] == 2 and incoming[node] >= 2:
            eights += 1
    # 전체 그래프 수에서 막대와 8자 수를 뺀다.
    donuts = outgoing[created] - sticks - eights
    return [created, donuts, sticks, eights]
```

## 정답이 되는 이유

막대와 8자는 각각 끝과 교차점이 정확히 하나입니다. 추가 정점의 진출 수가 원래 그래프 수와 같으므로 남은 수는 도넛 수입니다.

시간 O(E+M), 공간 O(M) / Time O(E+M), space O(M); M=최대 정점 번호 / largest vertex ID

주의할 점: 번호가 비어 있을 수 있어 미사용 정점은 막대로 세지 않습니다. 추가 정점이 만든 진입 간선 때문에 진입 차수는 원래보다 커질 수 있습니다.

## 다른 방법: 추가 정점 제거 후 연결 부분별 간선 수 분류

```python
from collections import defaultdict

def solution(edges):
    incoming, graph = defaultdict(int), defaultdict(list)
    for a,b in edges:
        graph[a].append(b)
        incoming[b] += 1
    root = next(v for v in graph if incoming[v]==0 and len(graph[v])>=2)
    counts = [0,0,0]
    for start in graph[root]:
        seen, stack = set(), [start]
        while stack:
            node = stack.pop()
            if node in seen:
                continue
            seen.add(node)
            stack.extend(graph[node])
        edge_count = sum(len(graph[v]) for v in seen)
        # 연결 부분마다 E−V는 도넛 0, 막대 −1, 8자 1이다.
        kind = {0:0,-1:1,1:2}[edge_count-len(seen)]
        counts[kind] += 1
    return [root] + counts
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 정점별 진입·진출 차수를 셉니다. 진입 0·진출 2 이상은 추가 정점, 진출 0인 사용 정점은 막대 끝, 진출 2·진입 2 이상은 8자 중심입니다. 전체 수에서 막대와 8자를 빼 도넛을 구합니다. | 추가 정점 제거 후 연결 부분별 간선 수 분류 |
| 비용 | 시간 O(E+M), 공간 O(M) / Time O(E+M), space O(M); M=최대 정점 번호 / largest vertex ID | 시간 O(V+E), 공간 O(V+E) / Time and space O(V+E) |

## 검증

공식 예제 2개와 생성 입력 40개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Identify the added vertex and count the original donut, stick and figure-eight graphs.

### Conditions and input/output

Input arguments: `edges`. The return value is a numeric list satisfying the task described below.

- 1 ≤ len(edges) ≤ 1000000; 1 ≤ vertex ID ≤ 1000000
- at least two original graphs; input satisfies the specified graph construction

### Approach

Count incoming and outgoing edges. The added vertex has indegree zero and outdegree at least two; a used sink ends a stick, and outdegree two with indegree at least two marks a figure-eight center. Subtract those counts from the total.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Each stick has exactly one sink and each figure eight one junction. The added vertex has one edge per original graph, so the remaining count is the donut count.

시간 O(E+M), 공간 O(M) / Time O(E+M), space O(M); M=최대 정점 번호 / largest vertex ID

Boundary cases: Skip unused vertex IDs. Added edges may increase the original indegree of their destination.

### Alternative: Remove the added vertex and classify reachable components by edge count

시간 O(V+E), 공간 O(V+E) / Time and space O(V+E)

### Verification

Local checks covered 2 official examples and 40 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 도넛과 막대 그래프](https://school.programmers.co.kr/learn/courses/30/lessons/258711) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
