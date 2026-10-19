def solution(a, b):
    return max(int(str(a) + str(b)), 2 * a * b)

# 전체 코드 줄별 설명
# def solution(a, b):  # def는 함수 정의. 두 정수 a와 b를 입력받음.
#     return max(int(str(a) + str(b)), 2 * a * b)  # str로 바꿔 +로 연결한 수와 *로 곱한 수를 max로 비교. int는 정수 변환.

# 풀이 요약
# 연결한 수와 2ab를 각각 계산해 큰 수를 반환합니다.
# 