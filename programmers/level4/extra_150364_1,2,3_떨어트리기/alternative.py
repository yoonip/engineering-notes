from itertools import product

def solution(edges, target):
    if sum(target)>10:raise ValueError("목표 합 10 이하의 값 배정 전수 비교용입니다")
    children=[[] for _ in target]
    for a,b in edges:children[a-1].append(b-1)
    for row in children:row.sort()
    pointers=[0]*len(target);destinations=[]
    # 경로는 공에 적는 값과 독립적이다. 길이부터 작은 순서로 비교한다.
    for length in range(1,sum(target)+1):
        node=0
        while children[node]:
            index=pointers[node];pointers[node]=(index+1)%len(children[node]);node=children[node][index]
        destinations.append(node)
        for values in product((1,2,3),repeat=length):
            sums=[0]*len(target)
            for leaf,value in zip(destinations,values):sums[leaf]+=value
            if sums==target:return list(values)
    return [-1]
