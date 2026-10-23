def solution(picks,minerals):
    usable = minerals[:sum(picks)*5]
    blocks=[]
    for i in range(0,len(usable),5):
        block=usable[i:i+5]
        d,f,s=(block.count(name) for name in ('diamond','iron','stone'))
        blocks.append((d,f,s))
    blocks.sort(reverse=True)
    left=list(picks)
    answer=0
    for d,f,s in blocks:
        pick=next(i for i,count in enumerate(left) if count)
        left[pick]-=1
        # 다이아 수, 철 수가 큰 묶음부터 배정하면 좋은 곡괭이의 절감 효과가 크다.
        answer += (d+f+s,5*d+f+s,25*d+5*f+s)[pick]
    return answer
