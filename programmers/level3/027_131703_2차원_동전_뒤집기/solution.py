# beginning과 target은 시작·목표 동전 격자.
def solution(beginning, target):
    # 행 수와 열 수를 언패킹.
    n, m = len(beginning), len(beginning[0])
    # ^는 XOR이므로 두 상태가 다르면 1, 같으면 0.
    difference = [[beginning[r][c] ^ target[r][c] for c in range(m)] for r in range(n)]
    # 첫 행을 뒤집지 않는다고 정하면 열별 뒤집기 여부는 이 값으로 확정.
    columns = difference[0][:]
    # 첫 열의 차이를 열 뒤집기로 설명하고 남는 차이가 각 행의 뒤집기 여부.
    rows = [difference[r][0] ^ columns[0] for r in range(n)]
    for r in range(n):
        for c in range(m):
            # 행·열 뒤집기의 XOR이 필요한 변화와 일치하는지 검사.
            if rows[r] ^ columns[c] != difference[r][c]:
                # 첫 행을 반대로 정해도 이 모순은 사라지지 않음.
                return -1
    # 0·1 선택값의 합이 실제 뒤집기 횟수.
    flips = sum(rows) + sum(columns)
    # 모든 행·열의 선택을 동시에 반대로 하면 같은 결과이므로 두 경우 중 최소 반환.
    return min(flips, n + m - flips)
