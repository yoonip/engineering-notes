# 선수 수와 승패 기록을 받음.
def solution(n, results):
    # wins[i][j]는 i가 j보다 강한지 나타내는 불리언(True/False) 표.
    wins = [[False] * n for _ in range(n)]
    # for로 승자·패자 번호를 언패킹.
    for winner, loser in results:
        # 입력은 1번부터, 배열은 0번부터이므로 1을 빼서 승리 기록.
        wins[winner - 1][loser - 1] = True
    # 중간 선수를 한 명씩 허용하는 플로이드-워셜 방식.
    for middle in range(n):
        # 출발 선수 순회.
        for first in range(n):
            # first가 middle을 이길 수 있을 때만 전파.
            if wins[first][middle]:
                # 도착 선수 순회.
                for last in range(n):
                    # middle이 last를 이기면 first도 last보다 강함.
                    if wins[middle][last]:
                        # 간접적으로 알 수 있는 승패까지 기록.
                        wins[first][last] = True
    # 순위가 확정되는 선수 수.
    answer = 0
    # 각 선수의 비교 가능한 상대 수 확인.
    for player in range(n):
        # sum은 True를 1로 세어 승리·패배 중 하나라도 아는 상대 수 합산.
        known = sum(wins[player][other] or wins[other][player] for other in range(n))
        # 자신 이외의 모든 선수와 비교할 수 있어야 순위 확정.
        if known == n - 1:
            # +=는 더해 저장.
            answer += 1
    # 확정된 선수 수 반환.
    return answer
