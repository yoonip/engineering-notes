# 혼자 놀기의 달인

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/131130) · Level 2 · Python3

카드 순열이 만드는 두 상자 그룹의 크기 곱을 최대화합니다.

## 조건과 입출력

입력 매개변수: `cards`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과입니다.

- 2 ≤ cards의 길이 ≤ 100
- cards의 원소는 cards의 길이 이하인 임의의 자연수입니다.

## 풀이를 따라가기

각 상자에서 카드가 가리키는 상자를 따라가며 아직 방문하지 않은 순환을 찾습니다. 순환 길이를 모아 가장 큰 두 길이를 곱합니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(cards):
    visited = set()
    groups = [0, 0]
    for start in range(len(cards)):
        node, size = start, 0
        # 순열의 포인터를 따라가면 한 순환 그룹이 만들어진다.
        while node not in visited:
            visited.add(node)
            size += 1
            node = cards[node] - 1
        groups.append(size)
    groups.sort(reverse=True)
    # 서로 다른 두 순환 중 가장 큰 둘이 곱을 최대화한다.
    return groups[0] * groups[1]
```

## 정답이 되는 이유

입력이 순열이라 각 상자의 진입·진출이 하나씩이며 연결 부분은 순환입니다. 첫 그룹이 한 순환을 모두 소진하고 두 번째는 다른 순환이므로 가장 큰 둘을 고르면 됩니다.

시간 O(N log N), 공간 O(N) / Time O(N log N), space O(N)

주의할 점: 전체가 한 순환이면 두 번째 그룹은 없어 0입니다. 카드 번호를 0 기반 인덱스로 바꿉니다.

## 다른 방법: 분리 집합으로 순환 그룹 크기 계산

```python
from heapq import nlargest

def solution(cards):
    parent=list(range(len(cards)))
    size=[1]*len(cards)
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]
            x=parent[x]
        return x
    for i,card in enumerate(cards):
        a,b=find(i),find(card-1)
        if a!=b:
            if size[a]<size[b]: a,b=b,a
            parent[b]=a
            size[a]+=size[b]
    largest=nlargest(2,[size[i] for i in range(len(cards)) if parent[i]==i]+[0,0])
    return largest[0]*largest[1]
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 각 상자에서 카드가 가리키는 상자를 따라가며 아직 방문하지 않은 순환을 찾습니다. 순환 길이를 모아 가장 큰 두 길이를 곱합니다. | 분리 집합으로 순환 그룹 크기 계산 |
| 비용 | 시간 O(N log N), 공간 O(N) / Time O(N log N), space O(N) | 시간 O(N α(N)), 공간 O(N) / Time O(N α(N)), space O(N) |

## 검증

공식 예제 1개와 생성 입력 48개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Maximize the product of sizes of two groups formed by a card permutation.

### Conditions and input/output

Input arguments: `cards`. The return value is an integer satisfying the task described below.

- 2 ≤ len(cards) ≤ 100; cards is a permutation of 1 … len(cards)

### Approach

Follow each unvisited box through its card pointers, recording cycle lengths. Multiply the two largest lengths.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

A permutation has one incoming and one outgoing edge per box, so its components are cycles. The two groups consume two distinct cycles, making the two largest optimal.

시간 O(N log N), 공간 O(N) / Time O(N log N), space O(N)

Boundary cases: A single cycle leaves no second group, giving zero. Convert one-based card numbers to zero-based indices.

### Alternative: Disjoint-set union to find cycle-group sizes

시간 O(N α(N)), 공간 O(N) / Time O(N α(N)), space O(N)

### Verification

Local checks covered 1 official examples and 48 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 혼자 놀기의 달인](https://school.programmers.co.kr/learn/courses/30/lessons/131130) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
