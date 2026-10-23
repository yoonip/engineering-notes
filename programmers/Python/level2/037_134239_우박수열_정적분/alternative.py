from fractions import Fraction

def solution(k,ranges):
    values=[k]
    while k>1:
        k=k//2 if k%2==0 else 3*k+1
        values.append(k)
    n=len(values)-1
    answer=[]
    for start,offset in ranges:
        end=n+offset
        area=sum((Fraction(values[i]+values[i+1],2) for i in range(start,end)),Fraction(0))
        answer.append(float(area) if start<=end else -1.0)
    return answer
