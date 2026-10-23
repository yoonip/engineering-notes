# 트리 트리오 중간값

[Level 4 목록 / Level 4 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

Level 4 · `68937` · Python3 · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/68937)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py)

## 문제와 조건

서로 다른 세 정점 사이의 세 거리에서 중간값을 택하고, 그 값을 최대화합니다.

입력 범위와 상수는 다음과 같습니다. 기호는 코드의 매개변수에 맞췄습니다.

`3≤n≤250000; exactly n−1 undirected edges; valid tree; vertices numbered 1..n.`

## 풀이를 따라가기

BFS로 지름 양 끝점을 구합니다. 한 끝점에서 지름 거리의 정점이 둘 이상이면 같은 끝점과 그 두 정점으로 거리 두 개를 지름으로 만들 수 있습니다.

양쪽 끝점 모두 지름 거리 정점이 하나뿐이면 지름을 두 번 포함하는 세 점은 없습니다. 대신 지름 경로 끝점의 바로 옆 정점을 고르면 중간값 지름−1을 만듭니다. 어떤 거리도 지름을 넘지 못하므로 두 경우가 상한과 일치합니다.

## 다른 방법과 비교

대안은 모든 정점 쌍 거리를 BFS로 구한 뒤 세 정점 조합을 전부 확인합니다. 정점 60개 이하에서 끝점 판정을 비교합니다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O(n)` | `O(n)` |
| 대안 풀이 | `O(n³+n²)` | `O(n²)` |

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었습니다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교합니다. 실행 기록은 [validation.json](validation.json)에 있습니다. 원본 제출 파일은 [submitted_original.py](submitted_original.py)에 그대로 보관했습니다.

```bash
python test_solution.py
```

## English

### Problem and constraints

For three distinct vertices, take the median of their three pairwise distances and maximize it.

Input limits and constants, using the parameter names in the code:

`3≤n≤250000; exactly n−1 undirected edges; valid tree; vertices numbered 1..n.`

### Following the solution

Find diameter endpoints with BFS. If an endpoint has two vertices at diameter distance, two of the triple distances attain the diameter.

Otherwise both endpoint checks have a unique opposite extremity, preventing two diameter distances in one triple. A neighbor of an endpoint along the diameter gives median diameter−1. No distance exceeds the diameter, so these constructions match the respective bounds.

### Alternative and comparison

The alternative computes every pair distance and enumerates triples for at most sixty vertices, independently checking the endpoint criterion.

The primary solution takes `O(n)` time and `O(n)` additional space. The alternative takes `O(n³+n²)` time. Its additional space is `O(n²)`.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.py](submitted_original.py).

## 출처 / Source

- [Programmers — 트리 트리오 중간값](https://school.programmers.co.kr/learn/courses/30/lessons/68937): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.
