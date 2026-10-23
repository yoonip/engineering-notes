# 홀짝트리

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/388354) · Level 3 · Python3

## 문제와 조건 / Task and conditions

노드는 1~400000개로 번호는 1~1000000에서 중복되지 않고 간선은 1~1000000개인 숲입니다. 루트를 적절히 정해 홀짝·역홀짝 트리로 만들 수 있는 연결 트리 수를 각각 반환합니다.

There are 1–400000 distinct node labels in [1,1000000] and 1–1000000 edges forming a forest. Count components rootable as normal and reversed parity trees.

## 풀이 흐름 / Approach

루트의 자식 수는 차수와 같지만 다른 노드는 부모 간선을 빼서 차수−1입니다. 각 연결 트리에서 번호와 차수의 홀짝이 같은 노드 수를 셉니다. 하나만 같으면 홀짝 트리, 하나만 다르면 역홀짝 트리로 만들 수 있습니다.

A root has degree-many children; every other node has degree−1 children. Count nodes whose number parity matches degree parity in each component. Exactly one match permits a normal parity tree; exactly one mismatch permits a reversed tree.

## 정답이 되는 이유 / Why it works

루트로 고른 한 노드만 번호·차수의 일치 성질이 자식 수와 그대로 연결되고, 나머지는 뒤집힙니다. 따라서 원하는 종류에 해당하는 유일한 예외 노드를 루트로 고를 수 있어야 하고 그 조건이 충분합니다.

Only the root preserves the degree-based parity relation; all nonroots flip it when removing their parent edge. Thus the unique exceptional node must serve as root, making the component count condition necessary and sufficient.

## 비용 / Complexity

시간 O((v+e)α(v)), 공간 O(v) / O((v+e)α(v)) time, O(v) space

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(nodes, edges):
    # 실제 노드 수.
    n = len(nodes)
    index = {node: i for i, node in enumerate(nodes)}
    # 서로소 집합의 부모를 자기 자신으로 초기화.
    parent = list(range(n))
    sizes = [1] * n
    # 노드별 연결된 간선 수인 차수 초기화.
    degrees = [0] * n

    def find(node):
        while parent[node] != node:
            # 다음 대표 탐색이 빨라지도록 조상으로 바로 연결.
            parent[node] = parent[parent[node]]
            node = parent[node]
        return node

    # 간선 두 끝 번호를 언패킹.
    for a, b in edges:
        a, b = index[a], index[b]
        # a의 차수 증가.
        degrees[a] += 1
        degrees[b] += 1
        # 두 노드의 연결 집합 대표 조회.
        first, second = find(a), find(b)
        if first != second:
            # 작은 집합을 큰 집합에 붙이기 위해 순서 조정.
            if sizes[first] < sizes[second]:
                first, second = second, first
            # 두 집합을 하나로 합침.
            parent[second] = first
            sizes[first] += sizes[second]
    # 각 트리에서 번호와 차수의 홀짝이 같은 노드 수 저장.
    matches = [0] * n
    for i, node in enumerate(nodes):
        # 번호와 차수의 홀짝 일치 여부.
        if node % 2 == degrees[i] % 2:
            matches[find(i)] += 1
    # 홀짝 트리 수·역홀짝 트리 수를 담은 리스트.
    answer = [0, 0]
    for root in range(n):
        # 부모가 자기 자신이면 한 트리의 대표.
        if parent[root] == root:
            answer[0] += int(matches[root] == 1)
            # 불일치 노드가 정확히 하나이면 그 노드를 루트로 삼아 역홀짝 트리 가능.
            answer[1] += int(matches[root] == sizes[root] - 1)
    return answer
```

## 다른 방법: 모든 루트로 실제 자식 수 확인 / Try all roots and count actual children

각 트리를 모든 노드에서 루팅하고 자식 수를 직접 셉니다. 최악 O(v²)이지만 차수 홀짝 공식과 독립적인 작은 숲 검증입니다.

Root each component at every node and directly count children. The O(v²) worst-case method independently checks the parity formula on small forests.

[alternative_reference.py](alternative_reference.py)

```python
def solution(nodes, edges):
    graph = {node: [] for node in nodes}
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    unseen, answer = set(nodes), [0, 0]
    while unseen:
        first = next(iter(unseen))
        component, stack = [], [first]
        unseen.remove(first)
        while stack:
            node = stack.pop()
            component.append(node)
            for nxt in graph[node]:
                if nxt in unseen:
                    unseen.remove(nxt)
                    stack.append(nxt)
        possible = [False, False]
        for root in component:
            good, inverse = True, True
            stack = [(root, None)]
            while stack:
                node, parent = stack.pop()
                children = [nxt for nxt in graph[node] if nxt != parent]
                matches = node % 2 == len(children) % 2
                good &= matches
                inverse &= not matches
                stack.extend((nxt, node) for nxt in children)
            possible[0] |= good
            possible[1] |= inverse
        answer[0] += possible[0]
        answer[1] += possible[1]
    return answer
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    [
      11,
      9,
      3,
      2,
      4,
      6
    ],
    [
      [
        9,
        11
      ],
      [
        2,
        3
      ],
      [
        6,
        3
      ],
      [
        3,
        4
      ]
    ]
  ],
  "output": [
    1,
    0
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

출처: [프로그래머스 문제 388354](https://school.programmers.co.kr/learn/courses/30/lessons/388354), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 388354](https://school.programmers.co.kr/learn/courses/30/lessons/388354), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

큰 입력 검사: 노드 40만 개의 경로 트리 / A 400000-node path tree

```bash
python verify_stress.py
```
