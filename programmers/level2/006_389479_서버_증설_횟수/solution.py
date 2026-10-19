def solution(players, m, k):
    expires = [0] * (len(players) + k)
    active = 0
    answer = 0
    for hour, people in enumerate(players):
        # 이번 시간에 수명이 끝난 서버를 제외한다.
        active -= expires[hour]
        # 이용자 수를 감당하는 데 부족한 서버만 설치한다.
        added = max(0, people // m - active)
        active += added
        answer += added
        # 정확히 k시간 뒤에 설치 수만큼 만료시킨다.
        expires[hour + k] += added
    return answer
