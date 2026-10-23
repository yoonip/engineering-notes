# 불량 사용자

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

Level 3 · [64064 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/64064)

## 문제와 조건

별표로 가린 각 불량 사용자 패턴에 서로 다른 사용자를 대응시킬 때 가능한 최종 제재 사용자 집합 수를 구합니다.

`1≤users≤8; 1≤patterns≤users; 1≤string length≤8`

## 풀이를 따라가기

1. 패턴마다 대응 가능한 사용자를 찾고, 기존 선택 조합에 아직 쓰지 않은 사용자 한 명을 추가합니다. 비트마스크 집합이 순서 중복을 제거합니다.
2. 예: 같은 *rodo 패턴 둘에 frodo·crodo를 배정하는 순서는 두 가지지만 최종 마스크는 같아서 한 번만 셉니다.
3. 사용자 N≤8, 패턴 B≤8, 아이디 길이 L≤8. 시간 O(B·N·(L+2^N)), 공간 O(2^N).

## 왜 이 방법으로 풀 수 있나

패턴마다 대응 가능한 사용자를 찾고, 기존 선택 조합에 아직 쓰지 않은 사용자 한 명을 추가합니다. 비트마스크 집합이 순서 중복을 제거합니다.

시간·공간: 시간 O(B·N·(L+2^N)), 공간 O(2^N).

## 다른 방법과 비교

패턴 개수만큼 사용자를 순서 있게 뽑아 하나씩 매칭합니다. 최종 사용자 집합으로 중복을 제거합니다. 비트마스크 DP보다 중복 탐색이 많지만 직접적입니다.

| 항목 | 기본 풀이 | 순열 배정 후 집합 중복 제거 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(B·N·(L+2^N)), 공간 O(2^N). | O(N!/(N-B)!·BL), 공간 O(조합(N,B)) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[["frodo", "fradi", "crodo", "abc123", "frodoc"], ["fr*d*", "abc1**"]]` | `2` |
| `[["frodo", "fradi", "crodo", "abc123", "frodoc"], ["*rodo", "*rodo", "******"]]` | `2` |
| `[["frodo", "fradi", "crodo", "abc123", "frodoc"], ["fr*d*", "*rodo", "******", "******"]]` | `3` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Count distinct final user sets that can be assigned injectively to the wildcard banned patterns.

`1≤users≤8; 1≤patterns≤users; 1≤string length≤8`

### Method and correctness

Find matching users for each wildcard pattern. Extend each current user bitmask with one unused matching user, collecting masks in a set. This removes duplicate assignment orders while retaining distinct final banned-user sets. Length must match exactly; a wildcard replaces one character only.

Main complexity: O(BN(L+2^N)) time, O(2^N) states.

### Alternative and trade-offs

Enumerate ordered user assignments to patterns, check each wildcard match, and deduplicate final user sets. This is more repetitive than bitmask DP but follows the assignment definition directly.

Code: [alternative.py](alternative.py).

Complexity: O(N!/(N-B)!·BL), space O(C(N,B)).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 불량 사용자](https://school.programmers.co.kr/learn/courses/30/lessons/64064) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 44개 입력에서 88회 검사를 통과했습니다.

Passed 88 implementation checks across 44 official, boundary and fixed-seed differential inputs.
