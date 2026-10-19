# 각 스킬의 직사각형을 실제로 모두 갱신합니다. 중간 내구도가 음수여도 회복을 계속 적용합니다. 작은 보드에서 차분 배열의
# 경계 부호를 검증하는 기준입니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
def solution(board,skill):
    grid=[row[:] for row in board]
    for kind,r1,c1,r2,c2,degree in skill:
        delta=degree if kind==2 else -degree
        for r in range(r1,r2+1):
            for c in range(c1,c2+1):grid[r][c]+=delta
    return sum(value>0 for row in grid for value in row)
