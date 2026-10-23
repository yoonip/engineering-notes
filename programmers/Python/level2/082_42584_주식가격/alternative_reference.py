def solution(prices):
    result = []
    for i, price in enumerate(prices):
        duration = 0
        for following in prices[i + 1:]:
            duration += 1
            if following < price:
                break
        result.append(duration)
    return result
