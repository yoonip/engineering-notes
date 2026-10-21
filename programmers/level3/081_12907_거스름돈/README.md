# 거스름돈

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

Level 3 · [12907 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12907)

## 문제와 조건

각 화폐를 무한히 사용할 때 n원을 만드는 서로 다른 조합 수를 구합니다. 동전 나열 순서는 구별하지 않습니다.

`1≤n≤100,000; coin types≤100; modulus=1,000,000,007`

## 풀이를 따라가기

1. 화폐 종류별로 금액을 오름차순 갱신합니다. dp[x-coin]의 모든 방법에 현재 동전 하나를 추가하면 x원을 만드는 새 방법이 됩니다.
2. 예: 5원을 [1,2,5]로 만들면 1×5, 1×3+2, 1+2×2, 5의 네 조합. [1,2]와 [2,1]은 같은 방법이라 종류를 바깥에서 반복합니다.
3. 화폐 C종류일 때 시간 O(NC), 공간 O(N). 금액 반복을 내림차순으로 바꾸면 동전당 한 번만 사용하는 다른 문제가 됩니다.

## 왜 이 방법으로 풀 수 있나

화폐 종류별로 금액을 오름차순 갱신합니다. dp[x-coin]의 모든 방법에 현재 동전 하나를 추가하면 x원을 만드는 새 방법이 됩니다.

시간·공간: 시간 O(NC), 공간 O(N). 금액 반복을 내림차순으로 바꾸면 동전당 한 번만 사용하는 다른 문제가 됩니다.

## 다른 방법과 비교

현재 화폐를 0개부터 가능한 개수까지 사용하고 다음 화폐로 넘어갑니다. 조합을 직접 세어 1차원 DP의 바깥 반복 순서를 검증합니다.

| 항목 | 기본 풀이 | 동전 개수 재귀 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(NC), 공간 O(N). 금액 반복을 내림차순으로 바꾸면 동전당 한 번만 사용하는 다른 문제가 됩니다. | 작은 금액에서 조합 탐색, 공간 O(화폐 수) |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[5, [1, 2, 5]]` | `4` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Count unordered ways to make n with unlimited copies of each denomination.

`1≤n≤100,000; coin types≤100; modulus=1,000,000,007`

### Method and correctness

Process denominations outside and amounts in ascending order inside. dp[x−coin] gains one current coin to create a combination for x. This permits unlimited copies without counting different coin orders separately. Descending amount order would instead model single-use coins. Reduce counts modulo 1,000,000,007.

Main complexity: O(amount·coin types) time, O(amount) space.

### Alternative and trade-offs

Choose the count of the current denomination, then move to the next denomination. This counts combinations directly and checks the coin-outer-loop order of the 1D DP.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: combination search for tiny amounts, space O(coin types).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 거스름돈](https://school.programmers.co.kr/learn/courses/30/lessons/12907) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 42개 입력에서 84회 검사를 통과했습니다.

Passed 84 implementation checks across 42 official, boundary and fixed-seed differential inputs.
