def solution(a, b):
    return max(int(str(a) + str(b)), int(str(b) + str(a)))

# 전체 코드 줄별 설명
# def solution(a, b):  # def는 함수 정의. 두 양의 정수 입력.
#     return max(int(str(a) + str(b)), int(str(b) + str(a)))  # str은 문자열 변환, +는 문자열 연결, int는 정수 변환, max는 큰 값 선택.

# 풀이 요약
# 문자열로 바꿔 두 순서로 연결한 뒤 정수로 비교합니다.
# 