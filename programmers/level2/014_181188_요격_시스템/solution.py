# 문제: 요격 시스템
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/181188
# 풀이: 구간 끝이 빠른 순서로 정렬해 끝 바로 왼쪽을 요격한다. 다음 구간이 그 위치를 포함하지 않을 때만 새 요격이 필요하다.
# 복잡도: 구간 N개: 시간 O(N log N), 정렬 추가 공간 O(N). 입력을 정렬한다.

def solution(targets):
    targets.sort(key=lambda target: target[1])
    answer = 0
    end = -1
    for start, stop in targets:
        if start >= end:
            answer += 1
            end = stop
    return answer
