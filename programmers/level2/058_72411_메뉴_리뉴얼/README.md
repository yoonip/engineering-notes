# 메뉴 리뉴얼

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/72411) · Level 2 · Python3

주문에서 함께 많이 선택된 메뉴 조합을 코스 길이별로 고른다.

## 조건과 입출력

입력 매개변수: `orders, course`. 반환값은 문자열 배열이며 아래 풀이의 조건을 만족하는 결과다.

- orders 배열의 크기는 2 이상 20 이하입니다.
- orders 배열의 각 원소는 크기가 2 이상 10 이하인 문자열입니다.
- course 배열의 크기는 1 이상 10 이하입니다.
- course 배열의 각 원소는 2 이상 10 이하인 자연수가 오름차순으로 정렬되어 있습니다.
- 정답은 각 코스요리 메뉴의 구성을 문자열 형식으로 배열에 담아 사전 순으로 오름차순 정렬해서 return 해주세요.
- 배열의 각 원소에 저장된 문자열 또한 알파벳 오름차순으로 정렬되어야 합니다.
- orders와 course 매개변수는 return 하는 배열의 길이가 1 이상이 되도록 주어집니다.

## 풀이를 따라가기

주문 문자를 정렬해 조합 표현을 통일한다. 각 길이의 조합을 Counter로 센다. 두 번 이상 나온 조합 중 최고 빈도인 것을 모두 고르고 전체를 정렬한다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
from collections import Counter
from itertools import combinations

def solution(orders, course):
    orders = [sorted(order) for order in orders]
    answer = []
    for size in course:
        counts = Counter()
        for order in orders:
            # 주문마다 해당 크기 메뉴 조합의 빈도를 더한다.
            counts.update(combinations(order, size))
        highest = max(counts.values(), default=0)
        # 두 명 이상이 주문한 최빈 조합만 새 코스로 고른다.
        if highest >= 2:
            answer.extend(''.join(menu) for menu, count in counts.items() if count == highest)
    return sorted(answer)
```

## 왜 맞는가

정렬된 조합은 메뉴 순서와 무관하게 같은 키가 된다. 주문당 해당 조합을 한 번 세고 길이별 최댓값을 고르면 문제의 코스 선정 조건과 일치한다.

시간 O(Σ주문 Σ길이 C(L,k)·k), 공간 O(서로 다른 조합 수) / Time O(Σorders Σsizes C(L,k)·k), space O(distinct combinations)

주의할 점: 최빈 조합이 한 번만 등장하면 제외한다. 각 코스 길이는 따로 최댓값을 구한다.

## 다른 방법: 후보 집합 생성 후 주문 포함 검사

```python
from itertools import combinations

def solution(orders,course):
    order_sets=[set(order) for order in orders]
    answer=[]
    for size in course:
        candidates={''.join(c) for order in orders for c in combinations(sorted(order),size)}
        counts={candidate:sum(set(candidate)<=order for order in order_sets) for candidate in candidates}
        maximum=max(counts.values(),default=0)
        if maximum>=2: answer.extend(c for c,n in counts.items() if n==maximum)
    return sorted(answer)
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 주문 문자를 정렬해 조합 표현을 통일한다. 각 길이의 조합을 Counter로 센다. 두 번 이상 나온 조합 중 최고 빈도인 것을 모두 고르고 전체를 정렬한다. | 후보 집합 생성 후 주문 포함 검사 |
| 비용 | 시간 O(Σ주문 Σ길이 C(L,k)·k), 공간 O(서로 다른 조합 수) / Time O(Σorders Σsizes C(L,k)·k), space O(distinct combinations) | 시간 O(C·N·L), 공간 O(C·L) / Time O(C·N·L), space O(C·L); C=후보 수 / candidate count |

## 검증

공식 예제 3개와 생성 입력 50개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Select the most frequently co-ordered menu combinations for each course length.

### Conditions and input/output

Input arguments: `orders, course`. The return value is a list of strings satisfying the task described below.

- 2 ≤ len(orders) ≤ 20; 2 ≤ each order length ≤ 10
- 1 ≤ len(course) ≤ 10; distinct increasing course sizes 2 … 10
- uppercase menu letters, no repeated menu within an order

### Approach

Sort each order to canonicalize combinations. Count combinations of each requested size, retain all maximum-frequency ones appearing at least twice, and sort the final list.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Canonical combinations ignore menu order. Counting each per order and selecting each size’s maximum exactly implements the course rule.

시간 O(Σ주문 Σ길이 C(L,k)·k), 공간 O(서로 다른 조합 수) / Time O(Σorders Σsizes C(L,k)·k), space O(distinct combinations)

Boundary cases: Exclude combinations occurring only once. Find the maximum separately for each course size.

### Alternative: Generate candidate sets, then test order containment

시간 O(C·N·L), 공간 O(C·L) / Time O(C·N·L), space O(C·L); C=후보 수 / candidate count

### Verification

Local checks covered 3 official examples and 50 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 메뉴 리뉴얼](https://school.programmers.co.kr/learn/courses/30/lessons/72411) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
