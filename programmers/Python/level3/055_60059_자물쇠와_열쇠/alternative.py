# 여백이 있는 좌표계에서 겹치는 열쇠 칸을 역산하고 자물쇠 값과의 합이 1인지 검사합니다.
# 확장 배열은 만들지 않으며, 열쇠를 회전할 때 새 배열을 만듭니다.
def solution(key,lock):
    m,n=len(key),len(lock);size=n+2*m
    for _ in range(4):
        for top in range(n+m+1):
            for left in range(n+m+1):
                good=True
                for r in range(n):
                    for c in range(n):
                        kr,kc=r+m-top,c+m-left
                        value=key[kr][kc] if 0<=kr<m and 0<=kc<m else 0
                        if lock[r][c]+value!=1:good=False;break
                    if not good:break
                if good:return True
        key=[list(row) for row in zip(*key[::-1])]
    return False
