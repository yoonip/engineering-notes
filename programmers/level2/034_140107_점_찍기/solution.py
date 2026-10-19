from math import isqrt

def solution(k, d):
    answer = 0
    for x in range(0, d + 1, k):
        max_y = isqrt(d * d - x * x)
        answer += max_y // k + 1
    return answer

# 전체 코드 줄별 설명
# from math import isqrt  # math 수학 모듈의 isqrt를 import로 가져옴. isqrt(n)은 제곱근의 정수 내림값.
# 
# def solution(k, d):  # def는 함수 정의, () 안 k는 격자 간격, d는 최대 거리.
#     answer = 0  # =는 대입. 점 개수 초기화.
#     for x in range(0, d + 1, k):  # range(시작,끝,간격)으로 0부터 d까지 k의 배수 순회.
#         max_y = isqrt(d * d - x * x)  # *는 곱셈. x²+y²<=d²를 만족하는 가장 큰 정수 y 계산.
#         answer += max_y // k + 1  # //는 정수 몫, +=는 더해 저장. y=0도 포함한 k 배수 개수 누적.
#     return answer  # return으로 찍을 수 있는 전체 점 개수 반환.

# 풀이 요약
# 각 x에서 원 내부의 최대 y를 구하고, 0부터 그 y까지 k의 배수인 좌표 수를 더합니다.
# 예: k=2,d=4이면 x=0,2,4에서 각각 3,2,1개로 총 6개. 시간 O(d/k+1), 공간 O(1).
