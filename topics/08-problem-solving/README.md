# 알고리즘과 코딩테스트

[전체 목차](../../CATALOG.md) · [처음으로](../../README.md)

코딩테스트에서는 시간과 메모리 제한 안에서 올바른 답을 계산한다. 프로그래머스·백준·LeetCode·Codeforces·AtCoder·HackerRank·Codility·SWEA는 문제 형식과 실행 환경이 달라 같은 알고리즘도 입출력 코드를 다르게 작성한다.

## 알고리즘을 선택하는 기준

완전탐색은 가능한 경우를 직접 조사하고, 정렬은 원소의 순서를 이용할 수 있게 한다. 해시는 빠른 키 조회에, 스택·큐는 처리 순서 유지에 쓰인다. BFS는 가중치가 같은 그래프의 최단 경로, Dijkstra는 음수 간선이 없는 그래프의 최단 경로에 쓰인다. 동적 계획법은 겹치는 부분 문제의 결과를 저장하며, 그리디는 각 단계의 선택이 전체 최적해로 이어진다는 근거가 필요하다.

## 입력 크기와 자료구조

입력 크기 `n`과 반복 횟수를 먼저 연결해 본다. `n=100,000`일 때 `n²`은 100억, `n log₂ n`은 약 166만이다. 이 수가 실제 실행 시간을 그대로 나타내지는 않지만, 어떤 접근을 검토할지 가늠하는 데 도움이 된다.

| 필요한 연산 | 자료구조를 고르는 이유 | 연산 비용 |
| --- | --- | --- |
| BFS의 앞에서 꺼내기 | Python의 `deque`는 뒤 원소를 당기지 않고 맨 앞 원소를 꺼낸다 | `popleft()`는 `O(1)`, 리스트의 `pop(0)`은 `O(n)` |
| 방문 여부·중복 확인 | `set`은 매번 전체를 순회하는 대신 해시로 값을 찾는다 | 조회 평균 `O(1)`, 최악 `O(n)` |
| 가장 작은 값 반복 추출 | heap은 전체를 다시 정렬하지 않고 최솟값을 꺼낸다 | 삽입·최솟값 추출 `O(log n)` |

인접 리스트와 방문 배열을 사용하는 BFS는 정점 `V`개와 간선 `E`개를 합쳐 `O(V+E)`에 탐색한다. 그래프를 인접 행렬로 저장하면 이웃을 확인하는 비용이 달라진다. 시간 복잡도는 알고리즘 이름만으로 정해지지 않고 자료 표현과 실제 연산에도 영향을 받는다.

## 이진 탐색의 경계

아래 함수는 정렬된 배열에서 `target` 이상인 첫 위치를 찾는다. 답이 항상 반열린 구간 `[left, right)`의 경계로 남도록 범위를 줄인다.

```python
def lower_bound(values, target):
    left, right = 0, len(values)
    while left < right:
        mid = (left + right) // 2
        if values[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left
```

`[1, 3, 3, 7]`에서 3을 찾으면 1, 4를 찾으면 3, 8을 찾으면 4다. 시간 복잡도는 `O(log n)`, 추가 공간은 `O(1)`이다. 빈 배열, 중복 값, 범위 밖의 값으로 경계 처리를 확인할 수 있다. 실제 지원 전형과 관련된 내용은 [지원·시험 기록](../55-applications-assessments/README.md)에서 다룬다.

## 관련 기술

프로그래머스 / Programmers, 백준 / Baekjoon, LeetCode, Codeforces, AtCoder, HackerRank, Codility, SWEA

## 참고 자료

- [프로그래머스 코딩테스트 연습](https://school.programmers.co.kr/learn/challenges)

## Programmers 풀이

[Level 2 Python 풀이 100개](../../programmers/README.md)를 문제 번호와 공식 문제 링크로 정리했다. 각 파일에서 실행 코드와 풀이를 확인할 수 있다.

## English

Coding problems ask for correct output within time and memory limits. Programmers, Baekjoon, LeetCode, Codeforces, AtCoder, HackerRank, Codility, and SWEA have different problem formats and execution environments, so the same algorithm may need different input and output code.

### Choosing an algorithm

Brute force checks possible cases directly. Sorting exposes order, hashing supports fast key lookup, and stacks and queues maintain processing order. BFS finds shortest paths when edges have equal weight; Dijkstra handles graphs with nonnegative edge weights. Dynamic programming stores overlapping subproblem results. A greedy algorithm needs a reason why each local choice preserves a globally optimal solution.

### Input size and data structures

Relate input size `n` to the number of operations. At `n=100,000`, `n²` is 10 billion, while `n log₂ n` is about 1.66 million. These counts do not directly predict execution time, but help judge which approaches are plausible.

| Operation needed | Why the structure fits | Operation cost |
| --- | --- | --- |
| Removing the front element in BFS | Python's `deque` avoids shifting the remaining elements | `popleft()` is `O(1)`; list `pop(0)` is `O(n)` |
| Tracking visits or duplicates | A `set` uses hashing instead of scanning all stored elements | Average lookup `O(1)`, worst case `O(n)` |
| Repeatedly extracting the smallest value | A heap avoids sorting the entire collection again | Insertion and minimum extraction `O(log n)` |

BFS with adjacency lists and a visited array takes `O(V+E)` for `V` vertices and `E` edges. An adjacency matrix changes the cost of finding neighbors. Complexity depends on representation and operations as well as the algorithm itself.

### Binary-search boundaries

The function above returns the first position whose value is at least `target` in a sorted array. It narrows a half-open search range, `[left, right)`, until the boundary is found. For `[1, 3, 3, 7]`, targets 3, 4, and 8 return indices 1, 3, and 4. Time complexity is `O(log n)` and extra space is `O(1)`. Empty arrays, duplicates, and targets outside the data range exercise its boundary handling.

Application-related records are kept in [Applications and assessments](../55-applications-assessments/README.md). The [100 Level 2 Python solutions](../../programmers/README.md) are organized by problem number and official problem link, with executable code and an explanation in each file.
