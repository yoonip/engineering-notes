# N으로 표현

Level 3 · [42895 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/42895)

## 문제와 조건

숫자 N을 이어 쓰거나 사칙연산해 number를 만드는 데 필요한 최소 N 사용 횟수를 구합니다.

괄호·사칙연산·이어 쓰기가 가능하고 나눗셈 나머지는 버립니다. 8개보다 많이 필요하면 −1입니다.

`1≤N≤9; 1≤number≤32,000; maximum N count=8`

## 풀이를 따라가기

1. N을 i번 사용한 결과 집합을 만든다. 붙여 쓰기 외의 수식은 마지막 연산을 기준으로 두 작은 수식으로 나눌 수 있으므로 네 연산을 전부 조합한다.
2. 예: (55+5)/5=12는 왼쪽 세 번·오른쪽 한 번을 조합하여 총 네 번. 음수·0도 이후 수식에 필요할 수 있어 보관한다.
3. 집합 DP로 같은 결과를 한 번만 저장한다. S_i를 N i개로 만든 서로 다른 결과 수라 하면 시간 O(Σ_(k=2..8) Σ_(i=1..k−1) S_i·S_(k−i)), 공간 O(Σ_(k=1..8) S_k)

## 왜 이 방법으로 풀 수 있나

N을 i번 사용한 결과 집합을 만든다. 붙여 쓰기 외의 수식은 마지막 연산을 기준으로 두 작은 수식으로 나눌 수 있으므로 네 연산을 전부 조합한다.

시간·공간: S_i를 N i개로 만든 서로 다른 결과 수라 하면 시간 O(Σ_(k=2..8) Σ_(i=1..k−1) S_i·S_(k−i)), 공간 O(Σ_(k=1..8) S_k)

## 다른 방법과 비교

정확히 k개의 N으로 만든 값들을 재귀적으로 생성하고 캐시합니다. 나눗셈은 음수에서도 0쪽으로 버림하도록 구현합니다. 양방향 연산과 이어 쓰기 모두 포함합니다.

| 항목 | 기본 풀이 | 표현식 개수별 재귀 집합 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | S_i를 N i개로 만든 서로 다른 결과 수라 하면 시간 O(Σ_(k=2..8) Σ_(i=1..k−1) S_i·S_(k−i)), 공간 O(Σ_(k=1..8) S_k) | 집합 크기 S_k에서 Σ S_i S_(k-i), 공간 Σ S_k |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[5, 12]` | `4` |
| `[2, 11]` | `3` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Find the fewest copies of N needed to express number using concatenation and arithmetic.

Parentheses, arithmetic operations, and concatenation are allowed; division discards its remainder. Return −1 if more than eight copies are needed.

`1≤N≤9; 1≤number≤32,000; maximum N count=8`

### Method and correctness

Build a set of values obtainable with each count of N, from one to eight. Include concatenation and split every final binary operation into two smaller expressions. Keep negative and zero intermediate values because later operations may need them, excluding division by zero. Stop at the first count containing the target.

Main complexity: Sum of pairwise result-set products over splits; space is the sum of cached result-set sizes.

### Alternative and trade-offs

Recursively generate and cache values using exactly k copies of N. Division truncates toward zero even for negative values. Both operand orders and concatenation are included.

Code: [alternative.py](alternative.py). Scope: alternative implementation.

Complexity: with result-set sizes S_k: Σ S_i S_(k-i), space Σ S_k.

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: N으로 표현](https://school.programmers.co.kr/learn/courses/30/lessons/42895) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 13개 입력에서 26회 검사를 통과했습니다.

Passed 26 implementation checks across 13 official, boundary and fixed-seed differential inputs.
