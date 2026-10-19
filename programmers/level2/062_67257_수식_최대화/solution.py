from itertools import permutations
from re import split
from operator import add, sub, mul

def solution(expression):
    original = split(r'([+*-])', expression)
    functions = {'+': add, '-': sub, '*': mul}
    answer = 0
    for order in permutations('+-*'):
        tokens = original[:]
        for operation in order:
            while operation in tokens:
                index = tokens.index(operation)
                value = functions[operation](int(tokens[index - 1]), int(tokens[index + 1]))
                tokens[index - 1:index + 2] = [str(value)]
        answer = max(answer, abs(int(tokens[0])))
    return answer

# 전체 코드 줄별 설명
# from itertools import permutations  # itertools의 permutations는 모든 순서인 순열을 생성. 연산자 우선순위 나열에 사용.
# from re import split  # re는 정규식 모듈. split은 패턴을 기준으로 문자열 분리.
# from operator import add, sub, mul  # operator의 add·sub·mul은 각각 덧셈·뺄셈·곱셈을 수행하는 함수.
# 
# def solution(expression):  # def는 함수 정의, expression은 수식 문자열 입력.
#     original = split(r'([+*-])', expression)  # r은 원시 문자열 표기. []는 정규식 문자 선택, () 캡처로 분리한 연산자도 결과에 보존.
#     functions = {'+': add, '-': sub, '*': mul}  # {} 딕셔너리로 연산자 문자를 계산 함수에 연결.
#     answer = 0  # =는 대입. 최대 절댓값 초기화.
#     for order in permutations('+-*'):  # for~in으로 세 연산자의 6가지 우선순위 순회.
#         tokens = original[:]  # [:] 슬라이스로 토큰 목록 복사. 원본 수식을 보존.
#         for operation in order:  # 우선순위가 높은 연산자부터 처리.
#             while operation in tokens:  # while은 반복, in은 포함 검사. 해당 연산이 남은 동안 계산.
#                 index = tokens.index(operation)  # index는 처음 나오는 위치 반환. 같은 연산자는 왼쪽부터 처리.
#                 value = functions[operation](int(tokens[index - 1]), int(tokens[index + 1]))  # [키]의 함수 호출. int로 좌우 피연산자를 정수 변환.
#                 tokens[index - 1:index + 2] = [str(value)]  # 구간 슬라이스 대입으로 피연산자·연산자 세 토큰을 결과 한 토큰으로 교체. str은 문자열 변환.
#         answer = max(answer, abs(int(tokens[0])))  # [0]의 최종 값을 정수화. abs는 절댓값, max는 최댓값.
#     return answer  # return으로 가능한 최대 상금 반환.

# 풀이 요약
# 6가지 연산자 우선순위마다 높은 연산부터 왼쪽 순서로 계산하고 결과의 절댓값을 비교합니다.
# 예: 100-200*300-500+20은 *→+→- 순서에서 60420. 토큰 수 T일 때 시간 O(6T²), 공간 O(T).
