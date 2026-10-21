# 퍼즐 조각 채우기

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

Level 3 · [84021 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/84021)

## 문제와 조건

테이블의 조각을 회전·이동해 게임 보드의 빈 공간에 정확히 넣어 채울 수 있는 최대 칸 수를 구합니다.

회전은 허용하지만 반사는 허용하지 않습니다. 조각은 나눌 수 없고 빈 공간과 정확히 맞아야 합니다.

`3≤N≤50; board/table=N×N; entries∈{0,1}; 1≤component size≤6`

## 풀이를 따라가기

1. DFS로 빈 공간과 조각을 추출하고, 회전한 네 모양을 같은 대표값으로 바꿔 Counter로 일치시킵니다.
2. 예: 4칸짜리 빈 공간과 회전해서 같은 4칸 조각이 만나면 4칸 추가하고 조각 수를 하나 줄입니다. 반사는 허용하지 않습니다.
3. 조각 크기는 최대 6이므로 시간·공간 O(N²). 동일한 빈 공간에는 동일 모양 조각만 들어가므로 개수만 맞추면 됩니다.

## 왜 이 방법으로 풀 수 있나

DFS로 빈 공간과 조각을 추출하고, 회전한 네 모양을 같은 대표값으로 바꿔 Counter로 일치시킵니다.

시간·공간: 시간·공간 O(N²). 동일한 빈 공간에는 동일 모양 조각만 들어가므로 개수만 맞추면 됩니다.

## 다른 방법과 비교

빈 공간과 조각을 각각 추출한 뒤 네 회전을 직접 비교합니다. 같은 모양을 Counter로 세는 대신 이분 매칭으로 조각의 중복 사용을 막습니다.

| 항목 | 기본 풀이 | 모양 쌍 비교와 이분 매칭 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간·공간 O(N²). 동일한 빈 공간에는 동일 모양 조각만 들어가므로 개수만 맞추면 됩니다. | 조각 수 H,P에서 O(HP·6 log 6+H²P), 공간 O(N²+HP) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[[[1, 1, 0, 0, 1, 0], [0, 0, 1, 0, 1, 0], [0, 1, 1, 0, 0, 1], [1, 1, 0, 1, 1, 1], [1, 0, 0, 0, 1, 0], [0, 1, 1, 1, 0, 0]], [[1, 0, 0, 1, 1, 0], [1, 0, 1, 0, 1, 0], [0, 1, 1, 0, 1, 1], [0, 0, 1, 0, 0, 0], [1, 1, 0, 1, 1, 0], [0, 1, 0, 0, 0, 0]]]` | `14` |
| `[[[0, 0, 0], [1, 1, 0], [1, 1, 1]], [[1, 1, 1], [1, 0, 0], [0, 0, 0]]]` | `0` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Rotate and translate unsplit pieces to exactly fill board holes, maximizing filled cells.

Rotation is allowed but reflection is not. Pieces cannot be split and must exactly fill a connected hole.

`3≤N≤50; board/table=N×N; entries∈{0,1}; 1≤component size≤6`

### Method and correctness

Extract connected holes and pieces by graph traversal. Normalize coordinates after every rotation and choose a canonical representation among four rotations; reflection is not allowed. Count available pieces by canonical shape and consume one for each matching hole. Exact shape classes do not compete with different classes, so per-class counting maximizes filled cells.

Main complexity: O(N²) time and space under the six-cell component bound.

### Alternative and trade-offs

Extract holes and pieces, compare all four rotations pairwise, and use bipartite matching to prevent reuse. This differs from counting canonical shapes in a Counter.

Code: [alternative.py](alternative.py).

Complexity: piece counts H,Pwith O(HP·6 log 6+H²P), space O(N²+HP).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 퍼즐 조각 채우기](https://school.programmers.co.kr/learn/courses/30/lessons/84021) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 42개 입력에서 84회 검사를 통과했습니다.

Passed 84 implementation checks across 42 official, boundary and fixed-seed differential inputs.
