# 문제: 힌트 스테이지
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/468377
# 풀이: 단계마다 힌트 구매 여부를 DFS로 비교한다. 티켓 수를 변경한 뒤 되돌려 상태 복사 없이 다음 선택을 탐색한다.
# 복잡도: 단계 N개·힌트 묶음 최대 길이 H: 시간 O(2^N H), 추가 공간 O(N).

def solution(cost, hint):
    n = len(cost)
    tickets = [0] * n
    answer = sum(row[0] for row in cost)

    def dfs(stage, total):
        nonlocal answer
        total += cost[stage][min(tickets[stage], n - 1)]
        if stage == n - 1:
            answer = min(answer, total)
            return

        dfs(stage + 1, total)
        bundle = hint[stage]
        for number in bundle[1:]:
            tickets[number - 1] += 1
        dfs(stage + 1, total + bundle[0])
        for number in bundle[1:]:
            tickets[number - 1] -= 1

    dfs(0, 0)
    return answer
