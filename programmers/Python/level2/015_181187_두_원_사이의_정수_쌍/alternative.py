def solution(r1,r2):
    return sum(r1*r1 <= x*x+y*y <= r2*r2 for x in range(-r2,r2+1) for y in range(-r2,r2+1))
