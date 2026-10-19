# 징검다리

Level 4 · `43236` · Python3 · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/43236)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py)

## 문제와 조건

정해진 수의 바위를 제거해 남은 인접 지점 사이 최소 거리를 최대화합니다. 출발점과 도착점은 제거하지 않습니다.

입력 범위와 상수는 다음과 같습니다. 기호는 코드의 매개변수에 맞췄습니다.

`1≤distance≤10^9; 1≤rocks≤50000; 1≤removed≤len(rocks); fixed start=0 and end=distance.`

## 풀이를 따라가기

최소 거리를 x로 가정하고 앞에서부터 너무 가까운 바위를 제거합니다. 필요한 최소 제거 수가 허용량 이하면 가능합니다. x가 커질수록 조건이 어려워지므로 이진 탐색합니다.

너무 가까운 두 지점에서는 앞에 남긴 지점을 유지하고 뒤의 지점을 제거해도 이후 선택을 불리하게 만들지 않습니다. 마지막 도착점 간격이 짧을 때 세는 제거는 도착점 대신 직전 바위를 없앤 것과 같은 개수입니다.

## 다른 방법과 비교

대안은 남길 바위 조합을 전부 만들고 실제 최소 간격을 비교합니다. 가능한 조합이 50만 이하인 경우만 허용해 이진 탐색의 판정과 답을 검산합니다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O(R log R + R log distance)` | `O(R)` |
| 대안 풀이 | `O(comb(R,removed) · R)` | `O(R)` |

R은 바위 수입니다. 정렬한 뒤, 후보 간격마다 필요한 제거 수를 셉니다.

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었습니다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교합니다. 실행 기록은 [validation.json](validation.json)에 있습니다. 원본 제출 파일은 [submitted_original.py](submitted_original.py)에 그대로 보관했습니다.

```bash
python test_solution.py
```

## English

### Problem and constraints

Remove the allowed number of rocks to maximize the minimum remaining gap, keeping the start and destination fixed.

Input limits and constants, using the parameter names in the code:

`1≤distance≤10^9; 1≤rocks≤50000; 1≤removed≤len(rocks); fixed start=0 and end=distance.`

### Following the solution

For a candidate gap x, greedily discard rocks too close to the last retained point. Feasibility is monotone as x increases, enabling binary search.

Keeping the earlier point of a too-close pair cannot worsen future spacing. If the last destination gap is short, the counted removal corresponds to deleting the previous retained rock, not the destination.

### Alternative and comparison

The alternative enumerates retained subsets and compares actual gaps, restricted to at most 500000 combinations as an independent reference.

R is the rock count; after sorting, each candidate gap is checked by counting necessary removals.

The primary solution takes `O(R log R + R log distance)` time and `O(R)` additional space. The alternative takes `O(comb(R,removed) · R)` time. Its additional space is `O(R)`.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.py](submitted_original.py).

## 출처 / Source

- [Programmers — 징검다리](https://school.programmers.co.kr/learn/courses/30/lessons/43236): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.
