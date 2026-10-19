# 2016년
# 분류: 누적 일수 / 나머지 연산
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12901
# 선택 이유: 2016년은 윤년이므로 월별 일수를 고정해 이전 달의 날짜 수를 더한다.
# 비용: 월은 12개로 고정되어 시간 O(1), 추가 공간 O(1).

def solution(a, b):
    month_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    weekdays = ["FRI", "SAT", "SUN", "MON", "TUE", "WED", "THU"]
    elapsed = sum(month_days[:a - 1]) + b - 1

    return weekdays[elapsed % 7]
