# 리프 노드 수 최대화

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/468372) · Level 2 · Python3

분배 노드 수와 경로 분배도 제한을 지키며 리프 수를 최대화합니다.

## 조건과 입출력

입력 매개변수: `dist_limit, split_limit`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과입니다.

- 0 ≤ dist_limit ≤ 10^9
- 1 ≤ split_limit ≤ 10^9

## 풀이를 따라가기

앞쪽 이진 분기의 깊이 d를 정하고 가능한 삼진 깊이 t를 붙입니다. 마지막 이진 층의 분배 노드가 count개라면 이진 노드 수 B=count+ceil(count/2)+…이고, 그 아래 시작 가지는 2count개입니다. 삼진 노드를 최대로 놓을 수 있는 수는 2count·(3^t−1)/2=count·(3^t−1)입니다. B와 삼진 용량의 합이 예산과 만나는 두 후보를 이진 탐색합니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(dist_limit, split_limit):
    def binary_cost(count, depth):
        total = 0
        for _ in range(depth):
            # 이 깊이에 필요한 분배 노드 수를 더한다.
            total += count
            # 한 층 위에서 필요한 부모 수를 올림 나눗셈으로 구한다.
            count = (count + 1) // 2
        return total

    answer = 1
    width = 1
    depth = 0
    while width <= split_limit:
        answer = max(answer, min(width, dist_limit + 1))
        power = 1
        while width * power * 3 <= split_limit:
            power *= 3
        if depth == 0:
            answer = max(answer, 1 + 2 * min(dist_limit, (power - 1) // 2))
        elif power > 1:
            low, high = 1, width // 2
            while low < high:
                mid = (low + high) // 2
                needed = binary_cost(mid, depth) + mid * (power - 1)
                if needed >= dist_limit:
                    high = mid
                else:
                    low = mid + 1
            # 예산과 용량이 만나는 경계 양쪽을 확인한다.
            for count in (low - 1, low):
                if count == 0:
                    continue
                used = binary_cost(count, depth)
                if used <= dist_limit:
                    ternary = min(dist_limit - used, count * (power - 1))
                    answer = max(answer, 1 + used + 2 * ternary)
        width *= 2
        depth += 1
    return answer
```

## 정답이 되는 이유

이진 분배 노드 B개와 삼진 분배 노드 T개가 있으면 리프는 1+B+2T개입니다. 같은 경로 분배도를 만드는 2·3 분기 순서를 비교할 때 이진 단계를 앞에 모으면 마지막 이진 층의 노드들이 더 적은 수의 조상을 공유할 수 있습니다. 고정한 깊이에서 B는 최소 조상 수로 만들고 T는 남은 예산과 용량 중 작은 값으로 채웁니다. 용량을 다 쓰는 구간에서는 count가 클수록, 예산이 먼저 소진되는 구간에서는 B가 작을수록 좋으므로 경계 양쪽이면 충분합니다. 예를 들어 예산 3·분배도 6은 B=1,T=2로 리프 6개입니다.

시간 O((log S)^3), 공간 O(log S) 이하 / Time O((log S)^3), space at most O(log S); S=split_limit

주의할 점: 분배 노드가 0개면 리프는 1개입니다. 같은 깊이에서 2분기와 3분기를 섞지 않습니다. 아래 완전 탐색은 작은 입력에서 이 최적화와 독립 비교하는 용도입니다.

## 다른 방법: 깊이별 분기 수 완전 탐색 · 작은 입력

이 대안은 작은 입력에서 원리를 비교하는 검증용입니다. 최대 제한에 제출할 기본 풀이와 구분합니다.

```python
from functools import lru_cache

def solution(dist_limit, split_limit):
    if dist_limit > 10 or split_limit > 50:
        raise ValueError('작은 입력 검증용: 분배 노드 10개, 분배도 50 이하')
    @lru_cache(None)
    def search(product, available, remaining):
        best = 0
        for degree in (2, 3):
            if product * degree > split_limit:
                continue
            for chosen in range(1, min(available, remaining)+1):
                # 이 깊이에서 chosen개만 확장하고 나머지는 리프로 끝낸다.
                added = chosen * (degree-1)
                best = max(best, added + search(product*degree, chosen*degree, remaining-chosen))
        return best
    return 1 + search(1, 1, dist_limit)
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 앞쪽 이진 분기의 깊이 d를 정하고 가능한 삼진 깊이 t를 붙입니다. 마지막 이진 층의 분배 노드가 count개라면 이진 노드 수 B=count+ceil(count/2)+…이고, 그 아래 시작 가지는 2count개입니다. 삼진 노드를 최대로 놓을 수 있는 수는 2count·(3^t−1)/2=count·(3^t−1)입니다. B와 삼진 용량의 합이 예산과 만나는 두 후보를 이진 탐색합니다. | 깊이별 분기 수 완전 탐색 · 작은 입력 |
| 비용 | 시간 O((log S)^3), 공간 O(log S) 이하 / Time O((log S)^3), space at most O(log S); S=split_limit | 상한 O(SD^3) 시간, O(SD^2) 공간 / upper bounds O(SD^3) time, O(SD^2) space; D=dist_limit |

## 검증

공식 예제 4개와 생성 입력 550개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Maximize leaves subject to a distributor budget and a bound on every root-to-leaf branching product.

### Conditions and input/output

Input arguments: `dist_limit, split_limit`. The return value is an integer satisfying the task described below.

- 0 ≤ dist_limit ≤ 10^9; 1 ≤ split_limit ≤ 10^9

### Approach

Choose d binary levels followed by t ternary levels. If count distributors occupy the last binary level, the minimum binary-node total is B=count+ceil(count/2)+…, with 2count branches below them. The ternary-node capacity is 2count·(3^t−1)/2=count·(3^t−1). Binary-search the two counts around the point where B plus that capacity reaches the budget.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

With B binary and T ternary distributors, the leaf count is 1+B+2T. For a fixed path product, placing binary levels before ternary levels permits the required final binary distributors to share a smaller ancestor structure. At fixed depths, use this minimum B and fill T up to the budget or capacity. Before capacity reaches the budget, larger count improves the result; after the budget binds, smaller B is better, so the two adjacent counts suffice. For budget 3 and product bound 6, B=1 and T=2 give six leaves.

시간 O((log S)^3), 공간 O(log S) 이하 / Time O((log S)^3), space at most O(log S); S=split_limit

Boundary cases: Zero distributors leave one leaf. Binary and ternary distributors cannot mix at one depth. The exhaustive alternative independently checks the optimization on small inputs.

### Alternative: Exhaustive level-by-level branching for small inputs

This alternative is for understanding and checking small inputs; use the main implementation for the full constraints. 상한 O(SD^3) 시간, O(SD^2) 공간 / upper bounds O(SD^3) time, O(SD^2) space; D=dist_limit

### Verification

Local checks covered 4 official examples and 550 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 리프 노드 수 최대화](https://school.programmers.co.kr/learn/courses/30/lessons/468372) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
