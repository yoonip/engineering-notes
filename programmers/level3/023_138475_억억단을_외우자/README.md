# 억억단을 외우자

Level 3 · [138475 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/138475)

## 문제와 조건

각 시작 수부터 e까지 구구단 확장 표에서 가장 많이 등장하는 수를 구합니다. 등장 횟수가 같으면 작은 수를 고릅니다.

`1≤e≤5,000,000; 1≤Q≤min(e,100,000); 1≤start≤e`

## 풀이를 따라가기

1. 정수 x가 곱셈표에 나오는 횟수는 x의 약수 개수입니다. 소인수 지수가 a일 때 약수 선택 수 a+1을 곱하는 체로 개수를 구합니다.
2. 시작점을 내림차순으로 처리하면 오른쪽부터 구간을 늘리며 한 번만 스캔할 수 있습니다. 같은 약수 개수면 더 작은 수로 갱신합니다. 시간 O(E log log E+Q log Q), 공간 O(E+Q).
3. 예: 1~8에서 6과 8의 약수는 네 개로 최다입니다. [1,8]·[3,8]은 작은 수 6, [7,8]은 8이 답입니다.

## 왜 이 방법으로 풀 수 있나

정수 x가 곱셈표에 나오는 횟수는 x의 약수 개수입니다. 소인수 지수가 a일 때 약수 선택 수 a+1을 곱하는 체로 개수를 구합니다.

시간·공간: 시간 O(E log log E+Q log Q), 공간 O(E+Q).

## 다른 방법과 비교

각 약수의 배수를 방문해 약수 개수를 직접 더합니다. 오른쪽부터 최선의 수를 저장하면 시작점마다 상수 시간에 답합니다. 소인수 지수로 세는 기본 풀이보다 느리지만 단순합니다.

| 항목 | 기본 풀이 | 약수 배수 체와 접미 최적값 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(E log log E+Q log Q), 공간 O(E+Q). | O(E log E+Q), 공간 O(E+Q) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[8, [1, 3, 7]]` | `[6, 6, 8]` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

For every start, find the most frequent multiplication-table value in [start,e], preferring the smaller value on a tie.

`1≤e≤5,000,000; 1≤Q≤min(e,100,000); 1≤start≤e`

### Method and correctness

A value appears in the multiplication table once for each positive divisor. Count divisors using a prime-power sieve, multiplying the choices for each exponent. Sort query starts descending and scan the upper range once. On equal divisor counts, replacing the current winner with the smaller scanned value enforces the requested tie break.

Main complexity: O(e log log e+Q log Q) time, O(e+Q) space.

### Alternative and trade-offs

Count divisors by visiting multiples, then build a suffix best-index array. Queries become constant-time; the direct divisor sieve is simpler but slower than the prime-power sieve.

Code: [alternative.py](alternative.py). Scope: alternative implementation.

Complexity: O(E log E+Q), space O(E+Q).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 억억단을 외우자](https://school.programmers.co.kr/learn/courses/30/lessons/138475) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 42개 입력에서 84회 검사를 통과했습니다.

Passed 84 implementation checks across 42 official, boundary and fixed-seed differential inputs.
