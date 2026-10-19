# 자물쇠 주변에 여백을 만들고 회전한 열쇠를 실제로 더합니다. 자물쇠 영역의 모든 합이 정확히 1인지 검사합니다. 좌표 집합
# 비교와 독립된 배열 구현입니다.
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
