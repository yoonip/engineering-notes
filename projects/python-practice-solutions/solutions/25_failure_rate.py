# 실패율
# 분류: 빈도 집계 / 정렬
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/42889
# 선택 이유: 스테이지별 인원을 한 번 센 뒤 도달 인원을 누적해서 줄인다. 매 스테이지마다 전체 인원을 다시 세지 않는다.
# 비용: 사용자 P명, 스테이지 N개: 시간 O(P+N log N), 추가 공간 O(N).

def solution(N, stages):
    counts = [0] * (N + 2)
    for stage in stages:
        counts[stage] += 1

    reached = len(stages)
    rates = []

    for stage in range(1, N + 1):
        if reached == 0:
            rate = 0
        else:
            rate = counts[stage] / reached

        rates.append((stage, rate))
        reached -= counts[stage]

    rates.sort(key=lambda item: (-item[1], item[0]))
    return [item[0] for item in rates]
