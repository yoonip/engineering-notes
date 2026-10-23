# 사라지는 발판

Level 3 · [92345 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/92345)

## 문제와 조건

이동하면 떠난 칸이 사라지는 보드 게임에서 두 플레이어가 최적으로 움직일 때 게임이 끝나기까지의 이동 횟수를 구합니다.

두 시작 칸은 발판이 있고 같은 칸이어도 됩니다. 상대 칸으로도 이동할 수 있습니다.

`1≤N,M≤5; board[r][c]∈{0,1}; 0≤r<N; 0≤c<M`

## 풀이를 따라가기

1. 미니맥스는 상대도 최적으로 움직인다고 보고 자신의 최선의 선택을 구하는 게임 탐색입니다. 현재 플레이어 기준으로 이기면 최소 이동, 반드시 지면 최대 이동을 택합니다.
2. 이동할 때 발판 하나를 지우고 플레이어 역할을 바꿉니다. 보드 비트마스크·두 위치를 캐시 키로 써 같은 게임 상태를 재사용합니다. 발판 P≤25, 도달 상태 수 S≤2^P·P²에서 시간 O(S), 캐시·보드 공간 O(S+P)
3. 예: 두 플레이어가 같은 칸에 있을 때 한 명이 떠나면 그 칸이 사라져 다음 플레이어가 즉시 집니다. 시작부터 이동할 곳이 없으면 이동 횟수는 0입니다.

## 왜 이 방법으로 풀 수 있나

미니맥스는 상대도 최적으로 움직인다고 보고 자신의 최선의 선택을 구하는 게임 탐색입니다. 현재 플레이어 기준으로 이기면 최소 이동, 반드시 지면 최대 이동을 택합니다.

시간·공간: 발판 P≤25, 도달 상태 수 S≤2^P·P²에서 시간 O(S), 캐시·보드 공간 O(S+P)

## 다른 방법과 비교

비트마스크 대신 실제 보드를 한 칸 지웠다가 재귀가 끝나면 복원합니다. 캐시가 없어 느리지만 발판 소멸과 플레이어 교대 규칙을 눈으로 확인하기 쉽습니다.

| 항목 | 기본 풀이 | 보드 복원 미니맥스 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 발판 P≤25, 도달 상태 수 S≤2^P·P²에서 시간 O(S), 캐시·보드 공간 O(S+P) | 최악 지수 시간, 재귀·보드 공간 O(NM), 작은 보드 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[[[1, 1, 1], [1, 1, 1], [1, 1, 1]], [1, 0], [1, 2]]` | `5` |
| `[[[1, 1, 1], [1, 0, 1], [1, 1, 1]], [1, 0], [1, 2]]` | `4` |
| `[[[1, 1, 1, 1, 1]], [0, 0], [0, 4]]` | `4` |
| `[[[1]], [0, 0], [0, 0]]` | `0` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Return the game length under optimal play when each departed tile disappears. A winner finishes quickly and a forced loser prolongs the game.

Both starting cells have tiles; starts may coincide, and moving onto the opponent’s cell is allowed.

`1≤N,M≤5; board[r][c]∈{0,1}; 0≤r<N; 0≤c<M`

### Method and correctness

Memoized minimax stores the remaining-tile bitmask and both player positions. Remove the moving player’s old tile, then swap player roles. If any move forces the opponent to lose, choose the fastest such win. If every move loses, prolong the game as much as possible. A missing current tile or no legal move loses immediately.

Main complexity: Exponential worst-case time and cached state space.

### Alternative and trade-offs

Mutate one board cell before recursion and restore it afterwards. Without memoization it is slower, but independently checks disappearing tiles and player swapping.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: exponential worst-case time, recursion and board space O(NM), small-board checking.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 사라지는 발판](https://school.programmers.co.kr/learn/courses/30/lessons/92345) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 45개 입력에서 90회 검사를 통과했습니다.

Passed 90 implementation checks across 45 official, boundary and fixed-seed differential inputs.
