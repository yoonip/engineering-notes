def solution(a, b):
    month_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    weekdays = ["FRI", "SAT", "SUN", "MON", "TUE", "WED", "THU"]
    elapsed = sum(month_days[:a - 1]) + b - 1

    return weekdays[elapsed % 7]


# 같은 정답 코드 + 줄별 문법 설명
# 아래는 전체가 주석이므로 실행되지 않습니다.

# def solution(a, b):  # def로 함수를 정의합니다. a는 월, b는 일을 받는 매개변수입니다.
#     month_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # 각 달의 일수를 담은 리스트입니다. 윤년이므로 2월은 29일입니다.
#     weekdays = ["FRI", "SAT", "SUN", "MON", "TUE", "WED", "THU"]  # 요일 문자열 리스트입니다. 인덱스 0을 금요일로 둡니다.
#     elapsed = sum(month_days[:a - 1]) + b - 1  # [:a-1]로 이전 달들을 꺼내 sum()으로 더합니다. b-1은 이번 달에서 이미 지난 일수입니다.
#
#     return weekdays[elapsed % 7]  # %는 나머지 연산입니다. 결과 0~6을 인덱스로 사용해 요일을 반환합니다.