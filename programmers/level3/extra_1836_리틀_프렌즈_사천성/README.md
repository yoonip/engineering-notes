# 리틀 프렌즈 사천성

Level 3 · [1836 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/1836)

## 문제와 조건

한 번 이하로 꺾는 빈 경로로 같은 타일 쌍을 지웁니다. 모두 지우는 사전순 최소 순서 또는 IMPOSSIBLE을 구합니다.

`1≤m,n≤100; letters≤26; each letter occurs twice`

## 풀이를 따라가기

1. 한 번만 꺾는 경로는 두 L자 모양 중 하나다. 두 선분을 확인하고 제거 가능한 타일 중 알파벳이 가장 빠른 것을 매번 제거한다.
2. 타일 제거는 다른 경로를 막지 않고 더 열어주므로 현재 제거 가능한 작은 글자를 먼저 골라도 완성 가능성을 잃지 않는다.
3. 예: DBA/C*A/CDB는 처음 A·C가 가능하지만 A를 먼저 골라 ABCD가 된다. 타일 종류 T≤26, 시간 O(MN+T²(M+N)), 공간 O(MN).

## 왜 이 방법으로 풀 수 있나

한 번만 꺾는 경로는 두 L자 모양 중 하나다. 두 선분을 확인하고 제거 가능한 타일 중 알파벳이 가장 빠른 것을 매번 제거한다.

시간·공간: 시간 O(MN+T²(M+N)), 공간 O(MN).

## 다른 방법과 비교

두 L자 선분만 보는 대신 타일 사이의 이동을 (위치, 방향, 꺾은 횟수)로 탐색합니다. 한 번 이하로 꺾어 도달하는 쌍 중 작은 글자부터 제거합니다.

| 항목 | 기본 풀이 | 방향·회전 횟수 경로 BFS |
|---|---|---|
| 코드 | [solution.cpp](solution.cpp) | [alternative.py](alternative.py) |
| 비용 | 시간 O(MN+T²(M+N)), 공간 O(MN). | O(T²MN), 공간 O(MN) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[3, 3, ["DBA", "C*A", "CDB"]]` | `"ABCD"` |
| `[2, 4, ["NRYN", "ARYA"]]` | `"RYAN"` |
| `[4, 4, [".ZI.", "M.**", "MZU.", ".IU."]]` | `"MUZI"` |
| `[2, 2, ["AB", "BA"]]` | `"IMPOSSIBLE"` |

Python 대안은 examples.json과 별도 경계·무작위 입력으로 로컬 검증합니다. C++ 제출본의 실행 결과는 전체 검증 기록에서 구분합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.cpp)

## English

### Task and constraints

Remove equal tile pairs connected through empty space with at most one turn. Return the lexicographically smallest complete removal order, or IMPOSSIBLE.

`1≤m,n≤100; letters≤26; each letter occurs twice`

### Method and correctness

With at most one turn, a connecting path is one of two L shapes. Check both segments and repeatedly remove the smallest currently removable letter. Removing tiles only opens paths and never blocks them, so choosing a smaller available letter cannot destroy a complete solution. If no pair is removable, return IMPOSSIBLE.

Main complexity: O(mn+T²(m+n)) time, O(mn) space; T≤26.

### Alternative and trade-offs

Search tile connectivity with (cell, direction, turn count) states rather than testing two L-shaped paths. Remove the smallest connectable letter, allowing at most one turn.

Code: [alternative.py](alternative.py). Scope: alternative implementation.

Complexity: O(T²MN), space O(MN).

### Verification

The Python alternative is checked with examples.json and separate edge/random cases; C++ execution is recorded separately in the repository validation report.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 리틀 프렌즈 사천성](https://school.programmers.co.kr/learn/courses/30/lessons/1836) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 34개 입력에서 34회 검사를 통과했습니다.

Passed 34 implementation checks across 34 official, boundary and fixed-seed differential inputs.

[Python 비교 원본 / Stored Python comparison source](submitted_original.py)
