from math import comb

def solution(n):
    # 반사 원리로 전체 균형 문자열에서 잘못된 접두사를 갖는 문자열을 뺀다.
    return comb(2*n,n)-comb(2*n,n+1)
