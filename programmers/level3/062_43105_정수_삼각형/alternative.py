# 각 칸으로 들어올 수 있는 두 부모의 최적값을 비교합니다. 아래에서 올라오는 기본 풀이와 달리 마지막 행의 최댓값이 답이
# 됩니다.
def solution(triangle):
    dp=[triangle[0][0]]
    for row in triangle[1:]:
        nxt=[float('-inf')]*len(row)
        for i,value in enumerate(row):
            if i<len(dp):nxt[i]=max(nxt[i],dp[i]+value)
            if i>0:nxt[i]=max(nxt[i],dp[i-1]+value)
        dp=nxt
    return max(dp)
