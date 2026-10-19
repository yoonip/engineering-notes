# 미로 탈출 명령어

Level 3 · [150365 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/150365)

## 문제와 조건

격자 안에서 출발점부터 목표까지 정확히 k번 이동하는 경로 중 사전순으로 가장 앞선 명령 문자열을 구합니다. 같은 칸을 다시 방문해도 됩니다.

`2≤n,m≤50; 1≤x,r≤n; 1≤y,c≤m; (x,y)≠(r,c); 1≤k≤2,500`

## 풀이를 따라가기

1. 정확히 남은 횟수로 도착하려면 최단거리 이하의 이동 횟수를 줄 수 없고, 여분은 왕복 이동처럼 짝수여야 합니다.
2. 매 칸마다 d·l·r·u 사전순으로 보면서 이 조건을 만족하는 첫 방향을 고르면 가장 앞선 경로가 됩니다. 시간 O(K), 공간 O(K).
3. 예: 3×4 격자의 (2,3)에서 (3,1)까지 5칸이면 가능한 가장 작은 접두사를 차례로 확정해 dllrl을 얻습니다.

## 왜 이 방법으로 풀 수 있나

정확히 남은 횟수로 도착하려면 최단거리 이하의 이동 횟수를 줄 수 없고, 여분은 왕복 이동처럼 짝수여야 합니다.

시간·공간: 시간 O(K), 공간 O(K).

## 다른 방법과 비교

목표에서 거꾸로 정확히 몇 걸음에 도달할 수 있는지 표를 만듭니다. 이 표를 보고 사전순으로 경로를 복원합니다. 맨해튼 거리·짝수 성질을 쓰지 않는 독립 비교 방법입니다.

| 항목 | 기본 풀이 | 남은 횟수별 도달 가능 DP |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(K), 공간 O(K). | O(knm), 공간 O(knm), 작은 입력 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[3, 4, 2, 3, 3, 1, 5]` | `"dllrl"` |
| `[2, 2, 1, 1, 2, 2, 2]` | `"dr"` |
| `[3, 3, 1, 2, 3, 3, 4]` | `"impossible"` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Find the lexicographically smallest in-bounds route reaching the target in exactly k moves. Revisiting cells is allowed.

`2≤n,m≤50; 1≤x,r≤n; 1≤y,c≤m; (x,y)≠(r,c); 1≤k≤2,500`

### Method and correctness

The Manhattan distance must not exceed the remaining move count, and their difference must be even. With both dimensions at least two, spare even moves can be spent on backtracking. At each step try d,l,r,u in lexical order and accept the first in-bounds move satisfying this feasibility test. Each chosen prefix is the smallest prefix that can still complete the route.

Main complexity: O(k) time and output space.

### Alternative and trade-offs

Build reachability sets backwards from the destination for each exact number of remaining moves, then reconstruct lexicographically. This checks the Manhattan-distance/parity rule independently.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: O(knm), space O(knm), small-input checking.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 미로 탈출 명령어](https://school.programmers.co.kr/learn/courses/30/lessons/150365) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 45개 입력에서 90회 검사를 통과했습니다.

Passed 90 implementation checks across 45 official, boundary and fixed-seed differential inputs.
