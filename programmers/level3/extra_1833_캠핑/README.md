# 캠핑

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

Level 3 · [1833 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/1833)

## 문제와 조건

두 쐐기를 대각 꼭짓점으로 고른 양의 면적 직사각형 안에 다른 쐐기가 없는 쌍의 수를 구합니다. 경계의 쐐기는 허용합니다.

`2≤n≤5,000; 0≤x,y≤2^31−1; points distinct`

## 풀이를 따라가기

1. 점을 x순으로 정렬합니다. 왼쪽 꼭짓점 하나를 고정하고 오른쪽으로 훑으며, 지금까지 안쪽 x구간에서 본 y 중 기준보다 바로 위·아래 값을 경계로 유지합니다.
2. 오른쪽 꼭짓점의 y가 그 경계를 넘으면 내부에 쐐기가 생깁니다. 같은 x의 점들은 모두 후보로 검사한 후 경계를 갱신해 직사각형 경계의 점을 허용합니다.
3. 예제는 세 쌍만 가능하고 (0,2)-(2,0)은 (1,1)이 안에 있어 제외됩니다. 시간 O(N²+N log N), 공간 O(N).

## 왜 이 방법으로 풀 수 있나

점을 x순으로 정렬합니다. 왼쪽 꼭짓점 하나를 고정하고 오른쪽으로 훑으며, 지금까지 안쪽 x구간에서 본 y 중 기준보다 바로 위·아래 값을 경계로 유지합니다.

시간·공간: 시간 O(N²+N log N), 공간 O(N).

## 다른 방법과 비교

두 쐐기를 대각 꼭짓점으로 정한 뒤 다른 모든 쐐기가 직사각형의 엄격한 내부에 있는지 확인합니다. 경계에 있는 쐐기는 허용합니다.

| 항목 | 기본 풀이 | 모든 쐐기 내부 검사 |
|---|---|---|
| 코드 | [solution.cpp](solution.cpp) | [alternative.py](alternative.py) |
| 비용 | 시간 O(N²+N log N), 공간 O(N). | O(N³), 공간 O(1), 작은 입력 비교용 |
| 용도 | 기본 제출 구현 | 작은 입력 비교·검증용 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[4, [[0, 0], [1, 1], [0, 2], [2, 0]]]` | `3` |

Python 대안은 examples.json과 별도 경계·무작위 입력으로 로컬 검증합니다. C++ 제출본의 실행 결과는 전체 검증 기록에서 구분합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.cpp)

## English

### Task and constraints

Count peg pairs forming positive-area axis-aligned rectangles with no other peg strictly inside; boundary pegs are allowed.

`2≤n≤5,000; 0≤x,y≤2^31−1; points distinct`

### Method and correctness

Sort pegs by x. For each left corner, scan later x groups while maintaining the nearest interior y above and below its y. A right corner outside those y bounds would enclose an earlier peg. Test a whole equal-x group before updating bounds so boundary pegs are allowed. Pairs with equal x or y have zero area and are excluded.

Main complexity: O(N²+N log N) time, O(N) space.

### Alternative and trade-offs

Choose each pair of pegs as diagonal corners and test every other peg for strict interior membership. Pegs on the boundary are allowed.

Code: [alternative.py](alternative.py). Scope: tiny-input oracle; not for maximum-size submissions.

Complexity: O(N³), space O(1), small-input checking.

### Verification

The Python alternative is checked with examples.json and separate edge/random cases; C++ execution is recorded separately in the repository validation report.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 캠핑](https://school.programmers.co.kr/learn/courses/30/lessons/1833) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 31개 입력에서 31회 검사를 통과했습니다.

Passed 31 implementation checks across 31 official, boundary and fixed-seed differential inputs.

[Python 비교 원본 / Stored Python comparison source](submitted_original.py)
