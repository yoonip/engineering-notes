from math import isqrt

def solution(n,k):
    digits=[]
    while n:
        n,d=divmod(n,k)
        digits.append(str(d))
    values=[int(s) for s in ''.join(reversed(digits)).split('0') if s]
    bound=isqrt(max(values,default=1))
    sieve=bytearray([1])*(bound+1)
    if bound>=0: sieve[0]=0
    if bound>=1: sieve[1]=0
    for p in range(2,isqrt(bound)+1):
        if sieve[p]:
            for multiple in range(p*p,bound+1,p): sieve[multiple]=0
    primes=[p for p in range(2,bound+1) if sieve[p]]
    answer=0
    for value in values:
        if value<2: continue
        for p in primes:
            if p*p>value: break
            if value%p==0: break
        else:
            answer+=1
            continue
        if p*p>value: answer+=1
    return answer
