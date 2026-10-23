def solution(expressions):
    # 리스트 내포와 split()으로 각 수식을 단어 목록으로 분리.
    parsed = [expression.split() for expression in expressions]
    minimum = max(2, 1 + max(int(char) for expression in expressions for char in expression if char.isdigit()))

    def calculate(a, operator, b, base):
        # int(문자열,진법)은 해당 진법의 문자열을 정수로 해석.
        first, second = int(a, base), int(b, base)
        return first + second if operator == '+' else first - second

    bases = []
    for base in range(minimum, 10):
        # X는 건너뛰고 알려진 결과가 맞는지 확인.
        if all(c == 'X' or calculate(a, operator, b, base) == int(c, base) for a, operator, b, _, c in parsed):
            bases.append(base)

    def encode(value, base):
        # 0은 반복에서 문자가 생기지 않으므로 따로 처리.
        if value == 0:
            return '0'
        digits = []
        while value:
            value, remainder = divmod(value, base)
            # 나머지가 현재 가장 낮은 자릿수.
            digits.append(str(remainder))
        return ''.join(reversed(digits))

    answer = []
    for a, operator, b, _, c in parsed:
        if c != 'X':
            continue
        # {} 집합 내포로 진법별 결과 문자열의 중복 제거.
        results = {encode(calculate(a, operator, b, base), base) for base in bases}
        result = results.pop() if len(results) == 1 else '?'
        # 원래 순서대로 결과 수식 추가.
        answer.append(f'{a} {operator} {b} = {result}')
    return answer
