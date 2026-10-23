from itertools import permutations
from re import split
from operator import add, sub, mul

def solution(expression):
    original = split(r'([+*-])', expression)
    functions = {'+': add, '-': sub, '*': mul}
    answer = 0
    # 세 연산자의 여섯 우선순위를 모두 확인한다.
    for order in permutations('+-*'):
        tokens = original[:]
        for operation in order:
            while operation in tokens:
                # 같은 연산자는 왼쪽부터 계산한다.
                index = tokens.index(operation)
                value = functions[operation](int(tokens[index - 1]), int(tokens[index + 1]))
                tokens[index - 1:index + 2] = [str(value)]
        answer = max(answer, abs(int(tokens[0])))
    return answer
