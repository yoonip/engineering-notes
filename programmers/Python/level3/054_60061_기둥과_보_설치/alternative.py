# 구조물 하나를 임시로 추가·삭제한 뒤 그 변화의 영향을 받을 수 있는 주변 기둥·보만 검사합니다. 전체 구조물을 다시
# 확인하는 기본 풀이보다 검사가 작아집니다.
def solution(n,build_frame):
    structures=set()
    def valid(x,y,t):
        if t==0:return y==0 or (x,y-1,0) in structures or (x-1,y,1) in structures or (x,y,1) in structures
        return (x,y-1,0) in structures or (x+1,y-1,0) in structures or ((x-1,y,1) in structures and (x+1,y,1) in structures)
    for x,y,t,action in build_frame:
        item=(x,y,t)
        if action:structures.add(item)
        else:structures.remove(item)
        affected=[(a,b,k) for a in range(x-1,x+2) for b in range(y-1,y+2) for k in (0,1)]
        if any(s in structures and not valid(*s) for s in affected):
            if action:structures.remove(item)
            else:structures.add(item)
    return [list(s) for s in sorted(structures)]
