# 시:분:초 문자열을 초 단위 정수로 변환.
def seconds(text):
    # 세 변수로 언패킹.
    hour, minute, second = map(int, text.split(':'))
    # 시간·분을 초로 바꿔 합산.
    return hour * 3600 + minute * 60 + second

# 영상 길이·광고 길이·시청 기록을 받는 정답 함수.
def solution(play_time, adv_time, logs):
    # 두 길이를 초로 변환.
    play, adv = seconds(play_time), seconds(adv_time)
    # 시청자 수가 변하는 지점만 표시하는 차분 배열.
    difference = [0] * (play + 1)
    # for로 시청 기록 순회.
    for log in logs:
        # 시작·종료 문자열을 분리하고 각각 초로 변환.
        start, end = map(seconds, log.split('-'))
        # 시작 초부터 시청자 1명 증가.
        difference[start] += 1
        # 종료 시각은 시청 구간에 포함하지 않음.
        difference[end] -= 1
    # prefix[t]는 0초부터 t초 직전까지의 누적 시청 시간.
    prefix = [0] * (play + 1)
    # 현재 초의 시청자 수.
    viewers = 0
    # range(play)는 0부터 play-1까지 반복.
    for time in range(play):
        # 차분을 누적해 현재 시청자 수 복원.
        viewers += difference[time]
        # 시청자 수를 다시 누적해 구간 합 계산 준비.
        prefix[time + 1] = prefix[time] + viewers
    # 가장 빠른 최적 시작 시각과 최대 누적 시청 시간 초기화.
    best_start, best_total = 0, -1
    # 광고가 영상 끝을 넘지 않는 모든 시작 초를 빠른 순서로 확인.
    for start in range(play - adv + 1):
        # 누적 합 두 개의 차이로 광고 구간의 시청 시간 계산.
        total = prefix[start + adv] - prefix[start]
        # 같은 값이면 갱신하지 않아 더 이른 시각 유지.
        if total > best_total:
            # 언패킹 대입으로 최적값 갱신.
            best_start, best_total = start, total
    # 시간과 남은 초 분리.
    hour, rest = divmod(best_start, 3600)
    # 나머지를 분·초로 분리.
    minute, second = divmod(rest, 60)
    # f문자열의 :02d는 두 자리 정수로 표시하고 앞을 0으로 채움.
    return f'{hour:02d}:{minute:02d}:{second:02d}'
