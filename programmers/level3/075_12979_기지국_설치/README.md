# 기지국 설치

Level 3 · [12979 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12979)

## 문제와 조건

기존 기지국에 더해 모든 아파트를 덮도록 추가할 기지국의 최소 개수를 구합니다.

`1≤N≤200,000,000; existing stations≤10,000; 1≤W≤10,000`

## 풀이를 따라가기

1. 기존 전파 구간 사이의 빈 구간을 각각 길이 2W+1짜리 전파로 채운다. 길이 L 구간에는 ceil(L/(2W+1))개가 최소로 필요하다.
2. 예: N=11, 기지국 4·11, W=1이면 빈 구간 길이가 2·4라서 1+2=3개. 새 기지국은 왼쪽 미포함 지점을 덮으며 최대한 오른쪽에 놓으면 된다.
3. 기존 기지국 S개일 때 시간 O(S), 공간 O(1). N이 2억이어도 N개 배열이나 반복이 필요 없다.

## 왜 이 방법으로 풀 수 있나

기존 전파 구간 사이의 빈 구간을 각각 길이 2W+1짜리 전파로 채운다. 길이 L 구간에는 ceil(L/(2W+1))개가 최소로 필요하다.

시간·공간: 시간 O(S), 공간 O(1). N이 2억이어도 N개 배열이나 반복이 필요 없다.

## 다른 방법과 비교

아직 덮이지 않은 가장 왼쪽 아파트를 잡습니다. 기존 기지국이 덮으면 건너뛰고, 아니면 그 지점을 덮도록 새 기지국을 최대한 오른쪽에 설치합니다. 구간 길이 나눗셈과 다른 직접 배치입니다.

| 항목 | 기본 풀이 | 미도달 첫 아파트 탐욕 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(S), 공간 O(1). N이 2억이어도 N개 배열이나 반복이 필요 없다. | O(기존+추가 기지국 수), 공간 O(1) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[11, [4, 11], 1]` | `3` |
| `[16, [9], 2]` | `3` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Find the minimum additional stations needed to cover every apartment alongside existing stations.

`1≤N≤200,000,000; existing stations≤10,000; 1≤W≤10,000`

### Method and correctness

Scan uncovered gaps between existing station ranges. A new station covers at most 2W+1 consecutive apartments, so a gap of length L requires ceil(L/(2W+1)) stations. Placing each at the farthest right location that still covers the gap’s first apartment attains that lower bound. No N-sized array is needed.

Main complexity: O(existing stations) time, O(1) extra space.

### Alternative and trade-offs

Track the leftmost uncovered apartment. Skip an existing covered interval or place a new station as far right as possible while covering that apartment. This directly constructs a placement instead of dividing gap lengths.

Code: [alternative.py](alternative.py).

Complexity: O(existing+new stations), space O(1).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 기지국 설치](https://school.programmers.co.kr/learn/courses/30/lessons/12979) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 43개 입력에서 86회 검사를 통과했습니다.

Passed 86 implementation checks across 43 official, boundary and fixed-seed differential inputs.
