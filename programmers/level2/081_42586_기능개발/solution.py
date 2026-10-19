# 문제: 기능개발
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/42586
# 풀이: 완료 일수를 올림 계산한다. 앞 기능의 배포일 이하에 끝난 기능을 같은 묶음으로 합쳐 날짜별 시뮬레이션을 피한다.
# 복잡도: 작업 N개: 시간 O(N), 반환 배열 외 추가 공간 O(1).

def solution(progresses, speeds):
    answer = []
    release_day = 0
    for progress, speed in zip(progresses, speeds):
        days = (100 - progress + speed - 1) // speed
        if days > release_day:
            answer.append(1)
            release_day = days
        else:
            answer[-1] += 1
    return answer
