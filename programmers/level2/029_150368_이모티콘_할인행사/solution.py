# 문제: 이모티콘 할인행사
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/150368
# 풀이: 네 할인율의 모든 조합을 평가한다. 가입자 수를 먼저, 매출을 다음 기준으로 비교하는 튜플로 최적 결과를 고른다.
# 복잡도: 사용자 N명·이모티콘 M개: 시간 O(4^M NM), 반환값 외 추가 공간 O(M).

from itertools import product

def solution(users, emoticons):
    best = (0, 0)
    for rates in product((10, 20, 30, 40), repeat=len(emoticons)):
        subscribers = revenue = 0
        for minimum, limit in users:
            cost = sum(price * (100 - rate) // 100 for price, rate in zip(emoticons, rates) if rate >= minimum)
            if cost >= limit:
                subscribers += 1
            else:
                revenue += cost
        best = max(best, (subscribers, revenue))
    return list(best)
