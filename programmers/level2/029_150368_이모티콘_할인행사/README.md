# 이모티콘 할인행사

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/150368) · Level 2 · Python3

가입자 수를 최우선으로, 그다음 이모티콘 매출을 최대화하는 할인 조합을 찾습니다.

## 조건과 입출력

입력 매개변수: `users, emoticons`. 반환값은 수치 배열이며 아래 풀이의 조건을 만족하는 결과입니다.

- 1 ≤ users의 길이 = n ≤ 100
- 비율% 이상의 할인이 있는 이모티콘을 모두 구매한다는 의미입니다.
- 1 ≤ 비율 ≤ 40
- 가격이상의 돈을 이모티콘 구매에 사용한다면, 이모티콘 구매를 모두 취소하고 이모티콘 플러스 서비스에 가입한다는 의미입니다.
- 100 ≤ 가격 ≤ 1,000,000
- 1 ≤ emoticons의 길이 = m ≤ 7
- 100 ≤ emoticons의 원소 ≤ 1,000,000

## 풀이를 따라가기

각 이모티콘에 10·20·30·40% 할인 중 하나를 배정합니다. 사용자별 구매 합계를 구해 기준 이상이면 가입, 아니면 매출에 더합니다. 결과를 (가입자,매출) 튜플로 비교합니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
from itertools import product

def solution(users, emoticons):
    best = (0, 0)
    # 각 상품의 네 할인율 조합을 빠짐없이 비교한다.
    for rates in product((10, 20, 30, 40), repeat=len(emoticons)):
        subscribers = revenue = 0
        for minimum, limit in users:
            cost = sum(price * (100 - rate) // 100 for price, rate in zip(emoticons, rates) if rate >= minimum)
            # 기준 이상이면 구매를 취소하고 가입자로 센다.
            if cost >= limit:
                subscribers += 1
            else:
                revenue += cost
        # 가입자 수를 먼저, 같은 경우 매출을 비교한다.
        best = max(best, (subscribers, revenue))
    return list(best)
```

## 정답이 되는 이유

모든 할인 조합을 빠짐없이 계산합니다. 튜플의 사전식 비교가 문제의 우선순위와 같으므로 최댓값이 요구한 답입니다.

시간 O(4^M·U·M), 공간 O(M) / Time O(4^M·U·M), space O(M)

주의할 점: 가입자의 구매액을 매출에 다시 더하지 않습니다. 할인율이 사용자 기준과 같아도 구매합니다.

## 다른 방법: 사용자별 누적 구매액을 갱신하는 DFS

```python
def solution(users,emoticons):
    spending=[0]*len(users)
    best=(0,0)
    def visit(index):
        nonlocal best
        if index==len(emoticons):
            joined=sum(paid>=user[1] for paid,user in zip(spending,users))
            revenue=sum(paid for paid,user in zip(spending,users) if paid<user[1])
            best=max(best,(joined,revenue))
            return
        for rate in (10,20,30,40):
            price=emoticons[index]*(100-rate)//100
            buyers=[i for i,user in enumerate(users) if rate>=user[0]]
            for i in buyers: spending[i]+=price
            visit(index+1)
            for i in buyers: spending[i]-=price
    visit(0)
    return list(best)
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 각 이모티콘에 10·20·30·40% 할인 중 하나를 배정합니다. 사용자별 구매 합계를 구해 기준 이상이면 가입, 아니면 매출에 더합니다. 결과를 (가입자,매출) 튜플로 비교합니다. | 사용자별 누적 구매액을 갱신하는 DFS |
| 비용 | 시간 O(4^M·U·M), 공간 O(M) / Time O(4^M·U·M), space O(M) | 시간 O(4^M·U), 공간 O(U+M) / Time O(4^M·U), space O(U+M) |

## 검증

공식 예제 2개와 생성 입력 35개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Choose discounts maximizing subscribers first and emoticon revenue second.

### Conditions and input/output

Input arguments: `users, emoticons`. The return value is a numeric list satisfying the task described below.

- 1 ≤ len(users) ≤ 100; minimum discount 1 … 40 percent
- 100 ≤ user budget, emoticon price ≤ 1000000; amounts are multiples of 100
- 1 ≤ len(emoticons) ≤ 7; discounts available: 10,20,30,40 percent

### Approach

Assign one of four discounts to each emoticon. Sum each user’s eligible purchases; convert them to a subscriber at the threshold, otherwise add their spending to revenue. Compare (subscribers,revenue).

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

All discount assignments are enumerated, and lexicographic tuple order exactly matches the two objectives.

시간 O(4^M·U·M), 공간 O(M) / Time O(4^M·U·M), space O(M)

Boundary cases: Do not add subscribers’ canceled purchases to revenue. A discount equal to the user’s minimum qualifies.

### Alternative: DFS with incremental per-user spending

시간 O(4^M·U), 공간 O(U+M) / Time O(4^M·U), space O(U+M)

### Verification

Local checks covered 2 official examples and 35 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 이모티콘 할인행사](https://school.programmers.co.kr/learn/courses/30/lessons/150368) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
