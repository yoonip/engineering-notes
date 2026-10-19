# 목표에서 거꾸로 정확히 몇 걸음에 도달할 수 있는지 표를 만듭니다. 이 표를 보고 사전순으로 경로를 복원합니다. 맨해튼
# 거리·짝수 성질을 쓰지 않는 독립 비교 방법입니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
def solution(n,m,x,y,r,c,k):
    layers=[{(r,c)}]
    directions=(('d',1,0),('l',0,-1),('r',0,1),('u',-1,0))
    for _ in range(k):
        layers.append({(a+da,b+db) for a,b in layers[-1] for _,da,db in directions
                       if 1<=a+da<=n and 1<=b+db<=m})
    if (x,y) not in layers[k]: return 'impossible'
    answer=[]
    for remaining in range(k-1,-1,-1):
        for letter,da,db in directions:
            if (x+da,y+db) in layers[remaining]:
                x+=da;y+=db;answer.append(letter);break
    return ''.join(answer)
