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
