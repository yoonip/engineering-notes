# 네트워크

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

Level 3 · [43162 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/43162)

## 문제와 조건

직접 또는 간접 연결된 컴퓨터들을 하나의 네트워크로 볼 때 서로 다른 네트워크 수를 구합니다.

`1≤n≤200; computers=n×n; computers[i][i]=1`

## 풀이를 따라가기

1. 미방문 컴퓨터를 발견할 때마다 네트워크 수를 하나 늘리고, 연결된 모든 컴퓨터를 DFS로 방문합니다.
2. 예: 0번과 1번이 연결되고 2번이 혼자이면 DFS를 두 번 시작하므로 답은 2.
3. 연결 행렬의 모든 행·열을 검사하므로 시간 O(N²), 추가 공간 O(N).

## 왜 이 방법으로 풀 수 있나

미방문 컴퓨터를 발견할 때마다 네트워크 수를 하나 늘리고, 연결된 모든 컴퓨터를 DFS로 방문합니다.

시간·공간: 시간 O(N²), 추가 공간 O(N).

## 다른 방법과 비교

연결된 컴퓨터의 집합을 합치고 서로 다른 대표의 개수를 셉니다. DFS 대신 연결 관계를 하나씩 처리하는 방식입니다.

| 항목 | 기본 풀이 | Union–Find |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(N²), 추가 공간 O(N). | O(N² α(N)), 공간 O(N) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[3, [[1, 1, 0], [1, 1, 0], [0, 0, 1]]]` | `2` |
| `[3, [[1, 1, 0], [1, 1, 1], [0, 1, 1]]]` | `1` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Count connected computer networks, including indirect connectivity.

`1≤n≤200; computers=n×n; computers[i][i]=1`

### Method and correctness

Start DFS from every unvisited computer and mark its entire connected component. Each new search adds one network. The input is an adjacency matrix, so scanning all rows takes quadratic time even when the graph is sparse.

Main complexity: O(N²) time, O(N) extra space.

### Alternative and trade-offs

Union connected computer pairs and count distinct representatives. This builds components incrementally instead of exploring them by DFS.

Code: [alternative.py](alternative.py).

Complexity: O(N² α(N)), space O(N).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 네트워크](https://school.programmers.co.kr/learn/courses/30/lessons/43162) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 43개 입력에서 86회 검사를 통과했습니다.

Passed 86 implementation checks across 43 official, boundary and fixed-seed differential inputs.
