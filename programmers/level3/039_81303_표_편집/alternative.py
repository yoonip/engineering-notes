# 살아 있는 행은 1, 삭제된 행은 0으로 두고 누적 개수를 관리합니다. 위·아래 이동을 현재 순위의 덧셈으로 바꾸고 해당
# 순위의 원래 행을 찾습니다.
def solution(n,k,cmd):
    bit=[0]+[i&-i for i in range(1,n+1)];deleted=[];alive=['O']*n;total=n
    def prefix(i):
        value=0
        while i:value+=bit[i];i-=i&-i
        return value
    def add(index,delta):
        i=index+1
        while i<=n:bit[i]+=delta;i+=i&-i
    def select(rank):
        index=0;step=1<<(n.bit_length()-1)
        while step:
            nxt=index+step
            if nxt<=n and bit[nxt]<rank:rank-=bit[nxt];index=nxt
            step//=2
        return index
    for command in cmd:
        action=command[0]
        if action in 'UD':
            rank=prefix(k+1)+(int(command[2:]) if action=='D' else -int(command[2:]))
            k=select(rank)
        elif action=='C':
            rank=prefix(k+1);deleted.append(k);alive[k]='X';add(k,-1);total-=1
            k=select(min(rank,total))
        else:
            row=deleted.pop();alive[row]='O';add(row,1);total+=1
    return ''.join(alive)
