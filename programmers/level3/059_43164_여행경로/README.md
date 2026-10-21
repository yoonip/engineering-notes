# 여행경로

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

Level 3 · [43164 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/43164)

## 문제와 조건

ICN에서 출발해 모든 항공권을 정확히 한 번 쓰는 경로 중 사전순 최솟값을 구합니다.

모든 항공권을 정확히 한 번 쓰는 경로가 보장되며, 여러 경로면 사전순 최솟값을 고릅니다.

`3≤airports≤10,000; airport code=[A-Z]{3}; start=ICN`

## 풀이를 따라가기

1. 모든 항공권을 간선으로 한 오일러 경로를 만듭니다. 작은 공항부터 탐색하되 막힌 공항은 뒤에서 확정하므로 중간에 표가 남는 단순 탐욕의 실패를 피합니다.
2. 예: ICN→AAA가 막다른 길이고 ICN→BBB→ICN도 있으면 최종 경로는 ICN→BBB→ICN→AAA입니다.
3. 항공권 T장일 때 시간 O(T log T), 공간 O(T). 스택을 사용해 재귀 깊이 제한도 피합니다.

## 왜 이 방법으로 풀 수 있나

모든 항공권을 간선으로 한 오일러 경로를 만듭니다. 작은 공항부터 탐색하되 막힌 공항은 뒤에서 확정하므로 중간에 표가 남는 단순 탐욕의 실패를 피합니다.

시간·공간: 시간 O(T log T), 공간 O(T). 스택을 사용해 재귀 깊이 제한도 피합니다.

## 다른 방법과 비교

항공권을 목적지 사전순으로 하나씩 선택하고 막히면 되돌립니다. 처음 완성되는 경로가 사전순 최솟값입니다. 오일러 경로보다 최악 시간은 훨씬 큽니다.

| 항목 | 기본 풀이 | 항공권 사용 상태 백트래킹 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(T log T), 공간 O(T). 스택을 사용해 재귀 깊이 제한도 피합니다. | 최악 O(T!·T), 작은 항공권 수 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[[["ICN", "JFK"], ["HND", "IAD"], ["JFK", "HND"]]]` | `["ICN", "JFK", "HND", "IAD"]` |
| `[[["ICN", "SFO"], ["ICN", "ATL"], ["SFO", "ATL"], ["ATL", "ICN"], ["ATL", "SFO"]]]` | `["ICN", "ATL", "ICN", "SFO", "ATL", "SFO"]` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Return the lexicographically smallest itinerary from ICN using every ticket exactly once.

A route using every ticket exactly once is guaranteed; choose the lexicographically smallest route.

`3≤airports≤10,000; airport code=[A-Z]{3}; start=ICN`

### Method and correctness

Construct an Euler trail using every ticket once. Sort outgoing destinations so the smallest is consumed first, but finalize airports only at dead ends and reverse the postorder result. This Hierholzer construction avoids getting stuck after a locally smallest but premature terminal edge. An iterative stack avoids recursion depth issues.

Main complexity: O(T log T) time, O(T) space.

### Alternative and trade-offs

Try outgoing tickets in lexical order and backtrack at dead ends. The first complete route is lexicographically smallest, but worst-case time is much larger than the Euler-trail algorithm.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: worst case O(T!·T), small-ticket oracle.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 여행경로](https://school.programmers.co.kr/learn/courses/30/lessons/43164) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 42개 입력에서 84회 검사를 통과했습니다.

Passed 84 implementation checks across 42 official, boundary and fixed-seed differential inputs.
