def solution(queue1,queue2):
    values=queue1+queue2
    n=len(values)
    target=sum(values)
    if target%2: return -1
    target//=2
    left,right=0,len(queue1)
    current=sum(queue1)
    for moves in range(2*n+1):
        if current==target: return moves
        if current>target:
            current-=values[left%n]
            left+=1
        else:
            current+=values[right%n]
            right+=1
    return -1
