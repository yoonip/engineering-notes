# 문제: 혼자 놀기의 달인
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/131130
# 풀이: 서로 겹치지 않는 카드 사이클을 한 번씩 방문한다. 그룹 전체를 정렬하지 않고 가장 큰 두 크기만 갱신한다.
# 복잡도: 카드 N개: 시간 O(N), 추가 공간 O(N). 그룹 전체를 정렬하지 않는다.

def solution(cards):
    visited = [False] * len(cards)
    largest = second = 0
    for start in range(len(cards)):
        if visited[start]:
            continue
        node, size = start, 0
        while not visited[node]:
            visited[node] = True
            size += 1
            node = cards[node] - 1
        if size >= largest:
            largest, second = size, largest
        elif size > second:
            second = size
    return largest * second
