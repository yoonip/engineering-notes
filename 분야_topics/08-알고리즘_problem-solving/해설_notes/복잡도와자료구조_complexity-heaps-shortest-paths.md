# 복잡도와 자료구조: heap으로 최단 경로 찾기

[Problem Solving](../README.md) · [실행 코드](../../../예제_examples/확장기초_extended/systems/extended_models.py) · [독립 검증](../../../예제_examples/확장기초_extended/systems/test_extended_models.py)

## 한국어

### 빠르다는 말을 입력 크기로 바꾸기

원소가 열 개일 때의 실행 시간만으로 큰 입력을 판단하기 어렵습니다. 시간복잡도는 입력 크기가 늘 때 필요한 연산량의 증가를 나타냅니다. $`O(n)`$은 상수 배까지 포함한 점근적 상계이며 “항상 정확히 n번”이나 특정 초 단위를 뜻하지 않습니다. 메모리, 상수 비용, 입력 분포와 최악 상황도 함께 봅니다.

반복해서 최소값을 꺼낼 때마다 전체 목록을 탐색하면 누적 비용이 커집니다. 이진 min-heap은 각 부모가 자식보다 크지 않다는 불변식을 유지합니다. 최소 원소는 루트에 있지만 나머지 배열 전체가 정렬된 것은 아닙니다. 삽입과 최소값 제거는 $`O(\log n)`$, 이미 있는 배열의 `heapify`는 $`O(n)`$입니다. [Python heapq](https://docs.python.org/3/library/heapq.html)

### Dijkstra가 성립하는 전제

시작점 $`s`$에서 각 정점까지의 거리 추정 $`d[v]`$를 두고, 간선 $`(u,v)`$를 통해 $`d[u]+w(u,v)`$가 더 작으면 갱신합니다. 이를 relaxation이라고 합니다. Dijkstra는 남은 추정 중 최소인 정점을 먼저 확정합니다. 모든 간선 가중치가 음이 아니어야 이 확정 규칙을 사용할 수 있습니다. [MIT 6.006 Lecture 16](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/6277a1f06100c26a7ff21031af6757b5_MIT6_006F11_lec16.pdf)

직관은 “앞으로 가면서 비용을 되돌려 받지 않는다”는 것입니다. 아직 확정하지 않은 정점을 거쳐 더 짧아지려면 그 경로의 첫 미확정 정점에 이미 더 작은 후보가 있어야 합니다. 최소 후보를 먼저 선택했다는 사실과 모순됩니다. 음수 간선이 있으면 나중에 비용을 크게 줄일 수 있어 이 논리가 깨집니다. 0 가중치는 허용됩니다.

간선 가중치가 모두 같으면 BFS가 더 간단할 수 있습니다. 음수 가중치에는 조건에 맞는 다른 알고리즘이 필요합니다. 조밀한 그래프에서는 배열 기반 $`O(V^2)`$ 구현도 합리적일 수 있으므로 heap이 언제나 더 빠르다는 규칙은 없습니다.

### 오래된 후보를 어떻게 처리할까요

`heapq`에는 이 구현에 필요한 decrease-key 연산이 없습니다. 예제 `dijkstra`는 더 나은 거리를 찾을 때 새 항목을 넣고, 꺼낸 거리가 현재 거리와 다르면 오래된 후보로 건너뜁니다. 예를 들어 s→a=10, s→b=1, b→a=1이면 a의 10은 나중에 무효가 됩니다. 같은 거리에서 서로 비교할 수 없는 노드 객체끼리 비교되지 않도록 증가하는 ticket을 두 번째 필드로 사용합니다. [heapq의 우선순위 큐 구현 설명](https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes)

이 버전은 음이 아닌 정수 가중치를 요구합니다. Python 정수는 고정 폭 정수 overflow 문제를 피하지만 무한한 자원을 쓰는 것은 아닙니다. 실수 가중치를 허용하려면 NaN·무한대·반올림과 비교 규칙을 다시 정해야 합니다. 도달 불가능한 정점은 무한대로 남으며, 그래프 전체의 입력 검증은 시작점에서 닿지 않는 음수 간선도 거부합니다.

lazy heap에는 정점당 하나보다 많은 후보가 쌓일 수 있습니다. 거리의 덧셈·비교를 상수 비용으로 세는 모형에서 일반적인 상계는 시간 $`O((V+E)\log(V+E+1))`$, 보조 공간 $`O(V+E)`$입니다. 매우 큰 정수의 실제 연산 비용은 자릿수에도 달려 있습니다. 인덱스 heap의 decrease-key 구현과 복잡도·메모리 조건이 다릅니다.

### 검증은 다른 계산 경로로

테스트는 작은 그래프 240개에서 간선을 반복 완화하는 Bellman–Ford 기준해와 결과를 대조합니다. 0 가중치, 오래된 후보, 단절 정점과 잘못된 입력도 확인합니다. 모든 간선 비용에 양의 정수 k를 곱하면 유한한 최단 거리도 k배가 되는 성질도 점검합니다. 이 성질만으로 완전한 정답을 증명하지 않으므로 알려진 예와 독립 기준해를 함께 씁니다. 특정 코딩테스트 제출이나 시간 제한 통과 결과를 뜻하는 검증은 아닙니다.

## English

### Express speed through input growth

A run on ten elements says little about much larger inputs. Complexity describes growth in operations; $`O(n)`$ is an asymptotic upper bound, not exactly n operations or a number of seconds. Memory, constants, distributions, and worst cases still matter.

A min-heap maintains parents no greater than children. Its root is minimal, but its array is not fully sorted. Insert and remove-min take $`O(\log n)`$, while `heapify` takes $`O(n)`$. Repeated full scans to find minima can therefore be avoidable. [heapq](https://docs.python.org/3/library/heapq.html)

### Why Dijkstra requires nonnegative costs

Relaxation improves $`d[v]`$ through a candidate $`d[u]+w(u,v)`$. Dijkstra repeatedly finalizes the minimum remaining estimate. Nonnegative edge weights make that rule valid. A supposedly shorter route through an unfinalized vertex would have required a smaller frontier candidate already, contradicting the choice of the minimum. Negative edges break the argument by allowing later cost reductions; zero weights are valid. [MIT lecture notes](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/6277a1f06100c26a7ff21031af6757b5_MIT6_006F11_lec16.pdf)

Equal-cost edges may allow simpler BFS. Negative weights require a suitable different algorithm. Dense graphs can favor an array-based $`O(V^2)`$ implementation, so a heap is not universally faster.

### Handle stale candidates explicitly

The implementation pushes a new heap entry after an improvement and skips an entry whose distance no longer equals the current best. With s→a=10, s→b=1, b→a=1, the old candidate ten becomes stale. An increasing ticket avoids comparing mutually unorderable node objects when distances tie. [Priority-queue notes](https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes)

This version accepts only nonnegative integer weights. Python integers avoid fixed-width overflow but still consume finite resources. Floating weights need a separate NaN, infinity, rounding, and comparison policy. Unreachable vertices retain infinity; validation also rejects negative edges outside the reachable component.

A lazy heap can hold several entries per vertex. Counting distance arithmetic and comparisons as constant-cost operations gives $`O((V+E)\log(V+E+1))`$ time and $`O(V+E)`$ auxiliary space. Actual operations on very large integers also depend on digit count. These bounds differ from indexed decrease-key heaps.

### Independent verification

Tests compare 240 small graphs with a Bellman–Ford reference using repeated edge relaxation. They cover zero costs, stale entries, disconnected vertices, and invalid input. Multiplying all weights by a positive integer must scale finite distances by the same factor. This metamorphic relation complements known cases and an independent oracle; it is not a complete proof or evidence of passing a particular online judge's time limit.

## 출처 / Sources

MIT의 알고리즘 전제와 Python의 heap 구현 규칙을 대조했습니다. / MIT's algorithm assumptions were checked against Python heap behavior. 확인 / checked: 2026-10-19.
