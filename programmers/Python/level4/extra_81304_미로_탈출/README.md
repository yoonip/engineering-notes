# 미로 탈출

[Level 4 목록 / Level 4 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

Level 4 · `81304` · Python3 · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/81304)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py)

## 문제와 조건

함정 방에 들어갈 때 그 방의 활성 상태가 바뀌고 연결 통로 방향도 뒤집힙니다. 같은 방에 다시 와도 활성 함정 조합이 다르면 갈 수 있는 길이 다릅니다.

입력 범위와 상수는 다음과 같습니다. 기호는 코드의 매개변수에 맞췄습니다.

`2≤n≤1000; 1≤roads≤3000; positive weights≤3000; 0≤traps≤10; start/end are not traps; escape exists.`

## 풀이를 따라가기

방 번호와 함정 비트마스크를 하나의 상태로 묶어 다익스트라를 수행합니다. 통로 양 끝 활성 여부가 서로 다를 때만 원래 방향이 반대가 됩니다. 도착 방이 함정이면 이동한 다음 비트를 바꿉니다.

확장 상태에서는 통로와 가중치가 고정되고 모든 이동 시간이 양수입니다. 따라서 일반 다익스트라의 최단 거리 확정 논리를 그대로 적용합니다. 방 번호만으로 방문을 막으면 필요한 재방문이 사라집니다.

## 다른 방법과 비교

대안은 확장 그래프를 Bellman–Ford 반복 완화로 풉니다. 우선순위 큐와 다른 기준으로 전이를 검사하지만 n≤20·함정≤4의 작은 입력에 한정합니다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O((n+E)·2^T log(n·2^T))` | `O(n·2^T+E)` |
| 대안 풀이 | `O(n·E·4^T)` | `O(n·2^T+E)` |

E는 통로 수, T는 함정 수입니다. 함정 조합은 2^T가지입니다.

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었습니다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교합니다. 실행 기록은 [validation.json](validation.json)에 있습니다. 원본 제출 파일은 [submitted_original.py](submitted_original.py)에 그대로 보관했습니다.

```bash
python test_solution.py
```

## English

### Problem and constraints

Entering a trap toggles its activation and incident edge directions. Revisiting a room with a different trap mask is a different state.

Input limits and constants, using the parameter names in the code:

`2≤n≤1000; 1≤roads≤3000; positive weights≤3000; 0≤traps≤10; start/end are not traps; escape exists.`

### Following the solution

Run Dijkstra on room/mask pairs. An edge reverses exactly when endpoint activation bits differ; toggle the destination trap after traversal.

The expanded graph has fixed transitions and positive costs, so ordinary Dijkstra correctness applies. Marking only room identifiers visited would wrongly suppress necessary returns.

### Alternative and comparison

The alternative relaxes the expanded graph with Bellman–Ford. It independently checks transitions without a priority queue, restricted to twenty rooms and four traps.

E counts roads and T counts traps, giving 2^T activation masks.

The primary solution takes `O((n+E)·2^T log(n·2^T))` time and `O(n·2^T+E)` additional space. The alternative takes `O(n·E·4^T)` time. Its additional space is `O(n·2^T+E)`.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.py](submitted_original.py).

## 출처 / Source

- [Programmers — 미로 탈출](https://school.programmers.co.kr/learn/courses/30/lessons/81304): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.
