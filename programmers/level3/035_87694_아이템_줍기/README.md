# 아이템 줍기

Level 3 · [87694 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/87694)

## 문제와 조건

합쳐진 직사각형 지형의 외곽선만 따라 캐릭터가 아이템에 도달하는 최단거리를 구합니다.

시작과 아이템은 서로 다른 외곽선 위의 점입니다. 직사각형은 문제의 겹침 조건을 따르고 서로 다른 직사각형끼리 같은 x·y 경계 좌표를 공유하지 않습니다.

`1≤R≤4; rectangle/character/item coordinates∈[1,50]`

## 풀이를 따라가기

1. 좌표를 두 배로 확대하고 직사각형들을 전부 채운 뒤, 각 직사각형의 내부를 모두 지워 합친 지형의 테두리를 만듭니다.
2. 테두리 위에서 BFS를 하면 최단 이동 거리입니다. 좌표 확대 때문에 생긴 거리 두 배를 마지막에 나눕니다. 좌표 최대값 C에 대해 시간·공간 O(C²), 직사각형 수는 최대 4입니다.
3. 예: 원래 한 칸 너비의 굴곡도 두 칸 간격으로 표현되어, 인접해 보이는 서로 다른 테두리를 가로지르는 지름길을 막습니다.

## 왜 이 방법으로 풀 수 있나

좌표를 두 배로 확대하고 직사각형들을 전부 채운 뒤, 각 직사각형의 내부를 모두 지워 합친 지형의 테두리를 만듭니다.

시간·공간: 시간·공간 O(C²), 직사각형 수는 최대 4입니다.

## 다른 방법과 비교

직사각형 내부 칸을 채우는 대신 각 테두리 선분만 정점으로 만듭니다. 다른 직사각형의 엄격한 내부에 있는 정점을 제거한 뒤 BFS합니다.

| 항목 | 기본 풀이 | 좌표 확대 경계선 그래프 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간·공간 O(C²), 직사각형 수는 최대 4입니다. | O(R²C+RC), 공간 O(RC) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[[[1, 1, 7, 4], [3, 2, 5, 5], [4, 3, 6, 9], [2, 6, 8, 8]], 1, 3, 7, 8]` | `17` |
| `[[[1, 1, 8, 4], [2, 2, 4, 9], [3, 6, 9, 8], [6, 3, 7, 7]], 9, 7, 6, 1]` | `11` |
| `[[[1, 1, 5, 7]], 1, 1, 4, 7]` | `9` |
| `[[[2, 1, 7, 5], [6, 4, 10, 10]], 3, 1, 7, 10]` | `15` |
| `[[[2, 2, 5, 5], [1, 3, 6, 4], [3, 1, 4, 6]], 1, 4, 6, 3]` | `10` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Find the shortest path from character to item along the exterior boundary of the rectangle union.

Start and item are distinct exterior-boundary points. Rectangles obey the specified overlap geometry and do not share x/y boundary coordinates across rectangles.

`1≤R≤4; rectangle/character/item coordinates∈[1,50]`

### Method and correctness

Double all coordinates, fill the rectangles, then erase their strict interiors. Doubling prevents grid adjacency from cutting across narrow bends. BFS on the remaining boundary gives a shortest boundary route; divide the doubled path length by two. Mark visited points separately or remove them from the traversable boundary.

Main complexity: O(C²) grid space and O(RC²) construction time; R≤4.

### Alternative and trade-offs

Build only rectangle perimeter points at doubled coordinates, discard points strictly inside another rectangle, and run BFS. This checks the filled-grid boundary construction.

Code: [alternative.py](alternative.py).

Complexity: O(R²C+RC), space O(RC).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 아이템 줍기](https://school.programmers.co.kr/learn/courses/30/lessons/87694) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 46개 입력에서 92회 검사를 통과했습니다.

Passed 92 implementation checks across 46 official, boundary and fixed-seed differential inputs.
