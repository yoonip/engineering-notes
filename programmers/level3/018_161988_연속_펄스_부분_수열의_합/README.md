# 연속 펄스 부분 수열의 합

Level 3 · [161988 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/161988)

## 문제와 조건

연속 부분수열에 +1,−1이 번갈아 나오는 펄스를 곱했을 때 가능한 합의 최댓값을 구합니다. 시작 부호는 두 가지 모두 가능합니다.

`1≤N≤500,000; −100,000≤sequence[i]≤100,000`

## 풀이를 따라가기

1. 전체 수열에 +1,-1을 번갈아 곱한 뒤 누적합을 구합니다. 어떤 구간의 합은 두 누적합의 차이입니다.
2. 반대 부호의 펄스도 허용되므로 구간 합 절댓값의 최댓값을 찾으면 됩니다. 이는 전체 누적합의 최댓값-최솟값입니다. 시간 O(N), 추가 공간 O(1).
3. 예: [2,3,-6,1,3,-1,2,4]를 변환한 누적합은 0,2,-1,-7,-8,-5,-4,-2,-6. 최대 2와 최소 -8의 차이는 10입니다.

## 왜 이 방법으로 풀 수 있나

전체 수열에 +1,-1을 번갈아 곱한 뒤 누적합을 구합니다. 어떤 구간의 합은 두 누적합의 차이입니다.

시간·공간: 시간 O(N), 추가 공간 O(1).

## 다른 방법과 비교

두 가지 펄스를 각각 적용하며 현재 위치에서 끝나는 최대 부분합을 갱신합니다. 누적합의 최댓값·최솟값 차이를 쓰는 기본 풀이와 달리 부분수열을 직접 연장할지 결정합니다.

| 항목 | 기본 풀이 | 두 부호 Kadane DP |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(N), 추가 공간 O(1). | O(N), 공간 O(1) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[[2, 3, -6, 1, 3, -1, 2, 4]]` | `10` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Maximize a contiguous subarray sum after alternating +1/−1 multiplication, allowing either starting sign.

`1≤N≤500,000; −100,000≤sequence[i]≤100,000`

### Method and correctness

Multiply the entire sequence by alternating +1 and −1 and form prefix sums, including the initial zero. A subarray sum is a difference of two prefixes. Because either pulse sign is allowed, its absolute value is achievable regardless of the prefixes’ time order. The answer is therefore maximum prefix minus minimum prefix. One pass and constant extra state suffice.

Main complexity: O(N) time, O(1) extra space.

### Alternative and trade-offs

Run Kadane DP for both alternating signs. Unlike the prefix-range solution, it explicitly decides whether to extend the current subarray.

Code: [alternative.py](alternative.py). Scope: alternative implementation.

Complexity: O(N), space O(1).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 연속 펄스 부분 수열의 합](https://school.programmers.co.kr/learn/courses/30/lessons/161988) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 44개 입력에서 88회 검사를 통과했습니다.

Passed 88 implementation checks across 44 official, boundary and fixed-seed differential inputs.
