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

        # 번들을 사지 않는 선택부터 확인한다.
        dfs(stage + 1, total)
        bundle = hint[stage]
        # 다음 스테이지용 티켓을 지급한다.
        for number in bundle[1:]:
            tickets[number - 1] += 1
        dfs(stage + 1, total + bundle[0])
        for number in bundle[1:]:
            # 다른 선택을 비교할 수 있도록 티켓 수를 되돌린다.
            tickets[number - 1] -= 1

    dfs(0, 0)
    return answer
