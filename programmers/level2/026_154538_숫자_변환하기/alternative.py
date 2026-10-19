def solution(x,y,n):
    inf=y+1
    dp=[inf]*(y-x+1)
    dp[y-x]=0
    for value in range(y,x-1,-1):
        if dp[value-x]==inf: continue
        previous=[value-n]
        if value%2==0: previous.append(value//2)
        if value%3==0: previous.append(value//3)
        for old in previous:
            if old>=x: dp[old-x]=min(dp[old-x],dp[value-x]+1)
    return dp[0] if dp[0]!=inf else -1
