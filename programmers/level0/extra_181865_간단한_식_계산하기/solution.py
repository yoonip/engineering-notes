def solution(binomial):
    left, operator, right = binomial.split()
    a, b = int(left), int(right)
    if operator == '+':
        return a + b
    if operator == '-':
        return a - b
    return a * b

# 전체 코드 줄별 설명
# def solution(binomial):  # def는 함수 정의. 두 정수와 연산 기호로 된 문자열 입력.
#     left, operator, right = binomial.split()  # split은 공백 분리. 세 항목을 왼쪽 수·기호·오른쪽 수로 나누어 대입.
#     a, b = int(left), int(right)  # int는 문자열을 정수로 변환. 두 숫자를 각각 저장.
#     if operator == '+':  # if는 조건, ==는 같음 비교. 덧셈 기호 검사.
#         return a + b  # 두 정수의 합 반환.
#     if operator == '-':  # 뺄셈 기호 검사.
#         return a - b  # 두 정수의 차 반환.
#     return a * b  # 남은 연산 기호 *는 곱셈이므로 곱 반환.

# 풀이 요약
# 문자열을 세 항목으로 나눈 뒤 연산 기호에 맞는 계산을 적용합니다.
# 