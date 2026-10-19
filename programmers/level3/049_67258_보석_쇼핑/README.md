# 보석 쇼핑

Level 3 · [67258 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/67258)

## 문제와 조건

모든 보석 종류를 한 개 이상 포함하는 가장 짧은 연속 진열 구간을 구합니다. 길이가 같으면 앞 구간입니다.

`1≤N≤100,000; 1≤gem-name length≤10`

## 풀이를 따라가기

1. 오른쪽 끝을 늘려 모든 종류를 모으고, 조건을 만족하는 동안 왼쪽 끝을 줄여 최단 구간을 찾습니다.
2. 예제 1은 1~7번을 모은 뒤 중복된 앞 보석을 빼면 3~7번이 됩니다. 두 포인터는 뒤로 돌아가지 않습니다.
3. 시간 O(N), 공간 O(보석 종류 수). 동점에는 갱신하지 않아 시작 번호가 가장 작은 구간을 반환합니다.

## 왜 이 방법으로 풀 수 있나

오른쪽 끝을 늘려 모든 종류를 모으고, 조건을 만족하는 동안 왼쪽 끝을 줄여 최단 구간을 찾습니다.

시간·공간: 시간 O(N), 공간 O(보석 종류 수). 동점에는 갱신하지 않아 시작 번호가 가장 작은 구간을 반환합니다.

## 다른 방법과 비교

길이를 고정해 모든 종류를 포함하는 창이 있는지 검사합니다. 길이를 늘리면 가능성이 유지되므로 이분탐색합니다. 기본 두 포인터보다 느리지만 다른 단조 조건을 이용합니다.

| 항목 | 기본 풀이 | 구간 길이 이분탐색 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(N), 공간 O(보석 종류 수). 동점에는 갱신하지 않아 시작 번호가 가장 작은 구간을 반환합니다. | O(N log N), 공간 O(종류 수) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[["DIA", "RUBY", "RUBY", "DIA", "DIA", "EMERALD", "SAPPHIRE", "DIA"]]` | `[3, 7]` |
| `[["AA", "AB", "AC", "AA", "AC"]]` | `[1, 3]` |
| `[["XYZ", "XYZ", "XYZ"]]` | `[1, 1]` |
| `[["ZZZ", "YYY", "NNNN", "YYY", "BBB"]]` | `[1, 5]` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Find the shortest contiguous interval containing every gem type, preferring the earlier start on ties.

`1≤N≤100,000; 1≤gem-name length≤10`

### Method and correctness

Expand the right end while counting gem types. Once all types are present, move the left end rightward as long as the window remains valid, recording shorter windows. Both pointers move only forward. Strictly shorter updates preserve the earliest starting index on ties.

Main complexity: O(N) time, O(gem types) space.

### Alternative and trade-offs

Binary-search a window length and test whether any window contains every gem type. Feasibility is monotone in length, giving a different formulation from two pointers.

Code: [alternative.py](alternative.py).

Complexity: O(N log N), space O(distinct types).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 보석 쇼핑](https://school.programmers.co.kr/learn/courses/30/lessons/67258) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 46개 입력에서 92회 검사를 통과했습니다.

Passed 92 implementation checks across 46 official, boundary and fixed-seed differential inputs.
