from math import isqrt

def solution(r1, r2):
    answer = 0
    for x in range(1, r2 + 1):
        high = isqrt(r2 * r2 - x * x)
        inner = max(0, r1 * r1 - x * x)
        low = isqrt(inner)
        if low * low < inner:
            low += 1
        answer += high - low + 1
    return answer * 4

# 전체 코드 줄별 설명
# from math import isqrt  # from~import는 모듈에서 기능 가져오기. math는 수학 모듈, isqrt(n)은 정수 제곱근의 내림값.
# 
# def solution(r1, r2):  # def는 함수 정의. ()의 r1,r2는 작은 원·큰 원 반지름.
#     answer = 0  # =는 대입. x>0,y>=0 영역의 점 수 초기화.
#     for x in range(1, r2 + 1):  # range는 끝 미포함 정수 범위. 1부터 r2까지 순회.
#         high = isqrt(r2 * r2 - x * x)  # *는 곱셈. 큰 원 안에 있는 최대 정수 y 계산.
#         inner = max(0, r1 * r1 - x * x)  # max는 최댓값. 음수가 되면 작은 원의 y 제한을 0으로 둠.
#         low = isqrt(inner)  # 작은 원 경계의 y를 우선 내림 계산.
#         if low * low < inner:  # if는 조건 분기, <는 작음. 완전제곱수가 아니면 올림 필요.
#             low += 1  # +=는 더해 저장. 최소 정수 y를 올림값으로 보정.
#         answer += high - low + 1  # low~high의 양 끝을 포함한 정수 개수를 누적.
#     return answer * 4  # return은 반환. 회전 대칭인 네 영역의 점 수로 확대.

# 풀이 요약
# x를 고정해 두 원 사이에 놓이는 정수 y의 최솟값·최댓값을 정수 제곱근으로 구합니다. 경계도 포함합니다.
# 예: r1=2,r2=3이면 한 영역 5개, 전체 20개. x>0,y>=0을 세면 축도 중복 없이 네 배 됩니다. 시간 O(r2), 공간 O(1).
