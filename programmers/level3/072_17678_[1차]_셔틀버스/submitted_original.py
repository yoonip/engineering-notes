def solution(n, t, m, timetable):
    crew = sorted(int(time[:2]) * 60 + int(time[3:]) for time in timetable)
    index = 0
    for trip in range(n):
        departure = 9 * 60 + trip * t
        boarded = 0
        while index < len(crew) and crew[index] <= departure and boarded < m:
            index += 1
            boarded += 1
        if boarded == m:
            answer = crew[index - 1] - 1
        else:
            answer = departure
    hour, minute = divmod(answer, 60)
    return f'{hour:02d}:{minute:02d}'

# 전체 코드 줄별 설명
# def solution(n, t, m, timetable):  # def는 함수 정의. 버스 수·간격·정원·크루 도착 시각 목록을 받음.
#     crew = sorted(int(time[:2]) * 60 + int(time[3:]) for time in timetable)  # [:2]·[3:]는 시·분 문자열 자르기. int는 정수 변환, sorted는 정렬. 시각을 분으로 통일.
#     index = 0  # 아직 버스에 타지 않은 첫 크루의 인덱스.
#     for trip in range(n):  # range(n)은 0~n-1. 버스를 첫 차부터 차례로 운행.
#         departure = 9 * 60 + trip * t  # 09:00부터 t분 간격으로 출발 시각 계산.
#         boarded = 0  # 이번 버스에 탄 크루 수.
#         while index < len(crew) and crew[index] <= departure and boarded < m:  # while은 조건 반복, and는 모두 참. 출발 전 도착한 사람을 정원까지 태움.
#             index += 1  # +=는 더해 저장. 다음 대기 크루를 가리킴.
#             boarded += 1  # 이번 탑승 인원 증가.
#         if boarded == m:  # ==는 같음. 버스가 만석인 경우.
#             answer = crew[index - 1] - 1  # 마지막 탑승 크루보다 1분 먼저 와야 같은 시각에 뒤에 서는 콘이 탈 수 있음.
#         else:  # 빈자리가 있는 경우.
#             answer = departure  # 출발 시각에 도착해도 탑승 가능. 반복이 끝나면 마지막 버스의 결과가 남음.
#     hour, minute = divmod(answer, 60)  # divmod는 몫·나머지 반환. 분 단위를 시·분으로 분리.
#     return f'{hour:02d}:{minute:02d}'  # f문자열의 :02d는 두 자리 정수로 표현하고 앞을 0으로 채움.

# 풀이 요약
# 크루를 도착 순서로 정렬한 뒤 실제 버스 탑승을 시뮬레이션한다. 마지막 버스에 자리가 남으면 출발 시각, 만석이면 마지막 탑승자보다 1분 먼저 도착한다.
# 예: 마지막 버스의 마지막 크루가 09:10이면 콘은 09:09까지 와야 한다. 이전 버스를 앞당겨 타야 하는 경우도 같은 경계 시각으로 처리된다.
# 크루 C명, 버스 N대일 때 시간 O(C log C+N), 공간 O(C). 크루는 한 번만 탑승 처리된다.
# 