# 튜브의 소개팅

Level 4 · `1839` · C++ · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/1839)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py) · [C++ 제출 코드](solution.cpp)

## 문제와 조건

대화 시간 합이 s 이하인 경로 중 이동 횟수를 먼저 최소화하고, 같은 횟수이면 대화 시간 합도 최소화한다. 가장 적은 대화 시간만 찾는 문제와 다르다.

입력 범위와 상수는 다음과 같다. 기호는 코드의 매개변수에 맞췄다.

`2≤m,n≤50; 1≤s≤2^31−1; cells:−1(wall) or 0..2^31−1; endpoints0; a feasible path exists.`

## 풀이를 따라가기

이동 횟수별로 각 칸에 도착하는 최소 대화 시간을 DP로 갱신한다. 끝점이 예산 안에 들어오는 첫 이동 횟수에서 그 최소 대화 시간을 반환한다.

같은 횟수·같은 칸에서는 대화 시간이 작은 경로가 이후에도 불리하지 않다. 대화 시간이 음수가 아니어서 최적 경로에서 순환을 지울 수 있으므로 V−1회 안의 단순 경로를 조사하면 충분하다. 누적 시간은 64비트 정수로 계산한다.

## 다른 방법과 비교

대안은 위치와 소비 시간을 상태로 잡아 (이동 횟수, 대화 시간) 순서의 heap 탐색을 한다. 격자 25칸·예산 1000 이하에서 두 목표의 우선순위를 독립적으로 확인한다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O(V²), V=m·n` | `O(V)` |
| 대안 풀이 | `O(V·s log(V·s)), 작은 정수 s / small integer budget` | 코드의 상태·탐색 구조 참조 |

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교한다. 실행 기록은 [validation.json](validation.json)에 있다. 원본 제출 파일은 [submitted_original.cpp](submitted_original.cpp)에 그대로 보관했다.

```bash
python test_solution.py
```

## English

### Problem and constraints

Among paths with conversation time at most s, minimize moves first and conversation time second. Minimizing conversation time alone is a different objective.

Input limits and constants, using the parameter names in the code:

`2≤m,n≤50; 1≤s≤2^31−1; cells:−1(wall) or 0..2^31−1; endpoints0; a feasible path exists.`

### Following the solution

For each move count, keep minimum conversation time at every cell. Return the destination cost at the first feasible move count.

At identical cells and move counts, lower time dominates. Nonnegative times let an optimal path discard cycles, so a simple path of at most V−1 moves suffices. Accumulated times use 64-bit integers.

### Alternative and comparison

The alternative searches position/time states with a heap ordered by moves then conversation time. At most twenty-five cells and budget 1000 independently check this lexicographic objective.

The primary solution takes `O(V²), V=m·n` time and `O(V)` additional space. The alternative takes `O(V·s log(V·s)), 작은 정수 s / small integer budget` time. Its code shows the states and storage it uses.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.cpp](submitted_original.cpp).

## 출처 / Source

- [Programmers — 튜브의 소개팅](https://school.programmers.co.kr/learn/courses/30/lessons/1839): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.

[Python 비교 원본 / Stored Python comparison source](submitted_original.py)
