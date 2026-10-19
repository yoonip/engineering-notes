# 징검다리 건너기

Level 3 · [64062 공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/64062)

## 문제와 조건

건널 때마다 돌 내구도가 1씩 줄고 빈 돌을 최대 k−1개 건너뛸 수 있을 때 건널 수 있는 최대 인원을 구합니다.

`1≤N≤200,000; 1≤stones[i]≤200,000,000; 1≤k≤N`

## 풀이를 따라가기

1. 연속 k개 돌이 모두 0이 되면 다음 사람은 k+1칸을 뛰어야 하므로 실패한다. 한 구간이 모두 소진되는 인원은 그 구간의 최대 내구도다.
2. 따라서 길이 k인 모든 구간의 최댓값 중 최솟값이 답이다. 단조 큐로 각 구간의 최댓값을 빠르게 유지한다.
3. 예제는 [3,2,1] 구간의 최대가 3이어서 세 명까지 가능하다. 각 인덱스는 한 번 들어오고 나가므로 시간 O(N), 공간 O(K).

## 왜 이 방법으로 풀 수 있나

연속 k개 돌이 모두 0이 되면 다음 사람은 k+1칸을 뛰어야 하므로 실패한다. 한 구간이 모두 소진되는 인원은 그 구간의 최대 내구도다.

시간·공간: 시간 O(N), 공간 O(K).

## 다른 방법과 비교

p명이 건너려면 원래 내구도가 p보다 작은 돌이 k개 연속이면 안 됩니다. 가능한 인원의 최댓값을 이분탐색합니다. 단조 큐보다 느리지만 조건을 직접 검사합니다.

| 항목 | 기본 풀이 | 통과 인원 이분탐색 |
|---|---|---|
| 코드 | [solution.py](solution.py) | [alternative.py](alternative.py) |
| 비용 | 시간 O(N), 공간 O(K). | O(N log 최대 내구도), 공간 O(1) |
| 용도 | 기본 제출 구현 | 대안 구현 |

## 예제와 검증

| 인수 / Arguments | 결과 / Result |
|---|---|
| `[[2, 4, 5, 3, 2, 1, 4, 2, 5, 1], 3]` | `3` |

공식 예제와 별도 경계·무작위 입력을 사용합니다. 대안이 전수검사라면 작은 입력에서만 비교합니다.

[실행 예제](examples.json) · [실제 제출 원본](submitted_original.py)

## English

### Task and constraints

Find the maximum number of people crossing stones whose durability decreases per use, allowing at most k−1 consecutive exhausted stones to be skipped.

`1≤N≤200,000; 1≤stones[i]≤200,000,000; 1≤k≤N`

### Method and correctness

For a length-k window, its maximum durability is the number of people that exhausts all stones in that window. The smallest such maximum is the crossing limit. Maintain each sliding-window maximum with a decreasing deque; every index enters and leaves at most once.

Main complexity: O(N) time, O(k) deque space.

### Alternative and trade-offs

For p people to cross, there must be no run of k stones with original durability below p. Binary-search the largest feasible p; it is slower than the monotone deque but checks feasibility directly.

Code: [alternative.py](alternative.py). Scope: alternative implementation.

Complexity: O(N log max durability), space O(1).

### Verification

Use official examples and separate edge/random inputs. Exhaustive alternatives are compared only on small inputs.

The table above supplies argument arrays and expected results; [examples.json](examples.json) stores them as executable data. The original locally stored submission was graded 100; comments and the separate alternative are reviewed and tested locally, which is distinct from a new website submission.

## 출처 / Sources

- [프로그래머스 공식 문제: 징검다리 건너기](https://school.programmers.co.kr/learn/courses/30/lessons/64062) — 문제 조건·예제·함수 인터페이스 / task rules, examples and interface. 확인 / checked: 2026-10-19.

## 실행 / Run

```bash
python test_solution.py
```

공식 예제·경계 입력·고정 시드 비교 입력을 합쳐 43개 입력에서 86회 검사를 통과했습니다.

Passed 86 implementation checks across 43 official, boundary and fixed-seed differential inputs.
