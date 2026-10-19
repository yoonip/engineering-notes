# 행렬과 연산

Level 4 · `118670` · Python3 · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/118670)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py)

## 문제와 조건

ShiftRow는 마지막 행을 맨 위로 옮기고, Rotate는 가장 바깥 테두리만 시계 방향으로 한 칸 옮긴다.

입력 범위와 상수는 다음과 같다. 기호는 코드의 매개변수에 맞췄다.

`2≤rows,cols≤50000; rows·cols≤100000; values:1..1000000; 1≤operations≤100000; ShiftRow or Rotate.`

## 풀이를 따라가기

왼쪽 열·오른쪽 열·행별 가운데 부분을 덱으로 나눈다. 행 이동은 세 덱을 한 칸 회전하면 끝난다. 테두리 회전은 위·아래 가운데 덱과 양쪽 열 사이에서 네 번 전달하면 된다.

각 덱의 순서가 현재 행렬의 해당 구역을 나타낸다는 불변식을 유지한다. 열이 두 개인 경우에도 비어 있는 가운데 덱에 넣은 직후 빼므로 같은 네 단계가 성립한다.

## 다른 방법과 비교

대안은 행렬 전체를 보관하고 테두리 좌표를 순서대로 나열해 값을 직접 옮긴다. 동작을 눈으로 확인하기 쉽지만 매 연산에 테두리 길이만큼 시간이 든다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O(rows·cols + operations)` | `O(rows·cols)` |
| 대안 풀이 | `O(operations · (rows+cols) + rows·cols)` | `O(rows·cols)` |

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교한다. 실행 기록은 [validation.json](validation.json)에 있다. 원본 제출 파일은 [submitted_original.py](submitted_original.py)에 그대로 보관했다.

```bash
python test_solution.py
```

## English

### Problem and constraints

ShiftRow moves the bottom row to the top; Rotate moves only the outer perimeter clockwise by one position.

Input limits and constants, using the parameter names in the code:

`2≤rows,cols≤50000; rows·cols≤100000; values:1..1000000; 1≤operations≤100000; ShiftRow or Rotate.`

### Following the solution

Split the matrix into left/right column deques and a deque of middle-row deques. Three deque rotations implement ShiftRow; four endpoint transfers implement Rotate.

Deque order always represents its current matrix region. With two columns, inserting into an empty middle deque immediately before removing from it preserves the same four-step update.

### Alternative and comparison

The alternative enumerates perimeter coordinates and physically moves entries. It makes the operation visible but pays perimeter-length work per rotation.

The primary solution takes `O(rows·cols + operations)` time and `O(rows·cols)` additional space. The alternative takes `O(operations · (rows+cols) + rows·cols)` time. Its additional space is `O(rows·cols)`.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.py](submitted_original.py).

## 출처 / Source

- [Programmers — 행렬과 연산](https://school.programmers.co.kr/learn/courses/30/lessons/118670): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.
