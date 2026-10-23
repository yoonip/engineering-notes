def solution(k,dungeons):
    n=len(dungeons)
    remaining=[-1]*(1<<n)
    remaining[0]=k
    answer=0
    for mask in range(1<<n):
        if remaining[mask]<0: continue
        answer=max(answer,mask.bit_count())
        for i,(required,cost) in enumerate(dungeons):
            if not mask>>i&1 and remaining[mask]>=required:
                remaining[mask|1<<i]=remaining[mask]-cost
    return answer
