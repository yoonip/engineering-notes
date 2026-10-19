# 짝수와 홀수
# 분류: 나머지 연산
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12937
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

def solution(num):
    if num % 2 == 0:
        return "Even"
    else:
        return "Odd"


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# def solution(num):  # def로 함수를 정의합니다. num은 입력 정수를 받는 매개변수입니다.
#     if num % 2 == 0:  # %는 나머지 연산, ==는 같은지 비교입니다. 2로 나누어 떨어지는지 확인합니다.
#         return "Even"  # 따옴표 안의 값은 문자열입니다. 짝수이면 "Even"을 반환하고 함수를 종료합니다.
#     else:  # if 조건이 거짓일 때 실행합니다. 이 경우는 홀수입니다.
#         return "Odd"  # 홀수이면 문자열 "Odd"를 반환하고 함수를 종료합니다.
#
