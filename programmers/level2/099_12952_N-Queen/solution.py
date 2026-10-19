# 문제: N-Queen
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/12952
# 풀이: 열과 두 대각선의 공격 범위를 비트마스크로 관리한다. 다음 행에서 가능한 열만 꺼내 백트래킹한다.
# 복잡도: 보드 한 변 N: 탐색 시간 상한 O(N!), 재귀 추가 공간 O(N). 큰 정수 비트 비용은 별도다.

def solution(n):
    full = (1 << n) - 1
    def search(columns, left, right):
        if columns == full:
            return 1
        available = full & ~(columns | left | right)
        count = 0
        while available:
            position = available & -available
            available -= position
            count += search(columns | position, (left | position) << 1, (right | position) >> 1)
        return count
    return search(0, 0, 0)
