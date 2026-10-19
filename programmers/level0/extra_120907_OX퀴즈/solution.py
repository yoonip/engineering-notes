def solution(quiz):
    answer = []
    for expression in quiz:
        left, operator, right, equal, result = expression.split()
        a, b = int(left), int(right)
        actual = a + b if operator == '+' else a - b
        answer.append('O' if actual == int(result) else 'X')
    return answer

# 전체 코드 줄별 설명
# def solution(quiz):  # def는 함수 정의. 덧셈·뺄셈 등식 문자열 리스트 입력.
#     answer = []  # []는 빈 리스트. O·X 판정 결과 저장.
#     for expression in quiz:  # for로 각 등식 순회.
#         left, operator, right, equal, result = expression.split()  # split은 공백으로 분리. 음수의 부호는 숫자에 붙어 있어 그대로 보존.
#         a, b = int(left), int(right)  # int는 숫자 문자열을 정수로 변환. 음수도 처리.
#         actual = a + b if operator == '+' else a - b  # 조건 표현식으로 덧셈 또는 뺄셈 계산.
#         answer.append('O' if actual == int(result) else 'X')  # ==는 같음 비교, append는 끝에 추가. 등식 오른쪽 값과 비교한 판정 저장.
#     return answer  # 입력 등식 순서의 판정 리스트 반환.

# 풀이 요약
# 등식을 다섯 항목으로 나누어 왼쪽 계산값과 오른쪽 숫자를 비교합니다.
# 