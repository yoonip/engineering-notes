def solution(n, times):
    left, right = 0, min(times) * n
    while left < right:
        middle = (left + right) // 2
        completed = 0
        for time in times:
            completed += middle // time
            if completed >= n:
                break
        if completed >= n:
            right = middle
        else:
            left = middle + 1
    return left

# 전체 코드 줄별 설명
# def solution(n, times):  # def는 함수 정의. 사람 수와 심사관별 한 사람 처리 시간을 받음.
#     left, right = 0, min(times) * n  # min은 최솟값. 가장 빠른 심사관 혼자 전부 처리하는 시간을 가능한 상한으로 사용.
#     while left < right:  # while은 조건이 참인 동안 반복. 가능한 최소 시간을 찾는 이분 탐색.
#         middle = (left + right) // 2  # ()는 계산 우선순위, //는 정수 나눗셈. 탐색 범위의 중간 시간.
#         completed = 0  # middle 시간까지 심사를 마칠 수 있는 사람 수.
#         for time in times:  # for로 심사관의 처리 시간을 순회.
#             completed += middle // time  # +=는 더해 저장. 각 심사관이 해당 시간 내 완료할 수 있는 인원 합산.
#             if completed >= n:  # >=는 이상. 필요한 인원에 도달하면 나머지 심사관은 확인할 필요 없음.
#                 break  # for 반복 종료.
#         if completed >= n:  # 중간 시간이 충분한 경우.
#             right = middle  # 더 작은 시간도 가능한지 왼쪽 범위 탐색.
#         else:  # 시간이 부족한 경우.
#             left = middle + 1  # middle 이하는 불가능하므로 다음 시간부터 탐색.
#     return left  # 두 경계가 만나는 최소 가능 시간 반환.

# 풀이 요약
# 시간 T에 완료할 수 있는 인원은 sum(T//time)이다. 시간이 늘면 처리 인원은 줄지 않으므로 가능 여부를 이분 탐색한다.
# 예: 28분에는 28//7+28//10=4+2=6명, 27분에는 3+2=5명이므로 정답 28.
# 심사관 수 M, 상한 U=n·min(times)일 때 시간 O(M log U), 공간 O(1).
# 