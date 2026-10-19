def solution(dots):
    xs, ys = zip(*dots)
    return (max(xs) - min(xs)) * (max(ys) - min(ys))

# 전체 코드 줄별 설명
# def solution(dots):  # def는 함수 정의. 축과 평행한 직사각형의 네 꼭짓점 입력.
#     xs, ys = zip(*dots)  # *는 좌표 리스트 풀기, zip은 같은 위치 원소 묶기. x좌표들과 y좌표들을 각각 모음.
#     return (max(xs) - min(xs)) * (max(ys) - min(ys))  # max·min은 최댓값·최솟값. 가로 길이와 세로 길이를 곱해 넓이 계산.

# 풀이 요약
# 가로는 x의 최댓값-최솟값, 세로는 y의 최댓값-최솟값입니다.
# 