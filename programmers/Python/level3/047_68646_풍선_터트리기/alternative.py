# 각 위치 왼쪽의 최솟값과 오른쪽의 최솟값을 미리 저장합니다. 현재 값보다 작은 값이 양쪽 모두에 있으면 살릴 수 없습니다.
def solution(a):
    n=len(a);left=[float('inf')]*n;right=[float('inf')]*n
    for i in range(1,n):left[i]=min(left[i-1],a[i-1])
    for i in range(n-2,-1,-1):right[i]=min(right[i+1],a[i+1])
    return sum(not (left[i]<a[i] and right[i]<a[i]) for i in range(n))
