# 경사로의 개수

Level 4 · `214290` · Python3 · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/214290)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py)

## 문제와 조건

높이 차 수열 d를 k번 반복해서 따르는 모든 이동 경로를 셉니다. 상하좌우 이동이며 같은 칸을 다시 방문할 수 있습니다.

입력 범위와 상수는 다음과 같습니다. 기호는 코드의 매개변수에 맞췄습니다.

`3≤n,m≤8; heights:0..1000; 1≤len(d)≤100; d:-100..100; 1≤k≤10^9; modulus 1000000007.`

## 풀이를 따라가기

d 한 번을 처리해 출발 칸별·도착 칸별 경로 수를 행렬에 저장합니다. 두 구간을 잇는 경우의 수는 중간 칸을 정한 뒤 앞·뒤 경우의 수를 곱해 더하므로 행렬 곱입니다.

같은 전이가 k번 반복되므로 제곱을 재사용하는 빠른 거듭제곱을 씁니다. 모든 시작점을 허용하는 초기 벡터에서 최종 칸별 수를 더하고 매 계산에 나머지를 적용합니다.

## 다른 방법과 비교

대안은 k번 모두 한 걸음씩 진행하는 격자 DP입니다. 반복 구조를 압축하지 않아 이해하기 쉽고 작은 k에서는 더 간단하지만, 길이×k가 5000 이하일 때만 실행합니다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O(len(d)·V² + V³ log k), V=n·m` | `O(V²)` |
| 대안 풀이 | `O(k · len(d) · V)` | `O(V)` |

V는 전체 칸 수이고 k는 수열 d의 반복 횟수입니다.

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었습니다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교합니다. 실행 기록은 [validation.json](validation.json)에 있습니다. 원본 제출 파일은 [submitted_original.py](submitted_original.py)에 그대로 보관했습니다.

```bash
python test_solution.py
```

## English

### Problem and constraints

Count four-neighbor walks following height-difference sequence d repeated k times; revisiting cells is permitted.

Input limits and constants, using the parameter names in the code:

`3≤n,m≤8; heights:0..1000; 1≤len(d)≤100; d:-100..100; 1≤k≤10^9; modulus 1000000007.`

### Following the solution

Compute a start-to-end transition matrix for one copy of d. Joining two walks sums products over the intermediate cell, which is exactly matrix multiplication.

Binary exponentiation reuses squared transitions for large k. Start with one way at every cell and sum final entries, reducing modulo 1000000007 throughout.

### Alternative and comparison

The alternative advances the ordinary grid DP for every step. It is a simpler independent reference for small repetition counts, capped at 5000 total steps.

V is the cell count and k is the repetition count of d.

The primary solution takes `O(len(d)·V² + V³ log k), V=n·m` time and `O(V²)` additional space. The alternative takes `O(k · len(d) · V)` time. Its additional space is `O(V)`.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.py](submitted_original.py).

## 출처 / Source

- [Programmers — 경사로의 개수](https://school.programmers.co.kr/learn/courses/30/lessons/214290): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.
