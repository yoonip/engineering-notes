# 도둑질

[Level 4 목록 / Level 4 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

Level 4 · `42897` · Python3 · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/42897)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py)

## 문제와 조건

원형으로 연결된 집에서 인접한 두 집을 함께 선택하지 않고 금액 합을 최대화합니다.

입력 범위와 상수는 다음과 같습니다. 기호는 코드의 매개변수에 맞췄습니다.

`3≤houses≤1000000; 0≤money[i]≤1000; circular adjacency.`

## 풀이를 따라가기

첫 집과 마지막 집을 동시에 고를 수 없으므로 첫 집을 제외한 일자 구간과 마지막 집을 제외한 일자 구간을 각각 계산합니다. 일자 구간은 현재 집을 건너뛰거나 두 칸 전 최적값에 현재 금액을 더합니다.

모든 원형 해는 두 끝 집 중 적어도 하나를 제외하므로 두 경우 중 최댓값이 전체 최적값입니다. 일자 DP는 앞 두 상태만 필요합니다.

## 다른 방법과 비교

대안은 선택 비트마스크와 한 칸 회전한 비트마스크가 겹치는지 검사합니다. 집 22개 이하에서 원형 경계까지 직접 비교하지만 큰 입력에는 쓰지 않습니다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O(n)` | `O(1)` |
| 대안 풀이 | `O(n·2^n)` | `O(1), n≤22` |

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었습니다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교합니다. 실행 기록은 [validation.json](validation.json)에 있습니다. 원본 제출 파일은 [submitted_original.py](submitted_original.py)에 그대로 보관했습니다.

```bash
python test_solution.py
```

## English

### Problem and constraints

Maximize money taken from a cycle of houses without choosing adjacent houses.

Input limits and constants, using the parameter names in the code:

`3≤houses≤1000000; 0≤money[i]≤1000; circular adjacency.`

### Following the solution

Solve two linear ranges: exclude the first house or exclude the last. The linear recurrence skips the current house or adds it to the optimum two positions earlier.

Every valid circular choice omits at least one endpoint, so these cases cover all possibilities. Only two preceding DP states are required.

### Alternative and comparison

The alternative rejects selection masks overlapping their one-position circular rotation. It independently checks circular boundaries for at most twenty-two houses.

The primary solution takes `O(n)` time and `O(1)` additional space. The alternative takes `O(n·2^n)` time. Its additional space is `O(1), n≤22`.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.py](submitted_original.py).

## 출처 / Source

- [Programmers — 도둑질](https://school.programmers.co.kr/learn/courses/30/lessons/42897): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.
