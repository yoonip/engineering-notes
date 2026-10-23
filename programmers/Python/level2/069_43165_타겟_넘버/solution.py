from collections import Counter

def solution(numbers, target):
    # 숫자를 사용하기 전 합 0을 만드는 방법은 1개.
    ways = Counter({0: 1})
    for number in numbers:
        # 다음 숫자까지 사용한 방법 수를 담을 빈 Counter.
        next_ways = Counter()
        for total, count in ways.items():
            # 이번 숫자를 더하는 모든 방법 누적.
            next_ways[total + number] += count
            next_ways[total - number] += count
        # =로 다음 단계의 방법 수 표로 교체.
        ways = next_ways
    return ways[target]
