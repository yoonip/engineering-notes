def solution(n, results):
    wins = [[False] * n for _ in range(n)]
    for winner, loser in results:
        wins[winner - 1][loser - 1] = True
    for middle in range(n):
        for first in range(n):
            if wins[first][middle]:
                for last in range(n):
                    if wins[middle][last]:
                        wins[first][last] = True
    answer = 0
    for player in range(n):
        known = sum(wins[player][other] or wins[other][player] for other in range(n))
        if known == n - 1:
            answer += 1
    return answer

# 전체 코드 줄별 설명
# def solution(n, results):  # def는 함수 정의. 선수 수와 승패 기록을 받음.
#     wins = [[False] * n for _ in range(n)]  # []는 리스트. wins[i][j]는 i가 j보다 강한지 나타내는 불리언(True/False) 표.
#     for winner, loser in results:  # for로 승자·패자 번호를 언패킹.
#         wins[winner - 1][loser - 1] = True  # 입력은 1번부터, 배열은 0번부터이므로 1을 빼서 승리 기록.
#     for middle in range(n):  # range(n)은 0~n-1. 중간 선수를 한 명씩 허용하는 플로이드-워셜 방식.
#         for first in range(n):  # 출발 선수 순회.
#             if wins[first][middle]:  # first가 middle을 이길 수 있을 때만 전파.
#                 for last in range(n):  # 도착 선수 순회.
#                     if wins[middle][last]:  # middle이 last를 이기면 first도 last보다 강함.
#                         wins[first][last] = True  # 간접적으로 알 수 있는 승패까지 기록.
#     answer = 0  # 순위가 확정되는 선수 수.
#     for player in range(n):  # 각 선수의 비교 가능한 상대 수 확인.
#         known = sum(wins[player][other] or wins[other][player] for other in range(n))  # or는 둘 중 하나라도 참. sum은 True를 1로 세어 승리·패배 중 하나라도 아는 상대 수 합산.
#         if known == n - 1:  # ==는 같음. 자신 이외의 모든 선수와 비교할 수 있어야 순위 확정.
#             answer += 1  # +=는 더해 저장.
#     return answer  # 확정된 선수 수 반환.

# 풀이 요약
# A가 B를 이기고 B가 C를 이기면 A도 C를 이긴다. 이 관계를 전부 전파한 뒤, 나머지 N-1명과 비교 가능한 선수만 센다.
# 예제에서 2번은 세 명에게 지고 5번에게 이겨 4위, 5번은 모두에게 져 5위가 확정된다.
# 순위는 자신보다 강한 선수 수+1이다. 시간 O(N³), 공간 O(N²). N≤100이라 삼중 반복문을 사용해도 된다.
# 