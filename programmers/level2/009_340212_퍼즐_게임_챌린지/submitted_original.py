def solution(diffs, times, limit):
    left = 1
    right = max(diffs)
    while left < right:
        level = (left + right) // 2
        elapsed = 0
        previous = 0
        for diff, current in zip(diffs, times):
            elapsed += current
            if diff > level:
                elapsed += (diff - level) * (current + previous)
            if elapsed > limit:
                break
            previous = current
        if elapsed <= limit:
            right = level
        else:
            left = level + 1
    return left

# 전체 코드 줄별 설명 (아래는 모두 실행되지 않는 주석입니다.)
# def solution(diffs, times, limit):  # def는 함수 정의. diffs,times,limit는 입력 매개변수, : 아래 들여쓰기는 함수 본문.
#     left = 1  # 양의 정수 숙련도 하한을 1로 설정. =는 대입.
#     right = max(diffs)  # max는 최댓값을 구하는 내장 함수. 모든 난이도 이상이면 실패하지 않으므로 상한으로 사용.
#     while left < right:  # while은 조건 반복, <는 미만. 탐색 구간이 한 값으로 줄 때까지 반복.
#         level = (left + right) // 2  # ()는 계산 묶음, //는 몫 내림. 중간 정수 숙련도 계산.
#         elapsed = 0  # 이번 숙련도의 누적 시간을 0으로 초기화.
#         previous = 0  # 이전 퍼즐의 기본 시간 초기화. 첫 퍼즐은 난이도1이라 실패하지 않음.
#         for diff, current in zip(diffs, times):  # zip은 같은 위치의 난이도·시간을 묶음. for로 순회하며 쉼표로 두 값을 언패킹.
#             elapsed += current  # +=는 더해서 저장. 마지막 성공 시도 시간 추가.
#             if diff > level:  # if는 조건문, >는 초과 비교. 숙련도보다 어려운 경우.
#                 elapsed += (diff - level) * (current + previous)  # 실패 횟수*(현재+이전 기본 시간)을 추가. 괄호는 계산 묶음, *는 곱셈.
#             if elapsed > limit:  # 이미 제한을 초과했는지 확인. 뒤의 시간도 양수이므로 조기 종료 가능.
#                 break  # break로 가장 가까운 for 반복 종료.
#             previous = current  # 다음 퍼즐을 위해 현재 기본 시간을 이전 시간으로 저장.
#         if elapsed <= limit:  # <=는 이하. 정확히 제한 시간과 같은 경우도 성공.
#             right = level  # 가능한 중간값을 남기고 상한 축소.
#         else:  # else는 앞 if가 거짓일 때 실행.
#             left = level + 1  # 불가능한 중간값 이하는 버리고 하한을 level+1로 설정.
#     return left  # return으로 최소 가능 숙련도 반환.

# 풀이 요약
# 퍼즐 시간은 current+max(0,diff-level)*(current+previous)입니다. 숙련도가 높아질수록 시간은 줄거나 같습니다.
# 이 단조성을 이용해 제한 시간 안에 가능한 최소 숙련도를 이진 탐색합니다. 시간 O(n log 최대 난이도), 추가 공간 O(1).
# 예: [1,5,3], [2,4,7], 제한30에서 숙련도2는42, 3은25이므로 최소3입니다.
