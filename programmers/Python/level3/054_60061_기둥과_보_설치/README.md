# 기둥과 보 설치

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

Level 3 · [60061 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/60061)

## 문제와 조건

기둥·보의 지지 규칙을 지키는 설치·삭제만 적용한 뒤 최종 구조물을 정렬해 반환합니다.

벽을 벗어나는 설치, 중복 설치, 없는 구조물 삭제는 없습니다. 출력은 x,y,종류 오름차순입니다.

`5≤n≤100; 1≤Q≤1,000; commands=[x,y,kind,action]; kind,action∈{0,1}`

## 풀이를 따라가기

1. 기둥·보의 지지 조건을 함수로 옮겨 시뮬레이션합니다. 설치는 새 구조물만 검사하고, 삭제는 남은 구조물을 전부 확인해 실패하면 되돌립니다.
2. 예제 2에서 보를 지워 다른 보가 떠버리는 삭제는 취소됩니다. 집합에 없는 음수 좌표 구조물은 in 검사에서 자연스럽게 거짓이 됩니다.
3. 명령 수 Q≤1000. 시간 O(Q² + Q log Q), 공간 O(Q).

## 왜 이 방법으로 풀 수 있나

기둥·보의 지지 조건을 함수로 옮겨 시뮬레이션합니다. 설치는 새 구조물만 검사하고, 삭제는 남은 구조물을 전부 확인해 실패하면 되돌립니다.

시간·공간: 시간 O(Q² + Q log Q), 공간 O(Q).

## 다른 방법과 비교

구조물 하나를 임시로 추가·삭제한 뒤 그 변화의 영향을 받을 수 있는 주변 기둥·보만 검사합니다. 전체 구조물을 다시 확인하는 기본 풀이보다 검사가 작아집니다.

| 항목 | 기본 풀이 | 변경 주변만 지지 검사 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(Q² + Q log Q), 공간 O(Q). | O(Q+Q log Q), 공간 O(Q) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[5, [[1, 0, 0, 1], [1, 1, 1, 1], [2, 1, 0, 1], [2, 2, 1, 1], [5, 0, 0, 1], [5, 1, 0, 1], [4, 2, 1, 1], [3, 2, 1, 1]]]` | `[[1, 0, 0], [1, 1, 1], [2, 1, 0], [2, 2, 1], [3, 2, 1], [4, 2, 1], [5, 0, 0], [5, 1, 0]]` |
| `[5, [[0, 0, 0, 1], [2, 0, 0, 1], [4, 0, 0, 1], [0, 1, 1, 1], [1, 1, 1, 1], [2, 1, 1, 1], [3, 1, 1, 1], [2, 0, 0, 0], [1, 1, 1, 0], [2, 2, 0, 1]]]` | `[[0, 0, 0], [0, 1, 1], [1, 1, 1], [2, 1, 1], [3, 1, 1], [4, 0, 0]]` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Apply only installations and removals preserving pillar/beam support rules, then return the sorted final structures.

There are no out-of-bounds installations, duplicate structures, or deletions of missing structures. Sort output by x, y, and kind.

`5≤n≤100; 1≤Q≤1,000; commands=[x,y,kind,action]; kind,action∈{0,1}`

### Method and correctness

Store installed pillars and beams in a set and encode their support rules exactly. A new structure only needs its own support checked. Temporarily remove a requested structure and validate all remaining structures; undo deletion if any becomes unsupported. Sort final structures by x, then y, then kind.

Main complexity: O(Q²+Q log Q) time, O(Q) space.

### Alternative and trade-offs

Temporarily apply an operation and validate only nearby structures whose supports could change. This avoids rechecking every installed structure after each deletion.

Code: [alternative.py](alternative.py).

Complexity: O(Q+Q log Q), space O(Q).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 기둥과 보 설치](https://school.programmers.co.kr/learn/courses/30/lessons/60061) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 43개 입력에서 86회 검사를 통과했습니다.

Passed 86 implementation checks across 43 official, boundary and fixed-seed differential inputs.
