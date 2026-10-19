def solution(money):
    n=len(money)
    if n>22:raise ValueError("집 22개 이하의 선택 전수 비교용입니다")
    best=0;all_bits=(1<<n)-1
    for mask in range(1<<n):
        rotated=((mask<<1)&all_bits)|(mask>>(n-1))
        if not mask&rotated:best=max(best,sum(money[i] for i in range(n) if mask>>i&1))
    return best
