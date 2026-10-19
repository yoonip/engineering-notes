# 호텔 방 배정

Level 4 · `64063` · Python3 · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/64063)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py)

## 문제와 조건

원하는 방이 비어 있으면 배정하고, 차 있으면 그보다 큰 빈 방 중 가장 작은 방을 배정합니다. 요청 순서를 바꾸면 안 됩니다.

입력 범위와 상수는 다음과 같습니다. 기호는 코드의 매개변수에 맞췄습니다.

`1≤k≤10^12; 1≤requests≤200000; requested rooms:1..k; every request can be assigned.`

## 풀이를 따라가기

이미 사용한 방 번호만 딕셔너리에 넣고 다음 검색 후보로 연결합니다. 후보를 따라 빈 방을 찾은 뒤 지나온 방들을 모두 그 다음 후보에 연결합니다.

건너뛰는 구간에는 배정된 방만 들어 있다는 불변식을 유지합니다. 경로 압축은 나중 요청이 같은 긴 구간을 다시 한 칸씩 보지 않게 합니다. k 크기의 배열은 필요하지 않습니다.

## 다른 방법과 비교

대안은 집합을 보며 한 번호씩 증가시킵니다. 원리는 단순하지만 같은 방 요청이 몰리면 이미 찬 구간을 반복해서 보므로 제곱 시간이 됩니다. 요청 5000개 이하 비교용입니다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O(Q log Q) 경로 압축 상계 / path-compression bound` | `O(Q)` |
| 대안 풀이 | `O(Q²)` | `O(Q)` |

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었습니다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교합니다. 실행 기록은 [validation.json](validation.json)에 있습니다. 원본 제출 파일은 [submitted_original.py](submitted_original.py)에 그대로 보관했습니다.

```bash
python test_solution.py
```

## English

### Problem and constraints

Assign a requested room if free; otherwise assign the smallest free larger room. Preserve request order.

Input limits and constants, using the parameter names in the code:

`1≤k≤10^12; 1≤requests≤200000; requested rooms:1..k; every request can be assigned.`

### Following the solution

Store only occupied identifiers and successor search candidates. After finding a free room, compress every traversed identifier toward the next candidate.

Only already assigned rooms are skipped, preserving the smallest-free-room invariant. Compression prevents repeated scans of the same occupied run without allocating an array of size k.

### Alternative and comparison

The alternative increments room numbers against an occupied set. Repeated requests rescan runs and can take quadratic time, so its comparison implementation caps requests at 5000.

The primary solution takes `O(Q log Q) path-compression bound` time and `O(Q)` additional space. The alternative takes `O(Q²)` time. Its additional space is `O(Q)`.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.py](submitted_original.py).

## 출처 / Source

- [Programmers — 호텔 방 배정](https://school.programmers.co.kr/learn/courses/30/lessons/64063): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.
