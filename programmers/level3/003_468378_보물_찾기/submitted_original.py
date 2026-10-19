def solution(depth, money, excavate):
    n = len(depth)
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    choice = [[0] * (n + 1) for _ in range(n)]
    for size in range(1, n + 1):
        for left in range(n - size + 1):
            right = left + size
            best = float('inf')
            for middle in range(left, right):
                cost = depth[middle] + max(dp[left][middle], dp[middle + 1][right])
                if cost < best:
                    best = cost
                    choice[left][right] = middle
            dp[left][right] = best
    left, right = 0, n
    while left < right:
        middle = choice[left][right]
        result = excavate(middle + 1)
        if result == 0:
            return middle + 1
        if result < 0:
            right = middle
        else:
            left = middle + 1
    return 0

# 전체 코드 줄별 설명
# def solution(depth, money, excavate):  # def는 함수 정의. depth는 열별 비용, money는 예산, excavate는 채점기가 제공하는 굴착 함수.
#     n = len(depth)  # len은 원소 개수. 전체 열 수.
#     dp = [[0] * (n + 1) for _ in range(n + 1)]  # 리스트 내포로 독립적인 행 생성. dp[l][r]는 [l,r)에서 반드시 찾기 위한 최소 최악 비용.
#     choice = [[0] * (n + 1) for _ in range(n)]  # []는 리스트. 구간마다 먼저 굴착할 최적의 열 번호 저장.
#     for size in range(1, n + 1):  # range는 끝을 제외. 짧은 구간부터 계산해야 작은 문제의 답을 사용할 수 있음.
#         for left in range(n - size + 1):  # 구간의 왼쪽 끝을 순회하는 for 반복.
#             right = left + size  # 오른쪽 끝은 포함하지 않는 구간 표기.
#             best = float('inf')  # float('inf')는 양의 무한대. 최소값 비교의 초기값.
#             for middle in range(left, right):  # 이번에 굴착할 열의 모든 후보를 순회.
#                 cost = depth[middle] + max(dp[left][middle], dp[middle + 1][right])  # max는 큰 값. 현재 비용에 왼쪽·오른쪽 중 최악의 추가 비용을 더함.
#                 if cost < best:  # if는 조건문, <는 미만. 최악 비용이 더 작은 후보인지 검사.
#                     best = cost  # =는 대입. 현재 최소 비용 저장.
#                     choice[left][right] = middle  # [][]로 행·열 접근. 이 구간의 최적 첫 굴착 위치 저장.
#             dp[left][right] = best  # 모든 후보 중 최소 최악 비용을 DP 표에 기록.
#     left, right = 0, n  # 두 값을 나눠 받는 언패킹. 처음에는 전체 열이 후보.
#     while left < right:  # while은 조건이 참인 동안 반복. 보물이 있을 수 있는 구간을 줄임.
#         middle = choice[left][right]  # 미리 구한 최적 전략에서 굴착할 열을 선택.
#         result = excavate(middle + 1)  # ()는 함수 호출. 채점기는 1부터 세는 열 번호를 받으므로 +1.
#         if result == 0:  # ==는 같음 비교. 0이면 실제 보물을 발굴한 상태.
#             return middle + 1  # return으로 발견한 열 번호를 반환하고 함수 종료.
#         if result < 0:  # 음수이면 보물이 왼쪽에 있음.
#             right = middle  # 현재 열을 제외한 왼쪽 구간으로 축소.
#         else:  # else는 앞 조건이 거짓일 때. 보물이 오른쪽에 있음.
#             left = middle + 1  # 현재 열을 제외한 오른쪽 구간으로 축소.
#     return 0  # 정상 입력에서는 도달하지 않는 방어용 반환.

# 풀이 요약
# 구간 DP로 현재 굴착 비용 + max(왼쪽 최악 비용, 오른쪽 최악 비용)을 최소화하는 열을 정합니다.
# excavate의 방향 응답에 따라 그 전략의 왼쪽·오른쪽 구간으로 이동합니다. 최소 최악 비용 이하로 항상 찾으므로 보장된 money를 넘지 않습니다. 시간 O(N³), 공간 O(N²).
# 예: 비용이 모두 1인 5열은 가운데를 먼저 파고, 응답 방향에서 같은 전략을 반복하면 최대 3번 안에 발굴합니다.
