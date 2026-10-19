# 완전범죄

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/389480) · Level 2 · Python3

물건을 A 또는 B에게 배정해 둘 다 체포되지 않으면서 A의 흔적을 최소화한다.

## 조건과 입출력

입력 매개변수: `info, n, m`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과다.

- 1 ≤ info의 길이 ≤ 40
- 1 ≤ 흔적 개수 ≤ 3
- 1 ≤ n ≤ 120
- 1 ≤ m ≤ 120

## 풀이를 따라가기

dp[b]는 B의 흔적이 b일 때 가능한 최소 A 흔적이다. 물건 하나를 A가 맡는 경우와 B가 맡는 경우로 새 배열을 만든다. 기준 이상인 상태는 버린다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(info, n, m):
    # B 흔적별 최소 A 흔적을 저장하며 n은 불가능 상태다.
    dp = [n] * m
    dp[0] = 0
    for a_trace, b_trace in info:
        # 물건 하나를 중복 배정하지 않도록 다음 상태를 따로 만든다.
        next_dp = [n] * m
        for b_used, a_used in enumerate(dp):
            if a_used == n:
                continue
            if a_used + a_trace < n:
                next_dp[b_used] = min(next_dp[b_used], a_used + a_trace)
            # B가 맡을 때도 체포 기준 미만이어야 한다.
            if b_used + b_trace < m:
                next_dp[b_used + b_trace] = min(next_dp[b_used + b_trace], a_used)
        dp = next_dp
    answer = min(dp)
    return answer if answer < n else -1
```

## 왜 맞는가

B의 흔적이 같으면 A의 흔적이 더 큰 상태는 이후에도 이득이 없다. 따라서 최소값 하나만 남겨도 최적 배정을 잃지 않는다.

시간 O(Nm), 공간 O(m) / Time O(Nm), space O(m); N=len(info)

주의할 점: 흔적은 기준 미만이어야 한다. 같은 배열을 즉시 갱신하면 한 물건을 여러 번 배정할 수 있어 다음 배열을 따로 쓴다.

## 다른 방법: A·B 흔적 쌍의 집합 DP

```python
def solution(info, n, m):
    states = {(0, 0)}
    for a, b in info:
        following = set()
        for ta, tb in states:
            if ta+a < n:
                following.add((ta+a, tb))
            if tb+b < m:
                following.add((ta, tb+b))
        states = following
    return min((a for a, b in states), default=-1)
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | dp[b]는 B의 흔적이 b일 때 가능한 최소 A 흔적이다. 물건 하나를 A가 맡는 경우와 B가 맡는 경우로 새 배열을 만든다. 기준 이상인 상태는 버린다. | A·B 흔적 쌍의 집합 DP |
| 비용 | 시간 O(Nm), 공간 O(m) / Time O(Nm), space O(m); N=len(info) | 시간 O(Nnm), 공간 O(nm) / Time O(Nnm), space O(nm) |

## 검증

공식 예제 4개와 생성 입력 80개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다. 제한 상한에 해당하는 크기·수치의 경계 검사도 저장된 테스트에 포함했다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Assign each item to A or B, keeping both below their arrest thresholds while minimizing A’s trace.

### Conditions and input/output

Input arguments: `info, n, m`. The return value is an integer satisfying the task described below.

- 1 ≤ len(info) ≤ 40; 1 ≤ trace per item ≤ 3
- 1 ≤ n,m ≤ 120; A trace < n and B trace < m

### Approach

Let dp[b] be the least A trace achievable with B trace b. For each item, create a fresh array from assigning it to A or B; discard states reaching either threshold.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

For equal B trace, a larger A trace can never improve a later assignment. Keeping only the minimum therefore preserves an optimum.

시간 O(Nm), 공간 O(m) / Time O(Nm), space O(m); N=len(info)

Boundary cases: Traces must be strictly below the thresholds. A fresh array prevents assigning the same item repeatedly.

### Alternative: Set-based DP over both trace totals

시간 O(Nnm), 공간 O(nm) / Time O(Nnm), space O(nm)

### Verification

Local checks covered 4 official examples and 80 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases. Saved tests also include a size or numeric boundary at the stated upper limit.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 완전범죄](https://school.programmers.co.kr/learn/courses/30/lessons/389480) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
