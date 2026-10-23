def solution(people, limit):
    people.sort()
    left, right = 0, len(people) - 1
    answer = 0
    while left <= right:
        if left < right and people[left] + people[right] <= limit:
            left += 1
        right -= 1
        answer += 1
    return answer

# 전체 코드 줄별 설명
# def solution(people, limit):  # def는 함수 정의. 사람 무게 목록·보트 제한 입력.
#     people.sort()  # sort는 리스트를 제자리 오름차순 정렬.
#     left, right = 0, len(people) - 1  # len은 길이. 가장 가벼운·무거운 사람 인덱스 초기화.
#     answer = 0  # =는 대입. 보트 수 초기화.
#     while left <= right:  # while은 반복, <=는 이하. 남은 사람이 있는 동안 진행.
#         if left < right and people[left] + people[right] <= limit:  # and는 둘 다 참. 서로 다른 두 사람의 합이 제한 이하면 동승.
#             left += 1  # +=는 더해 저장. 가벼운 사람도 보트에 태워 제외.
#         right -= 1  # -=는 빼서 저장. 가장 무거운 사람은 항상 이번 보트에 태움.
#         answer += 1  # 보트 한 개 사용.
#     return answer  # return으로 최소 보트 수 반환.

# 풀이 요약
# 가장 무거운 사람은 보트 하나가 필요합니다. 가장 가벼운 사람과 탈 수 있으면 함께, 안 되면 누구와도 못 타므로 혼자 보냅니다.
# 예: [70,50,80,50],100은 80·70 단독과 50+50으로 3대. 시간 O(N log N), 정렬 공간 O(N).
