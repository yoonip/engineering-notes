# 길이를 고정해 모든 종류를 포함하는 창이 있는지 검사합니다. 길이를 늘리면 가능성이 유지되므로 이분탐색합니다. 기본 두
# 포인터보다 느리지만 다른 단조 조건을 이용합니다.
def solution(gems):
    kinds=len(set(gems));n=len(gems)
    def find(length):
        counts={}
        for i,gem in enumerate(gems):
            counts[gem]=counts.get(gem,0)+1
            if i>=length:
                old=gems[i-length];counts[old]-=1
                if not counts[old]:del counts[old]
            if i+1>=length and len(counts)==kinds:return i-length+2
        return None
    low,high=1,n
    while low<high:
        mid=(low+high)//2
        if find(mid) is not None:high=mid
        else:low=mid+1
    start=find(low);return [start,start+low-1]
