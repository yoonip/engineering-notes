# 힌트 스테이지

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/468377) · Level 2 · Python3

스테이지를 순서대로 해결하면서 힌트 번들의 구매 여부를 정해 총비용을 최소화한다.

## 조건과 입출력

입력 매개변수: `cost, hint`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과다.

- 2 ≤ cost의 길이 = n ≤ 16
- 1 ≤ cost[i][j] ≤ 100,000
- 2 ≤ hint[i]의 길이 = k+1 ≤ 20
- 0 ≤ hint[i][0] ≤ 1,000,000
- i+1 < hint[i][j] ≤ n (j>0)

## 풀이를 따라가기

현재 티켓 수로 이번 스테이지 비용을 낸다. 번들을 사지 않는 경우와 사는 경우를 나눠 다음 스테이지를 탐색한다. 구매한 티켓은 탐색이 끝나면 되돌린다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(cost, hint):
    n = len(cost)
    tickets = [0] * n
    answer = sum(row[0] for row in cost)

    def dfs(stage, total):
        nonlocal answer
        total += cost[stage][min(tickets[stage], n - 1)]
        if stage == n - 1:
            answer = min(answer, total)
            return

        # 번들을 사지 않는 선택부터 확인한다.
        dfs(stage + 1, total)
        bundle = hint[stage]
        # 다음 스테이지용 티켓을 지급한다.
        for number in bundle[1:]:
            tickets[number - 1] += 1
        dfs(stage + 1, total + bundle[0])
        for number in bundle[1:]:
            # 다른 선택을 비교할 수 있도록 티켓 수를 되돌린다.
            tickets[number - 1] -= 1

    dfs(0, 0)
    return answer
```

## 왜 맞는가

각 번들은 한 번만 구매할 수 있어 구매·미구매의 이진 선택이 모든 계획을 정확히 포함한다. 미래 스테이지 티켓만 지급되므로 현재까지의 비용은 확정할 수 있다.

시간 O(2^n K), 공간 O(n+K) / Time O(2^n K), space O(n+K); K=최대 번들 길이 / maximum bundle length

주의할 점: 같은 번호의 티켓이 반복될 수 있다. 비용표는 n−1장까지이므로 초과 티켓 수를 마지막 열로 제한한다.

## 다른 방법: 구매 집합 비트마스크 열거

```python
def solution(cost, hint):
    n = len(cost)
    answer = float('inf')
    for mask in range(1 << (n - 1)):
        tickets = [0] * n
        price = 0
        for i, bundle in enumerate(hint):
            if mask & (1 << i):
                price += bundle[0]
                for stage in bundle[1:]:
                    tickets[stage-1] += 1
        # 이전 단계에서만 지급되는 티켓이므로 구매 집합만 알면 비용이 확정된다.
        price += sum(cost[i][min(n-1, tickets[i])] for i in range(n))
        answer = min(answer, price)
    return answer
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 현재 티켓 수로 이번 스테이지 비용을 낸다. 번들을 사지 않는 경우와 사는 경우를 나눠 다음 스테이지를 탐색한다. 구매한 티켓은 탐색이 끝나면 되돌린다. | 구매 집합 비트마스크 열거 |
| 비용 | 시간 O(2^n K), 공간 O(n+K) / Time O(2^n K), space O(n+K); K=최대 번들 길이 / maximum bundle length | 시간 O(2^n(n+nK)), 공간 O(n) / Time O(2^n(n+nK)), space O(n) |

## 검증

공식 예제 6개와 생성 입력 40개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Minimize the total cost of sequential stages by deciding which hint bundles to buy.

### Conditions and input/output

Input arguments: `cost, hint`. The return value is an integer satisfying the task described below.

- 2 ≤ n=len(cost) ≤ 16; len(cost[i])=n
- 1 ≤ cost[i][j] ≤ 100000; cost[i][j] > cost[i][j+1]
- len(hint)=n−1; 2 ≤ len(hint[i]) ≤ 20; 0 ≤ bundle price ≤ 1000000
- ticket numbers in bundle i: i+2 … n, repetitions allowed

### Approach

Pay the current stage using the available tickets. Explore both skipping and buying its bundle, then undo bought tickets after returning from that branch.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Every valid plan is a binary choice for each bundle. Bundles contain only future-stage tickets, so already-paid stage costs never change.

시간 O(2^n K), 공간 O(n+K) / Time O(2^n K), space O(n+K); K=최대 번들 길이 / maximum bundle length

Boundary cases: A bundle may repeat a ticket number. Cap the lookup at n−1 tickets, the last cost column.

### Alternative: Enumerating purchase subsets with a bitmask

시간 O(2^n(n+nK)), 공간 O(n) / Time O(2^n(n+nK)), space O(n)

### Verification

Local checks covered 6 official examples and 40 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 힌트 스테이지](https://school.programmers.co.kr/learn/courses/30/lessons/468377) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
