# 2016년
# 분류: 누적 일수 / 나머지 연산
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12901
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

def solution(a, b):
    month_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    weekdays = ["FRI", "SAT", "SUN", "MON", "TUE", "WED", "THU"]
    elapsed = sum(month_days[:a - 1]) + b - 1

    return weekdays[elapsed % 7]


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# def solution(a, b):  # def로 함수를 정의합니다. a는 월, b는 일을 받는 매개변수입니다.
#     month_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # 리스트에 1~12월의 일수를 저장합니다. 윤년이므로 2월은 29입니다.
#     weekdays = ["FRI", "SAT", "SUN", "MON", "TUE", "WED", "THU"]  # 요일 문자열 리스트입니다. 기준일이 금요일이므로 0번 값을 FRI로 둡니다.
#     elapsed = sum(month_days[:a - 1]) + b - 1  # [:a-1]은 이전 달들의 슬라이싱, sum()은 그 합입니다. b-1은 이번 달에서 이미 지난 일수입니다.
#
#     return weekdays[elapsed % 7]  # %는 나머지 연산입니다. 0~6 중 하나를 인덱스로 써 요일을 읽고 반환합니다.
#
