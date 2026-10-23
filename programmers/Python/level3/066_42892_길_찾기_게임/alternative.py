# 높은 노드부터 x좌표 기준 이진 탐색 트리에 삽입합니다. 단조 스택보다 최악 O(N²)이지만 부모·자식 결정 규칙을 직접
# 구현합니다.
def solution(nodeinfo):
    nodes=sorted([(x,y,i+1) for i,(x,y) in enumerate(nodeinfo)],key=lambda p:(-p[1],p[0]))
    child={i:[None,None] for x,y,i in nodes};xs={i:x for x,y,i in nodes};root=nodes[0][2]
    for x,y,node in nodes[1:]:
        current=root
        while True:
            side=int(x>xs[current])
            if child[current][side] is None:child[current][side]=node;break
            current=child[current][side]
    pre=[];post=[];stack=[(root,False)]
    while stack:
        node,done=stack.pop()
        if done:post.append(node);continue
        pre.append(node);stack.append((node,True))
        for nxt in reversed(child[node]):
            if nxt is not None:stack.append((nxt,False))
    return [pre,post]
