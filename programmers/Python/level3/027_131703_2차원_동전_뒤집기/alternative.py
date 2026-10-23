# 행을 뒤집을지 모두 정한 뒤 각 열이 일치하는지, 전부 반대인지 확인합니다. 열 선택은 그 결과로 결정됩니다. 기본 XOR
# 풀이보다 느리지만 가능한 행 선택을 직접 확인합니다.
def solution(beginning,target):
    n,m=len(beginning),len(beginning[0]);answer=float('inf')
    for mask in range(1<<n):
        cost=mask.bit_count()
        for c in range(m):
            difference=[beginning[r][c]^target[r][c]^((mask>>r)&1) for r in range(n)]
            if len(set(difference))!=1:break
            cost+=difference[0]
        else:answer=min(answer,cost)
    return -1 if answer==float('inf') else answer
