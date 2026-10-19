# 1,2,3 떨어트리기

Level 4 · `150364` · Python3 · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/150364)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py)

## 문제와 조건

트리에서 공이 내려갈 자식은 작은 번호부터 순환한다. 떨어뜨릴 공에 1·2·3을 적어 각 리프의 목표 합을 만들되 공 수를 최소화하고, 같은 길이면 사전순으로 가장 작은 배열을 구한다.

입력 범위와 상수는 다음과 같다. 기호는 코드의 매개변수에 맞췄다.

`1≤len(edges)≤100; root=1; target length=len(edges)+1; leaf targets:0..100; internal targets=0; sum(target)≥1.`

## 풀이를 따라가기

공에 적힌 값은 도착할 리프에 영향을 주지 않는다. 따라서 먼저 도착 순서만 시뮬레이션한다. 리프에 공이 c개 도착했으면 가능한 합은 c부터 3c까지다. 모든 목표가 이 범위에 들어오는 첫 시점이 최소 길이다.

이후 앞에서부터 값을 정한다. 남은 공을 전부 3으로 써도 목표에 못 미치지 않도록 필요한 최솟값 max(1, 남은 합−3×뒤의 공 수)를 고른다. 가장 이른 자리를 작게 하면서 뒤쪽의 가능성을 보존하므로 사전순 최소다.

## 다른 방법과 비교

대안은 길이를 늘리며 1·2·3의 모든 값 배열을 실제 합계와 비교한다. 목표 합 10 이하에서 최소 길이와 사전순을 함께 확인한다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O(B·H + n log n), B=공 수/balls, H=높이/height` | `O(B+n)` |
| 대안 풀이 | `O(3^B · B + B·H)` | `O(n+B)` |

n은 정점 수, B는 실제로 떨어뜨린 공 수, H는 트리 높이다.

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교한다. 실행 기록은 [validation.json](validation.json)에 있다. 원본 제출 파일은 [submitted_original.py](submitted_original.py)에 그대로 보관했다.

```bash
python test_solution.py
```

## English

### Problem and constraints

Children are chosen cyclically in increasing order. Label dropped balls 1, 2 or 3 to achieve leaf targets, minimizing ball count and then lexicographic order.

Input limits and constants, using the parameter names in the code:

`1≤len(edges)≤100; root=1; target length=len(edges)+1; leaf targets:0..100; internal targets=0; sum(target)≥1.`

### Following the solution

Labels do not affect destinations. Simulate leaf arrivals first: c balls can form every integer sum from c to 3c. The first prefix satisfying every target is the minimum feasible length.

Assign labels left to right using max(1, remaining target minus three times the later ball count). This keeps the suffix feasible while minimizing the earliest undecided entry.

### Alternative and comparison

The alternative enumerates label arrays in length and lexicographic order. A target-sum cap of ten keeps this independent exhaustive reference finite.

n is the vertex count, B the number of dropped balls and H the tree height.

The primary solution takes `O(B·H + n log n), B=balls, H=height` time and `O(B+n)` additional space. The alternative takes `O(3^B · B + B·H)` time. Its additional space is `O(n+B)`.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.py](submitted_original.py).

## 출처 / Source

- [Programmers — 1,2,3 떨어트리기](https://school.programmers.co.kr/learn/courses/30/lessons/150364): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.
