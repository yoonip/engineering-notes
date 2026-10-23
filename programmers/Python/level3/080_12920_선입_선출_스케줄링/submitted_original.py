def solution(n, cores):
    count = len(cores)
    if n <= count:
        return n
    left, right = 1, min(cores) * (n - count)
    while left < right:
        middle = (left + right) // 2
        assigned = count + sum(middle // core for core in cores)
        if assigned >= n:
            right = middle
        else:
            left = middle + 1
    time = left
    remaining = n - count - sum((time - 1) // core for core in cores)
    for i, core in enumerate(cores):
        if time % core == 0:
            remaining -= 1
            if remaining == 0:
                return i + 1

# 전체 코드 줄별 설명
# def solution(n, cores):  # def는 함수 정의. 작업 수와 코어별 처리 시간 목록을 받음.
#     count = len(cores)  # len은 코어 수.
#     if n <= count:  # 0시각에는 모든 코어가 비어 있어 코어 번호순으로 바로 작업 배정.
#         return n  # 작업이 코어 수 이하면 마지막 작업의 코어 번호는 n.
#     left, right = 1, min(cores) * (n - count)  # 언패킹 대입. 가장 빠른 코어만 추가 작업을 처리해도 되는 시각을 이분 탐색 상한으로 사용.
#     while left < right:  # while은 조건 반복. n번째 작업이 배정되는 최초 시각 탐색.
#         middle = (left + right) // 2  # //는 정수 나눗셈. 중간 시각.
#         assigned = count + sum(middle // core for core in cores)  # sum은 합계. 0시각의 count개에 각 코어의 재배정 횟수를 더함.
#         if assigned >= n:  # >=는 이상. 이 시각까지 충분한 작업을 시작할 수 있으면 더 이른 시각 탐색.
#             right = middle  # 가능한 시각은 상한으로 남김.
#         else:  # 아직 n번째 작업을 배정할 수 없는 경우.
#             left = middle + 1  # 이 시각 이하를 버리고 더 늦은 구간 탐색.
#     time = left  # n번째 작업이 시작되는 정확한 시각.
#     remaining = n - count - sum((time - 1) // core for core in cores)  # 직전 시각까지 배정한 작업을 빼서 time시각에 몇 번째 빈 코어를 골라야 하는지 계산.
#     for i, core in enumerate(cores):  # enumerate는 인덱스·값 제공. 코어 번호가 작은 순서대로 확인.
#         if time % core == 0:  # %는 나머지, ==는 같음. 처리 시간의 배수 시각에 해당 코어가 비어 다음 작업을 받음.
#             remaining -= 1  # -=는 빼서 저장. 현재 빈 코어에 작업 하나 배정.
#             if remaining == 0:  # 이 코어가 마지막 n번째 작업을 받는지 확인.
#                 return i + 1  # 배열 인덱스는 0부터지만 코어 번호는 1부터라 +1.

# 풀이 요약
# 시간 T까지 시작할 수 있는 작업 수는 코어 수+sum(T//처리 시간)이다. 완료 시각이 아니라 마지막 작업의 배정 시각을 찾는다.
# 예: n=6, [1,2,3]은 0시각 세 개, 1시각 한 개, 2시각 1·2번 코어가 두 개를 받아 마지막은 2번이다.
# 최초 배정 시각 직전의 작업 수를 빼고 동시에 비는 코어를 번호순으로 센다. 코어 C개, 탐색 상한 U일 때 시간 O(C log U), 공간 O(1).
# 