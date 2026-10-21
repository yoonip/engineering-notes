# [PCCP 기출문제] 2번 / 퍼즐 게임 챌린지

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/340212) · Level 2 · Python3

모든 퍼즐을 제한 시간 안에 푸는 최소 숙련도를 구합니다.

## 조건과 입출력

입력 매개변수: `diffs, times, limit`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과입니다.

- 1 ≤ diffs의 길이 = times의 길이 = n ≤ 300,000
- 1 ≤ diffs[i] ≤ 100,000
- 1 ≤ times[i] ≤ 10,000
- 1 ≤ limit ≤ 10^15

## 풀이를 따라가기

숙련도 하나를 정해 총 소요 시간을 계산합니다. 난도가 높으면 차이만큼 실패하며 현재 퍼즐과 이전 퍼즐 시간을 더 냅니다. 성공 가능한 숙련도 구간을 이진 탐색합니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(diffs, times, limit):
    left = 1
    right = max(diffs)
    # 소요 시간이 제한 안에 들어오는 최소 숙련도를 찾는다.
    while left < right:
        level = (left + right) // 2
        elapsed = 0
        previous = 0
        for diff, current in zip(diffs, times):
            elapsed += current
            if diff > level:
                # 실패 한 번에는 현재 퍼즐과 이전 퍼즐 시간이 함께 든다.
                elapsed += (diff - level) * (current + previous)
            # 이미 제한을 넘었으므로 이 숙련도의 나머지 계산은 필요 없다.
            if elapsed > limit:
                break
            previous = current
        if elapsed <= limit:
            right = level
        else:
            left = level + 1
    return left
```

## 정답이 되는 이유

숙련도가 커지면 모든 퍼즐의 실패 횟수가 줄거나 같아 총시간이 늘지 않습니다. 이 단조성으로 최소 성공 숙련도를 이진 탐색할 수 있습니다.

시간 O(N log D), 공간 O(1) / Time O(N log D), space O(1); D=max(diffs)

주의할 점: 첫 퍼즐 이전의 시간은 0입니다. 누적 시간이 limit를 넘으면 즉시 중단합니다.

## 다른 방법: 숙련도 순차 탐색 · 작은 난도

이 대안은 작은 입력에서 원리를 비교하는 검증용입니다. 최대 제한에 제출할 기본 풀이와 구분합니다.

```python
def solution(diffs, times, limit):
    for level in range(1, max(diffs)+1):
        total = 0
        for i, (difficulty, duration) in enumerate(zip(diffs, times)):
            previous = times[i-1] if i else 0
            total += duration + max(0,difficulty-level)*(duration+previous)
        if total <= limit:
            return level
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 숙련도 하나를 정해 총 소요 시간을 계산합니다. 난도가 높으면 차이만큼 실패하며 현재 퍼즐과 이전 퍼즐 시간을 더 냅니다. 성공 가능한 숙련도 구간을 이진 탐색합니다. | 숙련도 순차 탐색 · 작은 난도 |
| 비용 | 시간 O(N log D), 공간 O(1) / Time O(N log D), space O(1); D=max(diffs) | 시간 O(ND), 공간 O(1) / Time O(ND), space O(1) |

## 검증

공식 예제 4개와 생성 입력 50개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다. 제한 상한에 해당하는 크기·수치의 경계 검사도 저장된 테스트에 포함했습니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Find the minimum skill level that finishes all puzzles within the time limit.

### Conditions and input/output

Input arguments: `diffs, times, limit`. The return value is an integer satisfying the task described below.

- 1 ≤ len(diffs)=len(times) ≤ 300000; diffs[0]=1
- 1 ≤ diffs[i] ≤ 100000; 1 ≤ times[i] ≤ 10000; 1 ≤ limit ≤ 10^15
- a feasible skill always exists

### Approach

For a proposed skill, compute total time. Each excess difficulty unit adds a failure costing the current and previous puzzle times. Binary-search the first feasible skill.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Increasing skill never increases any failure count, so total time is nonincreasing. Binary search therefore finds the minimum feasible skill.

시간 O(N log D), 공간 O(1) / Time O(N log D), space O(1); D=max(diffs)

Boundary cases: The time before the first puzzle is zero. Stop evaluating a skill once accumulated time exceeds limit.

### Alternative: Linear skill search for small difficulty ranges

This alternative is for understanding and checking small inputs; use the main implementation for the full constraints. 시간 O(ND), 공간 O(1) / Time O(ND), space O(1)

### Verification

Local checks covered 4 official examples and 50 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases. Saved tests also include a size or numeric boundary at the stated upper limit.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: [PCCP 기출문제] 2번 / 퍼즐 게임 챌린지](https://school.programmers.co.kr/learn/courses/30/lessons/340212) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
