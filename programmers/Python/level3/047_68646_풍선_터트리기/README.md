# 풍선 터트리기

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

Level 3 · [68646 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/68646)

## 문제와 조건

인접한 두 풍선 중 큰 수를 지우되 작은 수를 지우는 예외는 최대 한 번 허용할 때 마지막까지 남길 수 있는 풍선 수를 구합니다.

`1≤N≤1,000,000; −10^9≤a[i]≤10^9; all values distinct`

## 풀이를 따라가기

1. 왼쪽과 오른쪽 모두에 자신보다 작은 풍선이 있으면 작은 풍선을 두 번 터뜨려야 해서 불가능합니다. 한쪽의 최솟값이면 생존 가능합니다.
2. 예: [9,-1,-5]의 왼쪽 최소 기록은 9,-1,-5, 오른쪽은 -5. 중복 -5를 빼면 3개.
3. 양쪽에서 최솟값이 갱신되는 원소 수를 더하고 전체 최솟값의 중복 1개를 뺍니다. 시간 O(N), 추가 공간 O(1).

## 왜 이 방법으로 풀 수 있나

왼쪽과 오른쪽 모두에 자신보다 작은 풍선이 있으면 작은 풍선을 두 번 터뜨려야 해서 불가능합니다. 한쪽의 최솟값이면 생존 가능합니다.

시간·공간: 시간 O(N), 추가 공간 O(1).

## 다른 방법과 비교

각 위치 왼쪽의 최솟값과 오른쪽의 최솟값을 미리 저장합니다. 현재 값보다 작은 값이 양쪽 모두에 있으면 살릴 수 없습니다.

| 항목 | 기본 풀이 | 양쪽 최소값 배열 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(N), 추가 공간 O(1). | O(N), 공간 O(N) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[[9, -1, -5]]` | `3` |
| `[[-16, 27, 65, -2, 58, -92, -71, -68, -61, -33]]` | `6` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Count balloons that can survive when the larger of adjacent balloons is removed, with at most one exception allowing the smaller to be removed.

`1≤N≤1,000,000; −10^9≤a[i]≤10^9; all values distinct`

### Method and correctness

A balloon can survive if it is a strict minimum from the left or from the right. If a smaller balloon exists on both sides, retaining it would need the forbidden larger-balloon deletion twice. Count record minima in both directions and subtract the global minimum counted twice; all values are distinct.

Main complexity: O(N) time, O(1) extra state.

### Alternative and trade-offs

Precompute prefix and suffix minima. A balloon is impossible to retain exactly when a smaller balloon exists on both sides. This uses arrays instead of counting record minima in two scans.

Code: [alternative.py](alternative.py).

Complexity: O(N), space O(N).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 풍선 터트리기](https://school.programmers.co.kr/learn/courses/30/lessons/68646) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 44개 입력에서 88회 검사를 통과했습니다.

Passed 88 implementation checks across 44 official, boundary and fixed-seed differential inputs.
