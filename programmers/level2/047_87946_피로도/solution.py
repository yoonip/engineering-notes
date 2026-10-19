from itertools import permutations

def solution(k, dungeons):
    answer = 0
    # 최대 8개 던전의 모든 방문 순서를 비교한다.
    for order in permutations(dungeons):
        remaining, count = k, 0
        for required, cost in order:
            # 입장 조건을 못 맞추면 해당 순서의 진행은 여기까지다.
            if remaining < required:
                break
            remaining -= cost
            count += 1
        answer = max(answer, count)
    return answer
