# 작은 격자의 모든 시작점을 움직여 목표에 도착한 수를 셉니다. 벽에서 좌표가 합쳐지는 역연산을 실제 이동과 대조합니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
def solution(n,m,x,y,queries):
    count=0
    for row in range(n):
        for col in range(m):
            r,c=row,col
            for command,distance in queries:
                if command==0:c=max(0,c-distance)
                elif command==1:c=min(m-1,c+distance)
                elif command==2:r=max(0,r-distance)
                else:r=min(n-1,r+distance)
            count+=(r,c)==(x,y)
    return count
