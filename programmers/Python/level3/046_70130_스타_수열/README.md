# 스타 수열

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

Level 3 · [70130 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/70130)

## 문제와 조건

길이가 짝수이고 각 쌍의 두 값이 다르면서 모든 쌍에 공통 값이 있는 스타 부분수열의 최대 길이를 구합니다.

`1≤N≤500,000; 0≤a[i]<N`

## 풀이를 따라가기

1. 공통 원소별로 겹치지 않는 유효한 인접 쌍을 왼쪽부터 선택합니다. 각 인접 쌍은 두 숫자의 후보에만 영향을 주므로 전체를 한 번만 훑습니다.
2. 가능한 쌍은 공통값과 다른 값이 만나는 경계의 인접 쌍으로 좁힐 수 있습니다. 가장 먼저 끝나는 쌍을 고르면 뒤에 쓸 공간이 최대한 남습니다.
3. 예제 3은 공통값 0으로 네 쌍을 만들어 길이 8. 시간 O(N), 공간 O(N).

## 왜 이 방법으로 풀 수 있나

공통 원소별로 겹치지 않는 유효한 인접 쌍을 왼쪽부터 선택합니다. 각 인접 쌍은 두 숫자의 후보에만 영향을 주므로 전체를 한 번만 훑습니다.

시간·공간: 시간 O(N), 공간 O(N).

## 다른 방법과 비교

스타 수열에 공통으로 들어갈 값을 하나 고르고 왼쪽부터 겹치지 않는 쌍을 만듭니다. 기본 풀이처럼 모든 값을 동시에 갱신하지 않아 최악 O(N²)입니다.

| 항목 | 기본 풀이 | 공통 값별 탐욕 스캔 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(N), 공간 O(N). | O(N²), 공간 O(N), 작은 입력 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[[0]]` | `0` |
| `[[5, 2, 3, 3, 5, 3]]` | `4` |
| `[[0, 3, 3, 0, 7, 2, 0, 2, 2, 0]]` | `8` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Find the longest even-length subsequence whose unequal-value pairs all contain one common value.

`1≤N≤500,000; 0≤a[i]<N`

### Method and correctness

For each adjacent unequal pair, greedily add a nonoverlapping pair to each of its two candidate common values. Keeping the earliest possible pair leaves the most room for later pairs. Separate last-used indices per candidate let all common values be processed in one scan. Twice the largest pair count is the star-subsequence length.

Main complexity: O(N) time and space.

### Alternative and trade-offs

Choose the common value, then greedily scan nonoverlapping unequal pairs containing it. This handles candidates separately rather than updating all values in one pass.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: O(N²), space O(N), small-input checking.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 스타 수열](https://school.programmers.co.kr/learn/courses/30/lessons/70130) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 45개 입력에서 90회 검사를 통과했습니다.

Passed 90 implementation checks across 45 official, boundary and fixed-seed differential inputs.
