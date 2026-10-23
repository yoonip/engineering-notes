from itertools import permutations
import re

def solution(expression):
    tokens=re.findall(r'\d+|[+*-]',expression)
    answer=0
    def calculate(a,b,op):
        return a+b if op=='+' else a-b if op=='-' else a*b
    for order in permutations('+-*'):
        rank={op:i for i,op in enumerate(order)}
        values=[]
        operators=[]
        def reduce_top():
            b,a=values.pop(),values.pop()
            values.append(calculate(a,b,operators.pop()))
        for token in tokens:
            if token.isdigit(): values.append(int(token))
            else:
                while operators and rank[operators[-1]]>=rank[token]: reduce_top()
                operators.append(token)
        while operators: reduce_top()
        answer=max(answer,abs(values[0]))
    return answer
