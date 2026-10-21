# 쿠키 구입

[Level 4 목록 / Level 4 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

Level 4 · `49995` · Python3 · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/49995)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py)

## 문제와 조건

붙어 있는 두 연속 구간의 합을 같게 만들고, 한쪽이 받는 쿠키 수를 최대화합니다. 떨어진 구간을 고르면 안 됩니다.

입력 범위와 상수는 다음과 같습니다. 기호는 코드의 매개변수에 맞췄습니다.

`1≤len(cookie)≤2000; cookie values:1..500; two nonempty adjacent intervals.`

## 풀이를 따라가기

두 구간의 경계를 고정하고 양쪽으로 늘립니다. 합이 작은 쪽만 확장하면 됩니다. 모든 값이 양수라 큰 쪽만 늘려서는 현재 차이가 줄어들지 않습니다.

어떤 같은 합 구간도 그 경계에서 작은 쪽을 늘리는 과정에 포함됩니다. 각 포인터는 경계 하나당 최대 n번 움직이므로 전체는 제곱 시간입니다.

## 다른 방법과 비교

대안은 prefix sum으로 왼쪽 구간 합을 구하고, 같은 오른쪽 합을 만드는 끝점을 이진 탐색합니다. 별도 탐색 구조로 대조할 수 있지만 로그 인자와 누적합 배열이 추가됩니다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O(n²)` | `O(1)` |
| 대안 풀이 | `O(n² log n), O(n) 공간 / space` | `O(n)` |

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었습니다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교합니다. 실행 기록은 [validation.json](validation.json)에 있습니다. 원본 제출 파일은 [submitted_original.py](submitted_original.py)에 그대로 보관했습니다.

```bash
python test_solution.py
```

## English

### Problem and constraints

Maximize the equal sum of two nonempty adjacent intervals; separated intervals are invalid.

Input limits and constants, using the parameter names in the code:

`1≤len(cookie)≤2000; cookie values:1..500; two nonempty adjacent intervals.`

### Following the solution

Fix their boundary and expand the side with the smaller sum. With positive entries, enlarging only the larger side cannot repair the imbalance.

Every feasible equal-sum pair can be reached by these expansions. Each pointer moves at most n times per boundary, giving quadratic total work.

### Alternative and comparison

The alternative uses prefix sums and binary searches for the right endpoint matching each left interval. It checks the condition differently but adds a logarithmic factor and prefix-array storage.

The primary solution takes `O(n²)` time and `O(1)` additional space. The alternative takes `O(n² log n), O(n) space` time. Its additional space is `O(n)`.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.py](submitted_original.py).

## 출처 / Source

- [Programmers — 쿠키 구입](https://school.programmers.co.kr/learn/courses/30/lessons/49995): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.
