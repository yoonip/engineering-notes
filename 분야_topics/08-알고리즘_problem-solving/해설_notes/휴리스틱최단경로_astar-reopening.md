# A*: 좋은 예상값으로 탐색을 줄이고 정답은 지키기

[분야 안내](../README.md) · [실행 예제](../../../예제_examples/심화_advanced/systems/advanced_models.py) · [독립 테스트](../../../예제_examples/심화_advanced/systems/test_advanced_models.py) · [실행 안내](../../../예제_examples/심화_advanced/systems/README.md)

## 한국어

### 목적지까지 남은 길을 예상합니다

Dijkstra는 지금까지 실제로 지불한 비용이 가장 작은 후보부터 꺼냅니다. A*는 거기에 목적지까지 남은 비용의 예상값을 더합니다. 이미 10을 쓴 길과 5를 쓴 길 중 무엇을 먼저 볼지는 남은 길의 길이에도 달려 있습니다. 다만 예상이 지나치게 낙관적이거나 비관적인 방식은 정답 보장과 연결되므로 “가까워 보이는 곳부터 간다”만으로 설명을 끝낼 수 없습니다.

시작점부터 현재 노드까지 알려진 최소 비용을 $`g(n)`$, 남은 비용 예상값을 $`h(n)`$라 하면 우선순위는 $`f(n)=g(n)+h(n)`$입니다. $`h=0`$이면 Dijkstra의 우선순위가 됩니다. 실제 최소 잔여 비용 $`h^*(n)`$보다 커지지 않는 $`0\le h(n)\le h^*(n)`$를 admissible이라 합니다. [Berkeley CS188 informed search](https://inst.eecs.berkeley.edu/~cs188/textbook/search/informed.html)

### 일관성은 한 edge씩 확인하는 조건입니다

노드 $`u`$에서 $`v`$로 가는 비용이 $`c(u,v)`$일 때 consistency는

```math
h(u)\le c(u,v)+h(v),\qquad h(\mathrm{goal})=0.
```

이 조건을 경로의 모든 edge에 적용하면 중간 h항이 이어져 처음 h는 전체 경로 비용 이합니다. 따라서 목표에 도달할 수 있는 노드에서 consistency는 admissibility를 함의합니다. 일관적인 h에서는 탐색 중 f가 경로를 따라 감소하지 않는 성질을 활용할 수 있습니다. admissible이지만 inconsistent한 h에서는 더 싼 경로가 나중에 발견되어 이미 확장한 노드를 다시 열어야 할 수 있습니다. [CMU 15-281 search](https://www.cs.cmu.edu/~15281/coursenotes/search/index.html)

예제는 영구 closed set을 쓰지 않습니다. 더 작은 g가 나오면 heap에 새 후보를 넣고, 꺼낼 때 저장된 최신 g와 다른 오래된 후보는 버립니다. goal을 처음 발견했을 때가 아니라 유효한 최소 f 후보로 꺼냈을 때 종료합니다. 유한 그래프, 유한 비음수 edge 비용, admissible h와 goal의 h=0이라는 전제에서 최적 비용을 얻습니다. 코드는 h의 유한성·비음수·goal 값만 검사하며 admissibility 전체를 자동 증명하지는 않습니다.

### 격자에서 Manhattan 거리가 맞는 이유

상하좌우 한 칸의 비용이 1이고 대각선 이동이 없다면 두 좌표 차이의 절댓값 합이 장애물을 지운 문제의 정확한 거리입니다. 장애물은 이 거리보다 길을 짧게 만들 수 없으므로 하한으로 쓸 수 있습니다. diagonal 이동이나 다른 가중치를 허용하면 같은 공식을 무조건 적용할 수 없습니다. 좌표 단위와 edge 비용 단위도 맞아야 합니다.

정확성만 같다고 항상 탐색량이 줄어드는 것은 아닙니다. h 계산 자체가 비쌀 수 있고 많은 노드의 f가 같으면 tie-breaking 영향이 큽니다. 특히 inconsistent h를 허용하면 같은 노드가 여러 번 확장될 수 있어 Dijkstra의 단순한 “노드당 한 번” 분석을 그대로 쓸 수 없습니다. heap 연산 횟수는 실제 삽입된 후보 수에 따라 정해집니다.

### 실행과 독립 검증

`astar()`는 비용·경로·확장 횟수를 반환합니다. 150개 6×6 장애물 격자에서 별도 BFS가 계산한 거리와 비교하고, 반환 경로의 연속 edge도 확인합니다. BFS는 이 테스트의 단위 가중치 조건에서 독립 정답으로 쓸 수 있습니다. 또 s→a=3, s→b=1, b→a=1, a→g=3 그래프에서 admissible이지만 inconsistent한 h를 주어 a를 다시 열어야 비용 5를 찾는 경우를 고정합니다.

음수 edge는 입력 단계에서 거부합니다. 도달할 수 없으면 무한대 비용과 빈 경로를 반환합니다. 이 검사들은 특정 그래프 집합의 정확성과 재개방 구현을 확인합니다. 로봇의 충돌·회전 반경·동적 장애물까지 해결하는 경로 계획기는 아니며, 그 제약은 상태와 edge 모델에 먼저 들어가야 합니다.

저장소 루트에서 실행합니다. 첫 명령은 입력과 계산 결과를 출력하고, 두 번째 명령은 이 디렉터리의 전체 테스트를 실행합니다.

```sh
python "예제_examples/심화_advanced/systems/demo.py" astar
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## English

### Estimate the remaining journey

Dijkstra expands candidates by cost already paid. A* adds an estimate of what remains. Choosing between a route that has spent ten and one that has spent five depends on their remaining costs, but heuristic assumptions determine correctness.

Let $`g(n)`$ be the best known cost from the start and $`h(n)`$ the estimate to the goal. Priority is $`f(n)=g(n)+h(n)`$. Setting $`h=0`$ recovers Dijkstra's priority. A nonnegative estimate is admissible when $`h(n)\le h^*(n)`$, the true remaining optimum. [Berkeley CS188 informed search](https://inst.eecs.berkeley.edu/~cs188/textbook/search/informed.html)

### Consistency is a local edge condition

For edge cost $`c(u,v)`$, consistency requires

```math
h(u)\le c(u,v)+h(v),\qquad h(\mathrm{goal})=0.
```

Applying this inequality along a path bounds its initial h by total path cost. Thus consistency implies admissibility on nodes with a path to the goal. It also makes f nondecreasing along paths. An admissible but inconsistent heuristic can reveal a better route after a node has already expanded, requiring reopening. [CMU 15-281 search](https://www.cs.cmu.edu/~15281/coursenotes/search/index.html)

The implementation has no permanent closed set. A lower g inserts another heap candidate; a popped entry with an obsolete g is discarded. It stops when the goal is popped as a valid minimum-f candidate, not when first discovered. Optimality assumes a finite graph, finite nonnegative edge costs, admissibility, and zero goal heuristic. The code validates finiteness, nonnegativity, and the goal value; it does not prove global admissibility.

### Why Manhattan distance works on this grid

For four-neighbor moves costing one, coordinate absolute differences sum to the exact distance after removing obstacles. Obstacles cannot shorten it, so it is a lower bound. Diagonal movement or different edge weights require reconsidering the formula and matching coordinate units with cost units.

Correctness does not guarantee fewer expansions in every implementation. Evaluating h costs time, ties affect exploration, and inconsistent h may expand nodes repeatedly. Dijkstra's simple one-expansion-per-node analysis cannot be carried over unchanged. Heap work follows the number of candidate insertions actually made.

### Executable and independent checks

`astar()` returns cost, path, and expansion count. Tests compare 150 obstacle-filled 6×6 grids against a separate BFS and verify every returned path edge. BFS is an independent reference because these tests use unit weights. A fixed graph with s→a=3, s→b=1, b→a=1, and a→g=3 uses an admissible inconsistent heuristic that requires reopening a to obtain cost five.

Negative edges are rejected. Unreachable goals return infinite cost and an empty path. These checks cover selected graphs and reopening behavior, not complete robotic motion planning. Collision geometry, turning radius, and moving obstacles must first become part of the state and edge model.

Run the following commands from the repository root. The first prints the input and computed observations; the second runs the complete test suite in this example directory.

```sh
python "예제_examples/심화_advanced/systems/demo.py" astar
python "예제_examples/심화_advanced/systems/test_advanced_models.py" -v
```

## 출처 / Sources

- [UC Berkeley CS188: Informed search](https://inst.eecs.berkeley.edu/~cs188/textbook/search/informed.html): A*와 admissibility / A* and admissibility
- [CMU 15-281: Search](https://www.cs.cmu.edu/~15281/coursenotes/search/index.html): consistency·graph search / consistency and graph search
