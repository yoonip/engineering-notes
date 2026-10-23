# 방문 가능한 자식 목록을 상태에 함께 넘깁니다. 방문 집합을 캐시하는 기본 풀이보다 같은 집합을 여러 순서로 방문할 수
# 있지만 후보 확장 과정이 직접 드러납니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
def solution(info,edges):
    children=[[] for _ in info]
    for a,b in edges:children[a].append(b)
    def visit(sheep,wolves,available):
        answer=sheep
        for node in available:
            s=sheep+(info[node]==0);w=wolves+(info[node]==1)
            if s<=w:continue
            nxt=(available-{node})|set(children[node])
            answer=max(answer,visit(s,w,nxt))
        return answer
    return visit(1,0,set(children[0]))
