def solution(n,info):
    best=(0,[])
    answer=[-1]
    shots=[0]*11
    def assign(index,left):
        nonlocal best,answer
        if index==10:
            shots[index]=left
            difference=sum((10-i) if shots[i]>info[i] else -(10-i) if info[i]>0 else 0 for i in range(10))
            key=(difference,shots[::-1])
            if difference>0 and key>best: best,answer=key,shots[:]
            return
        for used in range(left+1):
            shots[index]=used
            assign(index+1,left-used)
    assign(0,n)
    return answer
