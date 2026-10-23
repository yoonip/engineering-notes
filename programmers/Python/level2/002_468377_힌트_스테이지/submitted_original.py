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

# 전체 코드 줄별 설명 (아래는 모두 실행되지 않는 주석입니다.)
# def solution(cost, hint):  # def는 함수 정의, cost·hint는 입력 매개변수, : 아래 들여쓰기는 함수 본문.
#     n = len(cost)  # len(cost)로 단계 수를 구함. len은 원소 개수를 반환하는 내장 함수.
#     tickets = [0] * n  # [0]은 리스트, * n은 n번 반복. 단계별 티켓 수를 0으로 초기화.
#     answer = sum(row[0] for row in cost)  # row[0]은 첫 칸. for 표현식이 각 단계의 기본 비용을 만들고 sum이 합산.
#
#     def dfs(stage, total):  # def로 단계와 누적 비용을 받는 중첩 재귀 함수를 정의.
#         nonlocal answer  # nonlocal은 바깥 solution의 answer에 새 값을 대입하도록 지정.
#         total += cost[stage][min(tickets[stage], n - 1)]  # [][]는 행·열 접근. min은 작은 값 선택, +=는 비용을 더해 다시 저장.
#         if stage == n - 1:  # if는 조건문, ==는 같음 비교. 마지막 단계인지 확인.
#             answer = min(answer, total)  # min(answer,total)로 지금까지 찾은 최소 비용을 갱신.
#             return  # return은 현재 dfs 호출을 종료. 값이 없으면 None 반환.
#
#         dfs(stage + 1, total)  # 함수 이름 뒤 ()는 호출. 힌트를 사지 않고 다음 단계로 진행.
#         bundle = hint[stage]  # hint[stage]는 이번 단계의 힌트 묶음.
#         for number in bundle[1:]:  # for는 순회. [1:]은 첫 항목(가격)을 제외한 나머지의 슬라이스.
#             tickets[number - 1] += 1  # 번호는 1부터이므로 -1로 인덱스 변환. += 1로 티켓 추가.
#         dfs(stage + 1, total + bundle[0])  # 묶음 가격 bundle[0]을 더하고 다음 단계의 dfs를 호출.
#         for number in bundle[1:]:  # 앞서 지급한 티켓 목록을 다시 순회.
#             tickets[number - 1] -= 1  # -= 1은 1을 빼서 저장. 이전 상태로 복구하는 백트래킹.
#
#     dfs(0, 0)  # 0번 단계, 누적 비용 0으로 탐색 시작.
#     return answer  # return으로 최소 비용을 채점기에 반환.

# 풀이 요약
# 각 단계에서 힌트 구매/미구매를 DFS(깊이 우선 탐색)로 비교합니다.
# 티켓은 다음 단계에 적용하고, 탐색 후 되돌립니다. 모든 선택 중 최소 비용을 반환합니다.
# 예: 티켓이 0장이면 cost[i][0], 1장이면 cost[i][1]의 비용을 냅니다.
