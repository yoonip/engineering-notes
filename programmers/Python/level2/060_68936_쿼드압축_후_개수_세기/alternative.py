def solution(arr):
    n=len(arr)
    prefix=[[0]*(n+1) for _ in range(n+1)]
    for r in range(n):
        running=0
        for c in range(n):
            running+=arr[r][c]
            prefix[r+1][c+1]=prefix[r][c+1]+running
    answer=[0,0]
    def compress(r,c,size):
        total=prefix[r+size][c+size]-prefix[r][c+size]-prefix[r+size][c]+prefix[r][c]
        if total==0: answer[0]+=1; return
        if total==size*size: answer[1]+=1; return
        half=size//2
        for dr,dc in ((0,0),(0,half),(half,0),(half,half)): compress(r+dr,c+dc,half)
    compress(0,0,n)
    return answer
