from bisect import bisect_left

def solution(cookie):
    prefix=[0]
    for count in cookie:prefix.append(prefix[-1]+count)
    best=0;n=len(cookie)
    for boundary in range(1,n):
        for left in range(boundary):
            value=prefix[boundary]-prefix[left]
            right=bisect_left(prefix,prefix[boundary]+value,boundary+1)
            if right<=n and prefix[right]-prefix[boundary]==value:best=max(best,value)
    return best
