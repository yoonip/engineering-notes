from itertools import combinations


def solution(n, q, ans):
    attempts = [set(attempt) for attempt in q]
    answer = 0

    # 다섯 숫자의 순서 없는 모든 후보를 한 번씩 만든다.
    for candidate in combinations(range(1, n + 1), 5):
        code = set(candidate)
        valid = True
        for attempt, matched in zip(attempts, ans):
            # 각 시도에서 알려 준 공통 숫자 수와 정확히 같아야 한다.
            if len(code & attempt) != matched:
                valid = False
                break
        if valid:
            answer += 1

    return answer
