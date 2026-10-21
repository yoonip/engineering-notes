# 격자 뒤집기 미로

[Level 4 목록 / Level 4 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

Level 4 · `389630` · Python3 · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/389630)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py)

## 문제와 조건

행이나 열을 뒤집어 각 칸의 앞·뒷면을 바꾼 뒤, 왼쪽 위에서 오른쪽 아래까지 재방문 없이 이동합니다. 방문한 숫자의 합에서 뒤집기 비용을 뺀 최댓값을 구합니다.

입력 범위와 상수는 다음과 같습니다. 기호는 코드의 매개변수에 맞췄습니다.

`1≤n≤14, 2≤m≤100; visible/hidden: n×m, 1..100; 0≤k≤100.`

## 풀이를 따라가기

행 뒤집기를 비트마스크로 하나씩 고정합니다. 그러면 각 열은 그대로 둘지 한 번 뒤집을지만 비교하면 됩니다. 같은 행·열을 두 번 뒤집으면 원래 상태로 돌아가므로 비용을 더 내며 두 번 뒤집을 이유가 없습니다.

한 변이 홀수이면 모든 칸을 지나는 지그재그 경로가 있습니다. 양쪽 길이가 짝수이면 시작·끝이 같은 체스판 색이므로 반대 색 한 칸을 빼야 하며, 그중 어느 한 칸을 뺀 경로도 만들 수 있습니다. 점수가 양수이므로 더 많은 칸을 뺄 이득은 없습니다. 열별 최댓값에 가장 작은 제외 손실 하나를 반영합니다.

## 다른 방법과 비교

대안은 모든 행·열 뒤집기와 실제 단순 경로를 직접 열거합니다. 경로 구조에 관한 결론을 사용하지 않아 작은 격자의 독립 검산에 좋지만, 코드에서 9칸 이하로 제한합니다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O(2^n · n · m)` | `O(n)` |
| 대안 풀이 | `O(2^(n+m) · 단순 경로 수 / number of simple paths)` | `O(n·m)` |

n은 행 수, m은 열 수입니다.

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었습니다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교합니다. 실행 기록은 [validation.json](validation.json)에 있습니다. 원본 제출 파일은 [submitted_original.py](submitted_original.py)에 그대로 보관했습니다.

```bash
python test_solution.py
```

## English

### Problem and constraints

Flip rows or columns, then take a nonrepeating path from the top-left to bottom-right. Maximize visited values minus flip costs.

Input limits and constants, using the parameter names in the code:

`1≤n≤14, 2≤m≤100; visible/hidden: n×m, 1..100; 0≤k≤100.`

### Following the solution

Fix row flips with a bitmask. Each column can then independently choose its two orientations. Repeating a flip only restores the same state at no lower cost.

An odd dimension admits a spanning snake path. For even-by-even grids, endpoint colors require omitting one opposite-color cell, and a spanning path exists after omitting any such cell. Positive values make additional omissions unhelpful. Combine independent column optima with the best single-cell omission adjustment.

### Alternative and comparison

The alternative enumerates flips and actual simple paths, independently checking the path argument on at most nine cells. Its exponential path search is not intended for the full bounds.

n and m denote row and column counts.

The primary solution takes `O(2^n · n · m)` time and `O(n)` additional space. The alternative takes `O(2^(n+m) · number of simple paths)` time. Its additional space is `O(n·m)`.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.py](submitted_original.py).

## 출처 / Source

- [Programmers — 격자 뒤집기 미로](https://school.programmers.co.kr/learn/courses/30/lessons/389630): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.
