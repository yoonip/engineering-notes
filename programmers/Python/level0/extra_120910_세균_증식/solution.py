def solution(n, t):
    return n * 2 ** t

# 전체 코드 줄별 설명
# def solution(n, t):  # def는 함수 정의. 처음 세균 수와 경과 시간 입력.
#     return n * 2 ** t  # **는 거듭제곱, *는 곱셈. 시간마다 두 배이므로 최초 개수에 2의 t제곱을 곱함.

# 풀이 요약
# 매 시간 두 배로 증가하므로 n×2^t입니다.
# 