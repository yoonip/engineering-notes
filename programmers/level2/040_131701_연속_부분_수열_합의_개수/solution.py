# 문제: 연속 부분 수열 합의 개수
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/131701
# 풀이: 수열을 두 번 이어 원형 구간을 다룬다. 시작점마다 합을 누적하고 set에 넣어 같은 합은 한 번만 센다.
# 복잡도: 원소 N개: 평균 시간 O(N²), 서로 다른 합 저장 공간 O(N²).

def solution(elements):
    n = len(elements)
    doubled = elements * 2
    sums = set()
    for start in range(n):
        total = 0
        for end in range(start, start + n):
            total += doubled[end]
            sums.add(total)
    return len(sums)
