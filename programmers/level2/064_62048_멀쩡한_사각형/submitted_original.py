from math import gcd

def solution(w, h):
    broken = w + h - gcd(w, h)
    return w * h - broken

# 전체 코드 줄별 설명
# from math import gcd  # math 모듈의 gcd를 import. gcd(a,b)는 두 정수의 최대공약수 반환.
# 
# def solution(w, h):  # def는 함수 정의. () 안 w·h는 종이 가로·세로 길이.
#     broken = w + h - gcd(w, h)  # +·-는 덧셈·뺄셈, =는 대입. 대각선이 지나는 잘린 칸 수 계산.
#     return w * h - broken  # *는 곱셈. 전체 칸에서 잘린 칸을 빼 return으로 반환.

# 풀이 요약
# 대각선은 가로·세로 격자선을 지날 때 새 칸에 진입합니다. 공통 격자점에서는 두 번 세므로 최대공약수만큼 보정해 잘린 칸은 w+h-gcd(w,h)입니다.
# 예: 8×12에서 잘린 칸은 8+12-4=16, 남는 칸은 80. 시간 O(log min(w,h)), 공간 O(1).
