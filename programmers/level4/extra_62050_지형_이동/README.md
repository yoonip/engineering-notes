# 지형 이동

Level 4 · `62050` · Python3 · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/62050)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py)

## 문제와 조건

높이 차가 height 이하면 무료 이동하고, 넘으면 그 높이 차만큼 사다리 비용을 낸다. 모든 칸을 연결하는 최소 비용을 구한다.

입력 범위와 상수는 다음과 같다. 기호는 코드의 매개변수에 맞췄다.

`4≤N≤300; N×N land; heights and allowed difference:1..10000; ladder cost is the full height difference.`

## 풀이를 따라가기

인접 칸 사이 비용을 무료 또는 실제 높이 차로 놓으면 최소 신장 트리 문제다. 주 풀이는 연결한 영역 밖으로 나가는 가장 싼 간선을 heap에서 꺼내는 Prim 방식이다.

연결 영역과 바깥을 가르는 간선 중 최솟값은 어떤 최소 신장 트리에 포함시켜도 손해가 없다. 이 절단 성질을 반복한다. 사다리 비용에서 height를 빼면 다른 문제를 풀게 된다.

## 다른 방법과 비교

대안 Kruskal은 모든 인접 간선을 정렬하고 서로 다른 연결 요소를 DSU로 합친다. 같은 최소 신장 트리를 다른 순서로 구성하며, 간선 목록 정렬과 DSU 공간이 추가된다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O(N² log N)` | `O(N²)` |
| 대안 풀이 | `O(N² log N)` | 코드의 상태·탐색 구조 참조 |

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교한다. 실행 기록은 [validation.json](validation.json)에 있다. 원본 제출 파일은 [submitted_original.py](submitted_original.py)에 그대로 보관했다.

```bash
python test_solution.py
```

## English

### Problem and constraints

Adjacent cells are free within the height threshold; otherwise a ladder costs the full difference. Minimize the cost connecting every cell.

Input limits and constants, using the parameter names in the code:

`4≤N≤300; N×N land; heights and allowed difference:1..10000; ladder cost is the full height difference.`

### Following the solution

These edge costs define a minimum spanning tree. The main Prim implementation extracts the cheapest edge leaving the connected region from a heap.

By the cut property, a cheapest crossing edge can extend an optimum safely. Subtracting the threshold from ladder cost would solve a different problem.

### Alternative and comparison

Kruskal instead sorts all neighboring edges and merges distinct components with DSU. It constructs an optimum in a different order while storing an edge list and component structure.

The primary solution takes `O(N² log N)` time and `O(N²)` additional space. The alternative takes `O(N² log N)` time. Its code shows the states and storage it uses.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.py](submitted_original.py).

## 출처 / Source

- [Programmers — 지형 이동](https://school.programmers.co.kr/learn/courses/30/lessons/62050): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.
