# 문제: 거리두기 확인하기
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/81302
# 풀이: 사람 쌍의 맨해튼 거리가 1이면 위반이다. 거리가 2이면 중간 경로를 파티션이 모두 막았는지 확인한다.
# 복잡도: 방 R개·방당 사람 최대 P명: 시간 O(RP²), 추가 공간 O(P). 방은 5×5다.

from itertools import combinations

def solution(places):
    def valid(room):
        people = [(r, c) for r in range(5) for c in range(5) if room[r][c] == 'P']
        for (r1, c1), (r2, c2) in combinations(people, 2):
            distance = abs(r1 - r2) + abs(c1 - c2)
            if distance == 1:
                return 0
            if distance == 2:
                if r1 == r2:
                    if room[r1][(c1 + c2) // 2] != 'X':
                        return 0
                elif c1 == c2:
                    if room[(r1 + r2) // 2][c1] != 'X':
                        return 0
                elif room[r1][c2] != 'X' or room[r2][c1] != 'X':
                    return 0
        return 1
    return [valid(room) for room in places]
