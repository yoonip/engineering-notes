from itertools import combinations

def solution(a):
    rows,columns=len(a),len(a[0]);mod=10_000_019
    if rows>8:raise ValueError("행 8개 이하의 비트마스크 DP 비교용입니다")
    dp={0:1}
    for column in range(columns):
        ones=sum(a[row][column] for row in range(rows))
        masks=[sum(1<<r for r in choice) for choice in combinations(range(rows),ones)]
        following={}
        for parity,count in dp.items():
            for mask in masks:
                key=parity^mask;following[key]=(following.get(key,0)+count)%mod
        dp=following
    return dp.get(0,0)
