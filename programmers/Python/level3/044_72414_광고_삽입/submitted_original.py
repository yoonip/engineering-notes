def seconds(text):
    hour, minute, second = map(int, text.split(':'))
    return hour * 3600 + minute * 60 + second

def solution(play_time, adv_time, logs):
    play, adv = seconds(play_time), seconds(adv_time)
    difference = [0] * (play + 1)
    for log in logs:
        start, end = map(seconds, log.split('-'))
        difference[start] += 1
        difference[end] -= 1
    prefix = [0] * (play + 1)
    viewers = 0
    for time in range(play):
        viewers += difference[time]
        prefix[time + 1] = prefix[time] + viewers
    best_start, best_total = 0, -1
    for start in range(play - adv + 1):
        total = prefix[start + adv] - prefix[start]
        if total > best_total:
            best_start, best_total = start, total
    hour, rest = divmod(best_start, 3600)
    minute, second = divmod(rest, 60)
    return f'{hour:02d}:{minute:02d}:{second:02d}'

# 전체 코드 줄별 설명
# def seconds(text):  # def는 함수 정의. 시:분:초 문자열을 초 단위 정수로 변환.
#     hour, minute, second = map(int, text.split(':'))  # split은 구분자로 나누기, map은 각 값에 int 정수 변환 적용. 세 변수로 언패킹.
#     return hour * 3600 + minute * 60 + second  # 시간·분을 초로 바꿔 합산.
# 
# def solution(play_time, adv_time, logs):  # 영상 길이·광고 길이·시청 기록을 받는 정답 함수.
#     play, adv = seconds(play_time), seconds(adv_time)  # 함수 호출 괄호 (). 두 길이를 초로 변환.
#     difference = [0] * (play + 1)  # []는 리스트, *는 반복. 시청자 수가 변하는 지점만 표시하는 차분 배열.
#     for log in logs:  # for로 시청 기록 순회.
#         start, end = map(seconds, log.split('-'))  # 시작·종료 문자열을 분리하고 각각 초로 변환.
#         difference[start] += 1  # +=는 더해 저장. 시작 초부터 시청자 1명 증가.
#         difference[end] -= 1  # -=는 빼서 저장. 종료 시각은 시청 구간에 포함하지 않음.
#     prefix = [0] * (play + 1)  # prefix[t]는 0초부터 t초 직전까지의 누적 시청 시간.
#     viewers = 0  # 현재 초의 시청자 수.
#     for time in range(play):  # range(play)는 0부터 play-1까지 반복.
#         viewers += difference[time]  # 차분을 누적해 현재 시청자 수 복원.
#         prefix[time + 1] = prefix[time] + viewers  # []로 인덱스 조회. 시청자 수를 다시 누적해 구간 합 계산 준비.
#     best_start, best_total = 0, -1  # 가장 빠른 최적 시작 시각과 최대 누적 시청 시간 초기화.
#     for start in range(play - adv + 1):  # 광고가 영상 끝을 넘지 않는 모든 시작 초를 빠른 순서로 확인.
#         total = prefix[start + adv] - prefix[start]  # 누적 합 두 개의 차이로 광고 구간의 시청 시간 계산.
#         if total > best_total:  # >는 초과. 같은 값이면 갱신하지 않아 더 이른 시각 유지.
#             best_start, best_total = start, total  # 언패킹 대입으로 최적값 갱신.
#     hour, rest = divmod(best_start, 3600)  # divmod는 몫·나머지 반환. 시간과 남은 초 분리.
#     minute, second = divmod(rest, 60)  # 나머지를 분·초로 분리.
#     return f'{hour:02d}:{minute:02d}:{second:02d}'  # f문자열의 :02d는 두 자리 정수로 표시하고 앞을 0으로 채움.

# 풀이 요약
# 차분 배열로 초별 시청자 수를 만든 후, 누적 합으로 광고 길이만큼의 구간 합을 모두 비교한다.
# 예: 광고 구간 [start,end)의 시청 시간은 prefix[end]-prefix[start]. 동점이면 먼저 찾은 시작 시각을 유지한다.
# 시간 O(시청 기록 수 + 영상의 초 수), 공간 O(영상의 초 수). 최대 영상 길이는 359999초라 초 단위 계산이 가능하다.
# 