from fractions import Fraction

def solution(m,n,startX,startY,balls):
    answer=[]
    for x,y in balls:
        candidates=[]
        for mx,my,axis,bound in ((-x,y,0,0),(2*m-x,y,0,m),(x,-y,1,0),(x,2*n-y,1,n)):
            origin=(startX,startY)
            mirror=(mx,my)
            t=Fraction(bound-origin[axis],mirror[axis]-origin[axis])
            bounce=(origin[0]+t*(mx-startX),origin[1]+t*(my-startY))
            # 실제 공이 시작점과 반사점 사이에 놓였으면 벽을 맞히기 전에 충돌한다.
            vx,vy=bounce[0]-startX,bounce[1]-startY
            cross=(x-startX)*vy-(y-startY)*vx
            dot=(x-startX)*vx+(y-startY)*vy
            if cross==0 and 0<dot<vx*vx+vy*vy:
                continue
            candidates.append((mx-startX)**2+(my-startY)**2)
        answer.append(min(candidates))
    return answer
