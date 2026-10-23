# 남은 카드 위치, 커서, 첫 선택 카드를 상태로 두고 실제 방향키·Ctrl·Enter 한 번씩을 간선으로 탐색합니다.
# 카드쌍 단위 DP와 달리 조작 하나하나를 직접 검증합니다.
# 작은 입력의 비교·검증용입니다. 원래 최대 입력 제출에는 기본 풀이를 사용합니다.
from collections import deque

def solution(board,r,c):
    cards=[value for row in board for value in row]
    mask=sum(1<<i for i,value in enumerate(cards) if value)
    initial=(mask,r*4+c,-1);queue=deque([(initial,0)]);seen={initial}
    while queue:
        (remaining,cursor,opened),cost=queue.popleft()
        if remaining==0:return cost
        candidates=[];row,col=divmod(cursor,4)
        for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
            nr,nc=row+dr,col+dc
            if 0<=nr<4 and 0<=nc<4:candidates.append((remaining,nr*4+nc,opened))
            nr,nc=row,col
            while 0<=nr+dr<4 and 0<=nc+dc<4:
                nr+=dr;nc+=dc
                if remaining&(1<<(nr*4+nc)):break
            candidates.append((remaining,nr*4+nc,opened))
        if remaining&(1<<cursor) and cursor!=opened:
            if opened==-1:candidates.append((remaining,cursor,cursor))
            elif cards[opened]==cards[cursor]:
                candidates.append((remaining^(1<<opened)^(1<<cursor),cursor,-1))
            else:candidates.append((remaining,cursor,-1))
        for nxt in candidates:
            if nxt not in seen:seen.add(nxt);queue.append((nxt,cost+1))
