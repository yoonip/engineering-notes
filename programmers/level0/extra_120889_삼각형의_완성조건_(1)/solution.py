def solution(sides):
    return 1 if sum(sides) > 2 * max(sides) else 2

# 전체 코드 줄별 설명
# def solution(sides):  # def는 함수 정의. 세 변의 길이 리스트 입력.
#     return 1 if sum(sides) > 2 * max(sides) else 2  # sum은 합계, max는 최댓값. 가장 긴 변보다 나머지 두 변의 합이 크면 1, 아니면 2 반환.

# 풀이 요약
# 전체 합에서 가장 긴 변을 뺀 값이 가장 긴 변보다 큰지 확인합니다.
# 