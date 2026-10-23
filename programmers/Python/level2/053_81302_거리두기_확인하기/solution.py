from itertools import combinations

def solution(places):
    def valid(room):
        people = [(r, c) for r in range(5) for c in range(5) if room[r][c] == 'P']
        for (r1, c1), (r2, c2) in combinations(people, 2):
            distance = abs(r1 - r2) + abs(c1 - c2)
            # 바로 이웃한 응시자는 무조건 위반이다.
            if distance == 1:
                return 0
            if distance == 2:
                if r1 == r2:
                    if room[r1][(c1 + c2) // 2] != 'X':
                        return 0
                elif c1 == c2:
                    if room[(r1 + r2) // 2][c1] != 'X':
                        return 0
                # 대각선은 두 짧은 경로를 모두 파티션으로 막아야 한다.
                elif room[r1][c2] != 'X' or room[r2][c1] != 'X':
                    return 0
        return 1
    return [valid(room) for room in places]
