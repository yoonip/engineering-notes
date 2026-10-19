# 유연근무제
# 분류: 시간 변환 / 시뮬레이션
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/388351
# 선택 이유: 시각을 분으로 바꾼 뒤 평일 기록만 확인하면 59분에서 다음 시각으로 넘어가는 경우도 처리된다.
# 비용: 직원 N명, 기록은 7일 고정: 시간 O(N), 추가 공간 O(1).

def solution(schedules, timelogs, startday):
    answer = 0

    for i in range(len(schedules)):
        scheduled = schedules[i]
        limit = (scheduled // 100) * 60 + scheduled % 100 + 10
        eligible = True

        for day in range(7):
            weekday = (startday + day - 1) % 7 + 1

            if weekday >= 6:
                continue

            arrival = timelogs[i][day]
            arrival_minutes = (arrival // 100) * 60 + arrival % 100

            if arrival_minutes > limit:
                eligible = False
                break

        if eligible:
            answer += 1

    return answer
