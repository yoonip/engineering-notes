from itertools import combinations
from fractions import Fraction

def solution(line):
    points=set()
    for first,second in combinations(line,2):
        rows=[[Fraction(a),Fraction(b),Fraction(-c)] for a,b,c in (first,second)]
        if rows[0][0]==0: rows.reverse()
        if rows[0][0]==0: continue
        pivot=rows[0][0]
        rows[0]=[v/pivot for v in rows[0]]
        factor=rows[1][0]
        rows[1]=[a-factor*b for a,b in zip(rows[1],rows[0])]
        if rows[1][1]==0: continue
        y=rows[1][2]/rows[1][1]
        x=rows[0][2]-rows[0][1]*y
        if x.denominator==y.denominator==1: points.add((int(x),int(y)))
    lo_x,hi_x=min(x for x,y in points),max(x for x,y in points)
    lo_y,hi_y=min(y for x,y in points),max(y for x,y in points)
    return [''.join('*' if (x,y) in points else '.' for x in range(lo_x,hi_x+1)) for y in range(hi_y,lo_y-1,-1)]
