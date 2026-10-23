# 이진 실수의 소수 오차 방지.
from decimal import Decimal

# 요청 완료 시각·처리 시간이 기록된 로그 목록을 받음.
def solution(lines):
    # 각 요청의 [시작,종료] 밀리초 구간을 저장.
    intervals = []
    # for로 로그를 하나씩 처리.
    for line in lines:
        # 날짜는 모두 같음.
        date, clock, duration = line.split()
        # 시:분:초 문자열을 분리.
        hour, minute, second = clock.split(':')
        # 완료 시각을 정확한 밀리초 정수로 계산.
        end = (int(hour) * 3600 + int(minute) * 60) * 1000 + int(Decimal(second) * 1000)
        # 처리 시간을 밀리초로 변환.
        length = int(Decimal(duration[:-1]) * 1000)
        # 예: 종료 10ms·기간 3ms면 시작은 8ms.
        start = end - length + 1
        # append는 끝에 추가, ()는 두 값을 묶는 튜플.
        intervals.append((start, end))
    # 1초 구간 안 최대 처리량.
    answer = 0
    # _는 쓰지 않는 시작 시각.
    for _, time in intervals:
        # [time,time+999]와 겹치는 요청 수 계산.
        count = sum(start <= time + 999 and end >= time for start, end in intervals)
        # 후보별 최대 처리량 갱신.
        answer = max(answer, count)
    # 최대 처리량 반환.
    return answer
