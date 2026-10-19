from heapq import nlargest

def solution(cards):
    parent=list(range(len(cards)))
    size=[1]*len(cards)
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]
            x=parent[x]
        return x
    for i,card in enumerate(cards):
        a,b=find(i),find(card-1)
        if a!=b:
            if size[a]<size[b]: a,b=b,a
            parent[b]=a
            size[a]+=size[b]
    largest=nlargest(2,[size[i] for i in range(len(cards)) if parent[i]==i]+[0,0])
    return largest[0]*largest[1]
