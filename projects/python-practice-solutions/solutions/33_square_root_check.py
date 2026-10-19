# 정수 제곱근 판별
# 분류: 정수 제곱근
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12934
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

from math import isqrt


def solution(n):
    root = isqrt(n)

    if root * root == n:
        return (root + 1) ** 2

    return -1


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# from math import isqrt  # from 모듈 import 이름 문법입니다. math 모듈에서 정수 제곱근 함수 isqrt를 가져옵니다.
#
#
# def solution(n):  # def로 함수를 정의합니다. n은 입력 정수를 받는 매개변수입니다.
#     root = isqrt(n)  # 제곱근을 내림한 정수를 구해 root에 대입합니다. 예: isqrt(121)=11, isqrt(3)=1입니다.
#
#     if root * root == n:  # *는 곱셈, ==는 같은지 비교입니다. root가 정확한 정수 제곱근인지 검사합니다.
#         return (root + 1) ** 2  # 괄호 안을 먼저 계산합니다. **는 거듭제곱이므로 (root+1)을 제곱해 반환합니다.
#
#     return -1  # 위에서 반환하지 않았다면 제곱수가 아닙니다. 정수 -1을 반환하고 함수를 종료합니다.
#
