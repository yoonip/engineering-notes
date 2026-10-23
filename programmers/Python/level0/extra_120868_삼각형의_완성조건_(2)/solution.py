def solution(sides):
    return 2 * min(sides) - 1

# 전체 코드 줄별 설명
# def solution(sides):  # def는 함수 정의. 삼각형의 두 변 길이 입력.
#     return 2 * min(sides) - 1  # min은 작은 변 길이. |a-b|<세 번째 변<a+b 사이 정수 개수는 2*작은 변-1.

# 풀이 요약
# 삼각형 부등식을 합치면 세 번째 변은 두 변의 차보다 크고 합보다 작아야 합니다.
# 