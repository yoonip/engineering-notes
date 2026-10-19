# 카드 짝 맞추기

Level 3 · [72415 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/72415)

## 문제와 조건

방향키·Ctrl 이동·Enter로 4×4 카드 쌍을 모두 제거하는 최소 키 입력 횟수를 구합니다.

`board=4×4; entries∈{0,…,6}; each card type occurs twice; 0≤r,c≤3`

## 풀이를 따라가기

1. 남은 카드 종류를 비트마스크로 표시하고, 다음에 없앨 카드 쌍과 두 장을 뒤집는 순서를 모두 비교한다.
2. 각 상태의 이동 비용은 일반 이동·Ctrl 이동을 간선으로 한 BFS로 구한다. Enter 두 번 후에만 두 카드가 사라진다.
3. 예제 첫 보드는 이동 8번+Enter 6번=14. 종류 K≤6, 보드 칸 수 V=16일 때 시간 O(2^K·V·(V+K)), 공간 O(2^K·V²).

## 왜 이 방법으로 풀 수 있나

남은 카드 종류를 비트마스크로 표시하고, 다음에 없앨 카드 쌍과 두 장을 뒤집는 순서를 모두 비교한다.

시간·공간: 시간 O(2^K·V·(V+K)), 공간 O(2^K·V²).

## 다른 방법과 비교

남은 카드 위치, 커서, 첫 선택 카드를 상태로 두고 실제 방향키·Ctrl·Enter 한 번씩을 간선으로 탐색합니다. 카드쌍 단위 DP와 달리 조작 하나하나를 직접 검증합니다.

| 항목 | 기본 풀이 | 키 입력 전체 상태 BFS |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(2^K·V·(V+K)), 공간 O(2^K·V²). | 최대 O(2^(2P)·16²), 작은 카드 수 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[[[1, 0, 0, 3], [2, 0, 0, 0], [0, 0, 0, 2], [3, 0, 1, 0]], 1, 0]` | `14` |
| `[[[3, 0, 0, 2], [0, 0, 1, 0], [0, 1, 0, 0], [2, 0, 0, 3]], 0, 1]` | `16` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Minimize arrow, Ctrl-arrow and Enter presses needed to remove every card pair on a 4×4 board.

`board=4×4; entries∈{0,…,6}; each card type occurs twice; 0≤r,c≤3`

### Method and correctness

For each remaining card-type mask, BFS computes cursor movement including Ctrl jumps against the current cards. DP tries both selection orders of every pair, adds two Enter presses, removes that pair, and solves the remaining mask. The first selected card still occupies its cell until the pair is matched, so both movement distances use the old mask.

Main complexity: O(2^P·P·16) distance states plus pair transitions, exponential in P≤6.

### Alternative and trade-offs

Run BFS over remaining card cells, cursor, and the first selected card. Each arrow, Ctrl-arrow, and Enter is one edge, independently checking the pair-level DP against actual key presses.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: at most O(2^(2P)·16²), small-card oracle.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 카드 짝 맞추기](https://school.programmers.co.kr/learn/courses/30/lessons/72415) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 13개 입력에서 26회 검사를 통과했습니다.

Passed 26 implementation checks across 13 official, boundary and fixed-seed differential inputs.
