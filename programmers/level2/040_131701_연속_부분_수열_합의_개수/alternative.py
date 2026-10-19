def solution(elements):
    n=len(elements)
    totals=set()
    for length in range(1,n+1):
        current=sum(elements[:length])
        totals.add(current)
        for start in range(1,n):
            current-=elements[start-1]
            current+=elements[(start+length-1)%n]
            totals.add(current)
    return len(totals)
