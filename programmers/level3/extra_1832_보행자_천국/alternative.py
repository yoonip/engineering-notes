# 각 칸에 위에서 온 수와 왼쪽에서 온 수를 따로 저장합니다. 직진 전용 칸을 떠날 때 방향을 유지하도록 검사합니다. 1차원
# 압축 전의 명시적 상태입니다.
def solution(m,n,city_map):
    mod=20170805;down=[[0]*n for _ in range(m)];right=[[0]*n for _ in range(m)]
    # 시작점은 첫 이동에 어느 방향이든 선택할 수 있습니다.
    right[0][0]=1
    for r in range(m):
        for c in range(n):
            if city_map[r][c]==1:continue
            total=(down[r][c]+right[r][c])%mod
            if r+1<m and city_map[r+1][c]!=1:
                down[r+1][c]=(down[r+1][c]+(down[r][c] if city_map[r][c]==2 else total))%mod
            if c+1<n and city_map[r][c+1]!=1:
                right[r][c+1]=(right[r][c+1]+(right[r][c] if city_map[r][c]==2 else total))%mod
    return (down[-1][-1]+right[-1][-1])%mod
