from decimal import Decimal

def solution(lines):
    intervals = []
    for line in lines:
        date, clock, duration = line.split()
        hour, minute, second = clock.split(':')
        end = (int(hour) * 3600 + int(minute) * 60) * 1000 + int(Decimal(second) * 1000)
        length = int(Decimal(duration[:-1]) * 1000)
        start = end - length + 1
        intervals.append((start, end))
    answer = 0
    for _, time in intervals:
        count = sum(start <= time + 999 and end >= time for start, end in intervals)
        answer = max(answer, count)
    return answer

# 전체 코드 줄별 설명
# from decimal import Decimal  # import는 도구 가져오기. Decimal은 문자열의 십진수를 정확하게 계산하는 자료형. 이진 실수의 소수 오차 방지.
# 
# def solution(lines):  # def는 함수 정의. 요청 완료 시각·처리 시간이 기록된 로그 목록을 받음.
#     intervals = []  # []는 리스트. 각 요청의 [시작,종료] 밀리초 구간을 저장.
#     for line in lines:  # for로 로그를 하나씩 처리.
#         date, clock, duration = line.split()  # split은 공백으로 문자열 나누기. 세 값을 언패킹. 날짜는 모두 같음.
#         hour, minute, second = clock.split(':')  # 시:분:초 문자열을 분리.
#         end = (int(hour) * 3600 + int(minute) * 60) * 1000 + int(Decimal(second) * 1000)  # int는 정수 변환. 완료 시각을 정확한 밀리초 정수로 계산.
#         length = int(Decimal(duration[:-1]) * 1000)  # [:-1]은 끝의 s 제거. 처리 시간을 밀리초로 변환.
#         start = end - length + 1  # 양 끝을 포함하므로 +1. 예: 종료 10ms·기간 3ms면 시작은 8ms.
#         intervals.append((start, end))  # append는 끝에 추가, ()는 두 값을 묶는 튜플.
#     answer = 0  # 1초 구간 안 최대 처리량.
#     for _, time in intervals:  # 각 요청의 종료 시각을 1초 구간 시작 후보로 사용. _는 쓰지 않는 시작 시각.
#         count = sum(start <= time + 999 and end >= time for start, end in intervals)  # and는 모두 참, sum은 True를 1로 합산. [time,time+999]와 겹치는 요청 수 계산.
#         answer = max(answer, count)  # max는 최댓값. 후보별 최대 처리량 갱신.
#     return answer  # 최대 처리량 반환.

# 풀이 요약
# 각 요청을 양 끝 포함 정수 밀리초 구간으로 바꾸고, 어떤 요청의 종료 시각부터 시작하는 1000ms 창과 겹치는 요청 수를 센다.
# 임의의 최적 창도 겹치는 요청 중 가장 이른 종료 시각까지 오른쪽으로 밀어 요청을 잃지 않을 수 있어 종료 시각만 검사하면 충분하다.
# 창의 끝은 시작+1000이 아니라 시작+999다. 예제 1·2의 1ms 차이로 답이 1·2로 달라진다. 시간 O(N²), 공간 O(N).
# 