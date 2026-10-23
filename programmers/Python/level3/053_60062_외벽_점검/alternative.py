# 원형의 시작점을 고정하고 사용한 친구 집합마다 덮은 가장 먼 취약점 인덱스를 저장합니다. 같은 친구 집합에서는 더 멀리
# 덮은 상태만 남깁니다.
from bisect import bisect_right

def solution(n,weak,dist):
    w=len(weak);f=len(dist);extended=weak+[p+n for p in weak];answer=f+1
    for start in range(w):
        reach={0:start}
        for mask in range(1<<f):
            if mask not in reach:continue
            index=reach[mask]
            if index>=start+w:answer=min(answer,mask.bit_count());continue
            for j,length in enumerate(dist):
                if mask>>j&1:continue
                nxt=bisect_right(extended,extended[index]+length,index,start+w)
                new=mask|1<<j;reach[new]=max(reach.get(new,0),nxt)
    return answer if answer<=f else -1
