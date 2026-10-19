# 지형 편집

Level 4 · `12984` · Python3 · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12984)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py)

## 문제와 조건

모든 칸 높이를 같게 만들 때 블록 추가는 P, 제거는 Q의 비용이 듭니다. 가능한 최소 비용을 구합니다.

입력 범위와 상수는 다음과 같습니다. 기호는 코드의 매개변수에 맞췄습니다.

`1≤N≤300; N×N land; heights:0..10^9; insertion/deletion costs P,Q:1..100.`

## 풀이를 따라가기

목표 높이를 1 올릴 때 낮은 칸 수×P만큼 비용이 늘고 높은 칸 수×Q만큼 줄어듭니다. 정렬된 높이를 지날 때만 이 차이가 바뀝니다.

전체 칸 수가 V이면 정렬 순위 V·Q/(P+Q)를 넘어서는 지점에서 기울기가 음수에서 양수로 바뀝니다. 그 순위의 실제 높이를 골라 비용을 한 번 계산합니다. 경계에서 기울기 0이면 여러 높이가 같은 최적값입니다.

## 다른 방법과 비교

대안은 이산 볼록 함수의 cost(h)와 cost(h+1)를 비교해 높이를 이진 탐색합니다. 정렬 대신 높이 범위의 로그만큼 전체 칸을 다시 계산합니다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O(V log V), V=N²` | `O(V)` |
| 대안 풀이 | `O(V log H), H=높이 범위/height range` | `O(V)` |

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었습니다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교합니다. 실행 기록은 [validation.json](validation.json)에 있습니다. 원본 제출 파일은 [submitted_original.py](submitted_original.py)에 그대로 보관했습니다.

```bash
python test_solution.py
```

## English

### Problem and constraints

Equalize all heights with insertion cost P and deletion cost Q per block, minimizing total cost.

Input limits and constants, using the parameter names in the code:

`1≤N≤300; N×N land; heights:0..10^9; insertion/deletion costs P,Q:1..100.`

### Following the solution

Increasing the target by one adds P per lower cell and saves Q per higher cell. The discrete slope changes only when passing an observed height.

For V cells, the slope crosses zero at rank V·Q/(P+Q) in sorted heights. Evaluate that observed height once. A zero-slope interval can contain multiple equally optimal heights.

### Alternative and comparison

The alternative binary-searches the discrete convex cost by comparing cost(h) with cost(h+1). It avoids sorting but rescans every cell per height-range search step.

The primary solution takes `O(V log V), V=N²` time and `O(V)` additional space. The alternative takes `O(V log H), H=height range` time. Its additional space is `O(V)`.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.py](submitted_original.py).

## 출처 / Source

- [Programmers — 지형 편집](https://school.programmers.co.kr/learn/courses/30/lessons/12984): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.
