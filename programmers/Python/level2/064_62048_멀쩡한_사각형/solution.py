from math import gcd

def solution(w, h):
    # 대각선이 지나는 잘린 칸 수 계산.
    broken = w + h - gcd(w, h)
    return w * h - broken
