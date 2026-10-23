from math import isqrt

def solution(n):
    root = isqrt(n)
    return 1 if root * root == n else 2

# 전체 코드 줄별 설명
# from math import isqrt  # from 모듈 import 이름은 도구 가져오기. math는 수학 모듈, isqrt는 정수 제곱근의 내림값을 정확히 계산.
# 
# def solution(n):  # def는 함수 정의. 제곱수인지 검사할 양의 정수 입력.
#     root = isqrt(n)  # isqrt로 제곱근 이하의 가장 큰 정수 계산.
#     return 1 if root * root == n else 2  # 조건 표현식. 제곱근을 다시 제곱한 값이 원래 수와 같으면 1, 아니면 2.

# 풀이 요약
# 정수 제곱근을 구해 제곱했을 때 원래 수가 되는지 확인합니다.
# 