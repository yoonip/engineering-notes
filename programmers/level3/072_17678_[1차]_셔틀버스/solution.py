# 버스 수·간격·정원·크루 도착 시각 목록을 받음.
def solution(n, t, m, timetable):
    # 시각을 분으로 통일.
    crew = sorted(int(time[:2]) * 60 + int(time[3:]) for time in timetable)
    # 아직 버스에 타지 않은 첫 크루의 인덱스.
    index = 0
    # 버스를 첫 차부터 차례로 운행.
    for trip in range(n):
        # 09:00부터 t분 간격으로 출발 시각 계산.
        departure = 9 * 60 + trip * t
        # 이번 버스에 탄 크루 수.
        boarded = 0
        # 출발 전 도착한 사람을 정원까지 태움.
        while index < len(crew) and crew[index] <= departure and boarded < m:
            # 다음 대기 크루를 가리킴.
            index += 1
            # 이번 탑승 인원 증가.
            boarded += 1
        # 버스가 만석인 경우.
        if boarded == m:
            # 마지막 탑승 크루보다 1분 먼저 와야 같은 시각에 뒤에 서는 콘이 탈 수 있음.
            answer = crew[index - 1] - 1
        else:
            # 반복이 끝나면 마지막 버스의 결과가 남음.
            answer = departure
    # 분 단위를 시·분으로 분리.
    hour, minute = divmod(answer, 60)
    # f문자열의 :02d는 두 자리 정수로 표현하고 앞을 0으로 채움.
    return f'{hour:02d}:{minute:02d}'
