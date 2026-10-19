# 문제: 비밀 코드 해독
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/388352
# 풀이: 서로 다른 다섯 숫자의 조합을 만들고 각 시도와의 교집합 크기를 비교한다. 크기가 고정된 집합으로 일치 수를 확인한다.
# 복잡도: 가능 숫자 N개·시도 Q개: 시간 O(조합(N,5)·Q), 추가 공간 O(Q). 한 집합은 5개 원소다.

from itertools import combinations


def solution(n, q, ans):
    attempts = [set(attempt) for attempt in q]
    answer = 0

    for candidate in combinations(range(1, n + 1), 5):
        code = set(candidate)
        valid = True
        for attempt, matched in zip(attempts, ans):
            if len(code & attempt) != matched:
                valid = False
                break
        if valid:
            answer += 1

    return answer
