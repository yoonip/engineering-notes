# n + 1 카드게임

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/258707) · Level 3 · Python3

## 문제와 조건 / Task and conditions

n은 6의 배수로 6≤n<1000이고 카드는 1~n의 순열입니다. 초기 n/3장은 무료, 매 라운드 새 두 장은 동전으로 고릅니다. n+1 쌍을 내며 도달하는 최대 라운드를 반환합니다.

n is a multiple of six with 6≤n<1000; cards permute 1…n. The first n/3 cards are free; choose purchases from two new cards each round and discard a sum-(n+1) pair. Return the maximum reached round.

## 풀이 흐름 / Approach

합이 n+1인 카드 쌍은 서로 카드를 공유하지 않습니다. 처음 가진 카드끼리는 0원, 새 카드 한 장을 포함하면 1원, 새 카드 두 장이면 2원으로 쌍을 분류합니다. 매 라운드 완성된 쌍 중 가장 싼 것을 사용합니다.

Pairs summing to n+1 never share a card. Classify completed pairs by cost: zero for two initial cards, one for one drawn card, and two for two drawn cards. Spend the cheapest available pair each round.

## 정답이 되는 이유 / Why it works

한 카드의 짝은 유일하여 한 쌍을 써도 다른 쌍을 망가뜨리지 않습니다. 비싼 쌍보다 싼 쌍을 먼저 쓰는 교환은 이후 사용할 수 있는 총예산을 줄이지 않습니다. 쌍을 쓸 때 비용을 내는 결정은 그 카드를 뽑을 때 샀던 전략으로 되돌려 해석할 수 있습니다.

Each card has a unique partner, so using one pair cannot destroy another. Exchanging an expensive early pair for a cheaper one never reduces future budget. Deferred payment can be interpreted as buying those selected cards when originally drawn.

## 비용 / Complexity

시간·공간 O(n) / O(n) time and space

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(coin, cards):
    # len은 카드 개수.
    n = len(cards)
    target = n + 1
    # set은 초기 카드의 포함 여부를 확인할 집합.
    initial = set(cards[:n // 3])
    drawn = set()
    # 동전 0·1·2개로 사용할 수 있는 완성된 카드 쌍의 수.
    available = [0, 0, 0]
    for card in initial:
        # 초기 카드끼리의 쌍을 작은 카드에서만 세어 중복 방지.
        if card < target - card and target - card in initial:
            available[0] += 1
    # 게임은 1라운드부터 시작.
    round_number = 1
    for index in range(n // 3, n, 2):
        # 이번 라운드의 두 카드를 순회.
        for card in cards[index:index + 2]:
            partner = target - card
            # 짝이 초기 카드라면 새 카드 한 장만 구매하면 됨.
            if partner in initial:
                available[1] += 1
            elif partner in drawn:
                # 두 번째 카드가 나올 때만 세므로 중복되지 않음.
                available[2] += 1
            drawn.add(card)
        # 비용 0,1,2 순서로 쌍을 선택하는 그리디.
        for price in range(3):
            if available[price] and coin >= price:
                # 선택한 쌍 하나를 소모.
                available[price] -= 1
                coin -= price
                # 다음 라운드로 진행.
                round_number += 1
                break
        else:
            return round_number
    return round_number
```

## 다른 방법: 구매·제출 선택의 메모이제이션 / Memoized explicit buying and discarding

매 라운드 두 카드의 구매 조합과 낼 수 있는 쌍을 모두 고릅니다. 문제 규칙을 직접 구현한 지수 상태 탐색으로, n=6·12의 작은 입력에서 그리디를 검증합니다.

Enumerate purchases of each drawn pair and every legal pair to discard. This exponential state search directly follows the rules and checks the greedy method on small n such as 6 or 12.

[alternative_reference.py](alternative_reference.py)

```python
from functools import lru_cache

def solution(coin, cards):
    n = len(cards)
    @lru_cache(None)
    def play(index, money, hand):
        if index == n:
            return 1
        best = 1
        drawn = cards[index:index + 2]
        for purchase in range(4):
            price = purchase.bit_count()
            if price > money:
                continue
            owned = set(hand)
            owned.update(drawn[i] for i in range(2) if purchase >> i & 1)
            for first in sorted(owned):
                second = n + 1 - first
                if first < second and second in owned:
                    rest = tuple(sorted(owned - {first, second}))
                    best = max(best, 1 + play(index + 2, money - price, rest))
        return best
    return play(n // 3, coin, tuple(sorted(cards[:n // 3])))
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    4,
    [
      3,
      6,
      7,
      2,
      1,
      10,
      5,
      9,
      8,
      12,
      11,
      4
    ]
  ],
  "output": 5
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 32개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 32 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 32개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 32 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 258707](https://school.programmers.co.kr/learn/courses/30/lessons/258707), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 258707](https://school.programmers.co.kr/learn/courses/30/lessons/258707), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
