# 문제: 수식 최대화
# 원문: https://school.programmers.co.kr/learn/courses/30/lessons/67257
# 풀이: 우선순위 6가지를 비교하되 각 단계의 토큰을 왼쪽부터 한 번 접는다. 반복 검색과 리스트 중간 삭제를 피한다.
# 복잡도: 토큰 T개: 제한 범위 정수 연산 기준 시간 O(T), 추가 공간 O(T). 우선순위 6가지·단계 3개는 상수다.

from itertools import permutations
from re import split
from operator import add, sub, mul


def solution(expression):
    pieces = split(r'([+*-])', expression)
    original = [int(value) if index % 2 == 0 else value
                for index, value in enumerate(pieces)]
    functions = {'+': add, '-': sub, '*': mul}
    answer = 0
    for order in permutations('+-*'):
        tokens = original
        for operation in order:
            folded = [tokens[0]]
            for index in range(1, len(tokens), 2):
                if tokens[index] == operation:
                    # 같은 우선순위는 왼쪽부터 접어 결합 순서를 유지한다.
                    folded[-1] = functions[operation](folded[-1], tokens[index + 1])
                else:
                    folded.extend((tokens[index], tokens[index + 1]))
            tokens = folded
        answer = max(answer, abs(tokens[0]))
    return answer
