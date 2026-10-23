def solution(expressions):
    parsed = [expression.split() for expression in expressions]
    minimum = max(2, 1 + max(int(char) for expression in expressions for char in expression if char.isdigit()))

    def calculate(a, operator, b, base):
        first, second = int(a, base), int(b, base)
        return first + second if operator == '+' else first - second

    bases = []
    for base in range(minimum, 10):
        if all(c == 'X' or calculate(a, operator, b, base) == int(c, base) for a, operator, b, _, c in parsed):
            bases.append(base)

    def encode(value, base):
        if value == 0:
            return '0'
        digits = []
        while value:
            value, remainder = divmod(value, base)
            digits.append(str(remainder))
        return ''.join(reversed(digits))

    answer = []
    for a, operator, b, _, c in parsed:
        if c != 'X':
            continue
        results = {encode(calculate(a, operator, b, base), base) for base in bases}
        result = results.pop() if len(results) == 1 else '?'
        answer.append(f'{a} {operator} {b} = {result}')
    return answer

# 전체 코드 줄별 설명
# def solution(expressions):  # def는 함수 정의. expressions는 공백으로 구분된 수식 문자열 목록.
#     parsed = [expression.split() for expression in expressions]  # 리스트 내포와 split()으로 각 수식을 단어 목록으로 분리.
#     minimum = max(2, 1 + max(int(char) for expression in expressions for char in expression if char.isdigit()))  # isdigit은 숫자 문자 검사, int는 정수 변환. 가장 큰 자릿값보다 큰 진법만 가능.
# 
#     def calculate(a, operator, b, base):  # 두 피연산자와 연산자·진법을 받아 십진 정수 결과를 계산하는 중첩 함수.
#         first, second = int(a, base), int(b, base)  # int(문자열,진법)은 해당 진법의 문자열을 정수로 해석.
#         return first + second if operator == '+' else first - second  # ==는 같음. a if 조건 else b로 덧셈 또는 뺄셈 결과 반환.
# 
#     bases = []  # []는 빈 리스트. 모든 완성 수식을 만족하는 진법 목록.
#     for base in range(minimum, 10):  # range는 끝 제외. 가능한 최소 진법부터 9진법까지 순회.
#         if all(c == 'X' or calculate(a, operator, b, base) == int(c, base) for a, operator, b, _, c in parsed):  # all은 모두 참인지 검사, or는 하나라도 참. X는 건너뛰고 알려진 결과가 맞는지 확인.
#             bases.append(base)  # append로 가능한 진법 하나 추가.
# 
#     def encode(value, base):  # 십진 정수를 지정 진법의 문자열로 바꾸는 함수.
#         if value == 0:  # 0은 반복에서 문자가 생기지 않으므로 따로 처리.
#             return '0'  # return은 문자열 반환과 함수 종료.
#         digits = []  # 변환한 자릿수를 뒤에서부터 모음.
#         while value:  # while은 조건이 참인 동안 반복. 정수 0은 거짓.
#             value, remainder = divmod(value, base)  # divmod는 (몫, 나머지). 몫으로 다음 자릿수 진행.
#             digits.append(str(remainder))  # str은 문자열 변환. 나머지가 현재 가장 낮은 자릿수.
#         return ''.join(reversed(digits))  # reversed로 역순으로 읽고 join으로 이어 붙여 원래 자릿수 순서 복원.
# 
#     answer = []  # 복원할 수식 결과 목록.
#     for a, operator, b, _, c in parsed:  # 각 수식의 다섯 단어를 언패킹. _는 사용하지 않는 = 기호.
#         if c != 'X':  # !=는 다름. 이미 알려진 수식은 출력 대상이 아님.
#             continue  # continue는 다음 수식으로 진행.
#         results = {encode(calculate(a, operator, b, base), base) for base in bases}  # {} 집합 내포로 진법별 결과 문자열의 중복 제거.
#         result = results.pop() if len(results) == 1 else '?'  # len은 개수, pop은 집합 원소 하나를 제거·반환. 모든 진법의 결과가 같을 때만 확정.
#         answer.append(f'{a} {operator} {b} = {result}')  # f 문자열의 {}는 변수 값을 삽입. 원래 순서대로 결과 수식 추가.
#     return answer  # 복원된 수식 문자열 목록 반환.

# 풀이 요약
# 등장한 가장 큰 숫자보다 큰 2~9진법을 후보로 삼고, 이미 결과가 알려진 수식을 모두 만족하는 진법만 남깁니다.
# X 수식은 가능한 진법마다 계산한 결과 문자열을 비교합니다. 문자열이 하나로 같으면 그 값, 다르면 ?입니다. 수식 수 E·문자 길이 L에 대해 시간 O(8EL), 공간 O(EL).
# 예: 1+5는 6진법에서 10, 7~9진법에서 6이므로 ?. 반면 1+2는 모든 후보 진법에서 3으로 같아 확정됩니다.
