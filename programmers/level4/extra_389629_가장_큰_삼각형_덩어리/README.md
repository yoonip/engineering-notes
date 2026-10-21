# 가장 큰 삼각형 덩어리

[Level 4 목록 / Level 4 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

Level 4 · `389629` · Python3 · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/389629)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py)

## 문제와 조건

정사각형을 나누는 대각선마다 삼각형 두 개가 생깁니다. 같은 정사각형의 두 삼각형을 함께 쓰지 않으면서, 바깥 변으로 이어지는 가장 큰 덩어리의 삼각형 수를 구합니다.

입력 범위와 상수는 다음과 같습니다. 기호는 코드의 매개변수에 맞췄습니다.

`1≤N,M≤200000; 1≤N·M≤200000; grid∈{-1,1}: diagonal \ or /.`

## 풀이를 따라가기

삼각형 하나가 다른 칸과 맞닿는 바깥 변은 두 개뿐입니다. 연결 그래프의 각 정점 차수가 2 이하이므로 연결 요소는 길 또는 고리입니다. 순서대로 펼친 뒤 같은 정사각형이 다시 나타나면 왼쪽 경계를 옮깁니다.

연결된 선택은 길·고리 위의 연속 구간입니다. 각 정사각형 번호가 한 번만 있는 가장 긴 구간을 슬라이딩 윈도로 찾으면 조건과 크기를 함께 만족합니다. 고리는 두 번 이어 붙이되 원래 길이보다 길게 고르지 않습니다.

## 다른 방법과 비교

대안은 정사각형마다 위쪽·아래쪽 삼각형·미선택의 세 경우를 고르고 실제 연결 여부를 검사합니다. 6칸 이하에서 그래프를 펼치는 논리를 독립적으로 확인합니다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O(N·M)` | `O(N·M)` |
| 대안 풀이 | `O(3^(N·M) · N · M)` | `O(N·M)` |

N·M은 정사각형 수입니다. 각 칸에 삼각형이 두 개씩 있습니다.

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었습니다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교합니다. 실행 기록은 [validation.json](validation.json)에 있습니다. 원본 제출 파일은 [submitted_original.py](submitted_original.py)에 그대로 보관했습니다.

```bash
python test_solution.py
```

## English

### Problem and constraints

Each diagonal creates two triangles. Find the largest externally connected selection containing at most one triangle from each square.

Input limits and constants, using the parameter names in the code:

`1≤N,M≤200000; 1≤N·M≤200000; grid∈{-1,1}: diagonal \ or /.`

### Following the solution

Every triangle has at most two external neighbors, so components are paths or cycles. Traverse them in order and slide the left boundary whenever a square identifier repeats.

Connected selections are contiguous intervals of those components. A longest interval with unique square identifiers is therefore sufficient. Duplicate a cycle to cover wraparound intervals and cap their length at the component size.

### Alternative and comparison

The alternative selects upper, lower or neither triangle per square and checks connectivity explicitly. Its three-way exhaustive search is restricted to six squares.

N·M is the square count; each square has two triangles.

The primary solution takes `O(N·M)` time and `O(N·M)` additional space. The alternative takes `O(3^(N·M) · N · M)` time. Its additional space is `O(N·M)`.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.py](submitted_original.py).

## 출처 / Source

- [Programmers — 가장 큰 삼각형 덩어리](https://school.programmers.co.kr/learn/courses/30/lessons/389629): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.
