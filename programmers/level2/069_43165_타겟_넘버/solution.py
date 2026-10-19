# 문제: 타겟 넘버
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/43165
# 풀이: 합별 방법 수를 Counter에 저장하고 다음 숫자의 +와 -를 더한다. 같은 합으로 모인 경로는 개수만 합쳐 재사용한다.
# 복잡도: 숫자 N개·절댓값 합 S: 시간 상한 O(N(S+1)), 추가 공간 O(S+1).

from collections import Counter

def solution(numbers, target):
    ways = Counter({0: 1})
    for number in numbers:
        next_ways = Counter()
        for total, count in ways.items():
            next_ways[total + number] += count
            next_ways[total - number] += count
        ways = next_ways
    return ways[target]
