# 무지의 먹방 라이브

[Level 4 목록 / Level 4 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

Level 4 · `42891` · Python3 · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/42891)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py)

## 문제와 조건

음식을 번호순으로 한 초씩 먹다가 k초 후 다시 먹을 음식 번호를 구합니다. 다 먹은 음식은 건너뜁니다.

입력 범위와 상수는 다음과 같습니다. 기호는 코드의 매개변수에 맞췄습니다.

`효율성/efficiency: 1≤N≤200000; 1≤food_times[i]≤10^8; 1≤k≤2·10^13; return −1 if all consumed.`

## 풀이를 따라가기

최소 남은 시간을 기준으로 모든 음식에서 같은 높이의 층을 한꺼번에 제거합니다. 한 층 비용은 높이 차×남은 음식 수입니다. 남은 시간이 그 비용보다 작아지는 층에서 멈춥니다.

완전히 제거한 층은 원래 원형 순회와 같은 양을 소비합니다. 마지막 음식들을 원래 번호순으로 정렬하고 남은 초를 개수로 나눈 나머지 위치를 택하면 정확한 다음 음식입니다.

## 다른 방법과 비교

대안은 deque로 매초 실제 음식을 하나 소비합니다. 이해하기 쉽고 작은 k의 검산에 유용하지만 대안 코드는 k≤200000으로 제한합니다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O(N log N)` | `O(N)` |
| 대안 풀이 | `O(N+k)` | `O(N)` |

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었습니다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교합니다. 실행 기록은 [validation.json](validation.json)에 있습니다. 원본 제출 파일은 [submitted_original.py](submitted_original.py)에 그대로 보관했습니다.

```bash
python test_solution.py
```

## English

### Problem and constraints

Eat one second from foods cyclically, skipping exhausted foods, and identify the next food after k seconds.

Input limits and constants, using the parameter names in the code:

`efficiency: 1≤N≤200000; 1≤food_times[i]≤10^8; 1≤k≤2·10^13; return −1 if all consumed.`

### Following the solution

Remove equal-height layers in bulk. A layer costs the next height difference times the remaining food count; stop when the remaining budget cannot remove a complete layer.

Each removed layer matches full cyclic rounds. Sort surviving foods by original index and take the residual time modulo their count to locate the next food.

### Alternative and comparison

The alternative simulates every second with a deque. Its k≤200000 cap makes it a readable small-time reference rather than the efficiency solution.

The primary solution takes `O(N log N)` time and `O(N)` additional space. The alternative takes `O(N+k)` time. Its additional space is `O(N)`.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.py](submitted_original.py).

## 출처 / Source

- [Programmers — 무지의 먹방 라이브](https://school.programmers.co.kr/learn/courses/30/lessons/42891): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.
