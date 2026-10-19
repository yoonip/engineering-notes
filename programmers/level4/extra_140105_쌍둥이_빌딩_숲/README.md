# 쌍둥이 빌딩 숲

Level 4 · `140105` · Python3 · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/140105)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py)

## 문제와 조건

높이 1부터 n까지 각각 두 채를 놓는다. 같은 높이 사이에 더 높은 빌딩이 없고, 한쪽에서 구분해 보이는 높이가 count개인 배치를 센다.

입력 범위와 상수는 다음과 같다. 기호는 코드의 매개변수에 맞췄다.

`1≤n≤100; 1≤count≤n; two buildings per height; identical heights indistinguishable; modulus 1000000007.`

## 풀이를 따라가기

기존 높이를 모두 1씩 올리고 새 최저 높이 쌍을 붙여 넣는다. 최저 높이 사이에는 더 높은 건물을 넣을 수 없어 두 채가 붙어 있어야 한다. 맨 앞에 넣으면 보이는 수가 하나 늘고, 나머지 2(n−1)곳에서는 가려진다.

따라서 dp[n][c]=dp[n−1][c−1]+2(n−1)dp[n−1][c]다. 마지막으로 넣은 최저 높이 쌍을 제거하면 이전 배치가 유일하게 복원되므로 중복 집계가 없다.

## 다른 방법과 비교

대안은 해당 삽입 위치를 실제 배열로 전부 생성해 보이는 수를 직접 센다. n≤6에서 점화식의 계수와 경계를 확인한다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O(n·count)` | `O(count)` |
| 대안 풀이 | `O(n · (2n−1)!!), 작은 n / small n` | 코드의 상태·탐색 구조 참조 |

n은 높이 종류 수다. (2n−1)!!는 1·3·5·…·(2n−1)을 뜻한다.

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교한다. 실행 기록은 [validation.json](validation.json)에 있다. 원본 제출 파일은 [submitted_original.py](submitted_original.py)에 그대로 보관했다.

```bash
python test_solution.py
```

## English

### Problem and constraints

Place two indistinguishable buildings of each height 1 through n, forbidding taller buildings between equal-height copies. Count arrangements showing exactly count distinct heights from one side.

Input limits and constants, using the parameter names in the code:

`1≤n≤100; 1≤count≤n; two buildings per height; identical heights indistinguishable; modulus 1000000007.`

### Following the solution

Raise existing heights and insert the new minimum pair adjacently. It must stay adjacent because every existing building is taller. The front position adds a visible height; the other 2(n−1) positions do not.

This yields dp[n][c]=dp[n−1][c−1]+2(n−1)dp[n−1][c]. Removing the unique minimum pair recovers exactly one predecessor, so the recurrence does not duplicate arrangements.

### Alternative and comparison

The alternative constructs every insertion arrangement and counts records directly for n≤6, checking the recurrence coefficients and boundaries.

n is the number of height classes; (2n−1)!! means 1·3·5·…·(2n−1).

The primary solution takes `O(n·count)` time and `O(count)` additional space. The alternative takes `O(n · (2n−1)!!), 작은 n / small n` time. Its code shows the states and storage it uses.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.py](submitted_original.py).

## 출처 / Source

- [Programmers — 쌍둥이 빌딩 숲](https://school.programmers.co.kr/learn/courses/30/lessons/140105): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.
