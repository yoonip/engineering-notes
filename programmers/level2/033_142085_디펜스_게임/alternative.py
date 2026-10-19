def solution(n,k,enemy):
    def possible(count):
        ordered=sorted(enemy[:count])
        return sum(ordered[:max(0,count-k)])<=n
    low,high=0,len(enemy)
    while low<high:
        mid=(low+high+1)//2
        if possible(mid): low=mid
        else: high=mid-1
    return low
