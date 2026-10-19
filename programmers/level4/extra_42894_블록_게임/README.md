# 블록 게임

Level 4 · `42894` · Python3 · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/42894)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py)

## 문제와 조건

검은 칸 두 개를 위에서 떨어뜨려 기존 블록과 꽉 찬 직사각형을 만들면 그 블록을 지울 수 있습니다. 지울 수 있는 블록 수를 최대화합니다.

입력 범위와 상수는 다음과 같습니다. 기호는 코드의 매개변수에 맞췄습니다.

`4≤N≤50; N×N board; 0=empty, block identifiers:1..200; valid stated block shapes.`

## 풀이를 따라가기

블록의 네 칸을 둘러싼 직사각형 넓이가 6인지 확인합니다. 나머지 두 칸이 비어 있고 각 칸 위가 막히지 않았으면 검은 칸을 넣을 수 있습니다. 자기 블록의 윗부분이 막는 경우도 검사합니다.

블록 제거는 다른 블록 위의 장애물을 없앨 뿐 새 장애물을 만들지 않습니다. 지금 가능한 제거를 먼저 수행해도 이후 가능한 제거를 잃지 않으므로 변화가 없을 때까지 반복합니다.

## 다른 방법과 비교

대안은 가능한 모든 제거 순서를 보드 상태로 메모해 최댓값을 직접 탐색합니다. 블록 10개 이하에서 탐욕적인 제거 순서가 답을 잃지 않는지 확인합니다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O(N²+B²·N)` | `O(N²+B)` |
| 대안 풀이 | `제거 상태 수에 지수적 / exponential in removable-block states` | `O(S·N²)` |

N은 보드 한 변의 길이, B는 블록 수입니다.

대안 비용에서 S는 서로 다른 보드 상태 수입니다. 각 상태의 판 N²칸을 캐시하므로 저장 공간은 O(S·N²)입니다.

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었습니다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교합니다. 실행 기록은 [validation.json](validation.json)에 있습니다. 원본 제출 파일은 [submitted_original.py](submitted_original.py)에 그대로 보관했습니다.

```bash
python test_solution.py
```

## English

### Problem and constraints

Drop two black cells from above to complete a solid rectangle with an existing four-cell block, then remove it. Maximize removals.

Input limits and constants, using the parameter names in the code:

`4≤N≤50; N×N board; 0=empty, block identifiers:1..200; valid stated block shapes.`

### Following the solution

The block bounding rectangle must have area six. Its other two cells must be empty with unobstructed vertical access, including obstruction by the same block.

Removing a block only clears obstacles and never creates one. Taking any currently feasible removal cannot destroy future removals, so repeat until no change remains.

### Alternative and comparison

The alternative memoizes board states and explores every feasible removal order for at most ten blocks, independently checking the greedy ordering argument.

N is the board side length and B is the block count.

The primary solution takes `O(N²+B²·N)` time and `O(N²+B)` additional space. The alternative takes `exponential in removable-block states` time. Its additional space is `O(S·N²)`.

For the alternative, S counts distinct board states. Memoizing an N²-cell board per state uses O(S·N²) storage.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.py](submitted_original.py).

## 출처 / Source

- [Programmers — 블록 게임](https://school.programmers.co.kr/learn/courses/30/lessons/42894): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.
