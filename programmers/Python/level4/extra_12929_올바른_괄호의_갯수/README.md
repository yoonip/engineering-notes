# 올바른 괄호의 갯수

[Level 4 목록 / Level 4 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

Level 4 · `12929` · Python3 · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12929)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py)

## 문제와 조건

괄호 n쌍으로 만들 수 있는 올바른 괄호 문자열 수를 구합니다. 어떤 접두사에서도 닫는 괄호가 더 많아서는 안 됩니다.

입력 범위와 상수는 다음과 같습니다. 기호는 코드의 매개변수에 맞췄습니다.

`1≤n≤14; n matching bracket pairs; return the exact integer, without a modulus.`

## 풀이를 따라가기

첫 여는 괄호와 짝이 되는 닫는 괄호를 기준으로 (내부 문자열)+뒤쪽 문자열로 나눕니다. 내부에 i쌍이면 뒤쪽은 n−1−i쌍이므로 두 경우의 수를 곱합니다.

모든 올바른 문자열은 이 분해가 유일합니다. i=0부터 n−1까지 합한 Catalan 점화식과 빈 문자열 한 가지 C[0]=1을 사용합니다.

## 다른 방법과 비교

대안은 반사 원리로 전체 균형 문자열 C(2n,n)에서 잘못된 접두사를 갖는 C(2n,n+1)을 뺍니다. Python 정수 조합을 사용해 부동소수점 나눗셈을 피합니다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O(n²)` | `O(n)` |
| 대안 풀이 | `조합 계산 비용 / binomial arithmetic cost` | `O(n) bits` |

대안은 반사 원리의 이항계수 두 개를 math.comb로 계산합니다. 반환 정수는 O(n)비트이고, 실제 조합 계산 시간은 정수 연산 구현에 달려 있습니다. n≤14에서는 모두 작은 정수 범위입니다.

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었습니다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교합니다. 실행 기록은 [validation.json](validation.json)에 있습니다. 원본 제출 파일은 [submitted_original.py](submitted_original.py)에 그대로 보관했습니다.

```bash
python test_solution.py
```

## English

### Problem and constraints

Count valid strings of n bracket pairs. No prefix may contain more closing than opening brackets.

Input limits and constants, using the parameter names in the code:

`1≤n≤14; n matching bracket pairs; return the exact integer, without a modulus.`

### Following the solution

The closing bracket matching the first opening splits a string into an enclosed valid string and a trailing valid string. With i pairs inside, n−1−i remain outside, so multiply their counts.

This decomposition is unique. Sum over all i and initialize the empty string with C[0]=1, yielding the Catalan recurrence.

### Alternative and comparison

The alternative uses the reflection principle: subtract C(2n,n+1) invalid-prefix strings from C(2n,n) balanced strings. Integer binomial arithmetic avoids floating-point division.

The primary solution takes `O(n²)` time and `O(n)` additional space. The alternative takes `binomial arithmetic cost` time. Its additional space is `O(n) bits`.

The alternative computes two reflection-principle binomial coefficients with math.comb. The returned integers have O(n) bits; exact arithmetic runtime depends on the binomial implementation. All values are small within n≤14.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.py](submitted_original.py).

## 출처 / Source

- [Programmers — 올바른 괄호의 갯수](https://school.programmers.co.kr/learn/courses/30/lessons/12929): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.
