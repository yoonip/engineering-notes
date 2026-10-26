import sys  # 네 점의 정수 토큰 읽기
tokens = iter(map(int, sys.stdin.read().split()))  # 좌표 입력 순회
points = [(next(tokens), next(tokens)) for _ in range(4)]  # A,B,C,D
def orientation(a, b, c):  # 외적의 방향 부호
    value = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])  # AB와 AC의 외적
    return (value > 0) - (value < 0)  # 세 가지 방향
def between(a, x, b):  # 닫힌 좌표 범위
    return min(a, b) <= x <= max(a, b)  # 끝점 순서와 무관한 포함
def on_segment(a, b, p):  # 직선과 선분 구분
    return orientation(a, b, p) == 0 and between(a[0], p[0], b[0]) and between(a[1], p[1], b[1])  # 일직선과 경계 포함
a, b, c, d = points  # 두 선분 이름
first, second = orientation(a, b, c), orientation(a, b, d)  # AB 양쪽 부호
third, fourth = orientation(c, d, a), orientation(c, d, b)  # CD 양쪽 부호
result = first * second < 0 and third * fourth < 0  # 엄격한 내부 교차
result = result or on_segment(a, b, c) or on_segment(a, b, d) or on_segment(c, d, a) or on_segment(c, d, b)  # 일직선과 끝점 교차
print(first, "YES" if result else "NO")  # 방향과 최종 판정
