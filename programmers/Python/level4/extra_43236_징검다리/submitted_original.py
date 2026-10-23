def solution(distance, rocks, n):
    positions = sorted(rocks) + [distance]
    low, high = 1, distance
    answer = 0
    while low <= high:
        gap = (low + high) // 2
        previous = 0
        removed = 0
        for position in positions:
            if position - previous < gap:
                removed += 1
            else:
                previous = position
            if removed > n:
                break
        if removed <= n:
            answer = gap
            low = gap + 1
        else:
            high = gap - 1
    return answer

# 전체 코드 줄별 설명
# def solution(distance, rocks, n):  # def는 함수 정의. 전체 거리·바위 위치·제거할 개수를 입력받음.
#     positions = sorted(rocks) + [distance]  # sorted는 새 정렬 리스트 생성. +로 고정 도착점도 마지막 간격 검사에 포함.
#     low, high = 1, distance  # 최소 간격의 가능한 탐색 범위를 1부터 전체 거리로 초기화.
#     answer = 0  # 지금까지 확인한 가능한 최대 최소 간격.
#     while low <= high:  # while은 조건이 참인 동안 반복. 이진 탐색 범위가 남아 있으면 실행.
#         gap = (low + high) // 2  # //는 정수 나눗셈. 검사할 최소 간격 후보 선택.
#         previous = 0  # 마지막으로 남긴 지점은 출발점 0.
#         removed = 0  # 최소 간격을 유지하기 위해 제거한 바위 수 초기화.
#         for position in positions:  # 앞에서부터 바위와 도착점 순회.
#             if position - previous < gap:  # if는 조건문. 마지막 남긴 지점과 너무 가까우면 제거 필요.
#                 removed += 1  # +=는 더한 값 저장. 도착점에서 부족하면 직전 바위를 제거한 것으로 계산 가능.
#             else:  # else는 필요한 간격 이상 떨어진 경우.
#                 previous = position  # 현재 바위를 남기고 기준 위치로 갱신.
#             if removed > n:  # 허용 제거 개수를 초과했는지 확인.
#                 break  # break로 불가능한 후보의 검사를 일찍 종료.
#         if removed <= n:  # 이 간격이 최대 n개 제거로 가능하면 실행.
#             answer = gap  # 가능한 최솟값의 최댓값 후보 저장.
#             low = gap + 1  # 더 큰 간격이 가능한지 오른쪽 절반 탐색.
#         else:  # 너무 많은 바위 제거가 필요한 경우.
#             high = gap - 1  # 간격을 줄여 왼쪽 절반 탐색.
#     return answer  # return으로 제거 후 최소 간격의 가능한 최댓값 반환.

# 풀이 요약
# 최소 간격이 x 이상인지 검사할 때, 앞에서부터 너무 가까운 바위만 제거하면 필요한 최소 제거 개수를 얻습니다. 가능 여부는 x가 커질수록 어려워져 이진 탐색할 수 있습니다.
# 도착점은 실제로 제거하지 않습니다. 마지막 간격이 짧으면 직전 바위를 제거해 두 간격을 합친 것으로 같은 개수를 셉니다.
# 예제는 2·14 위치를 제거해 최소 간격 4. 바위 수 R, 거리 D에 대해 시간 O(R*log R+R*log D), 공간 O(R).
# 