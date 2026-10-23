def solution(arr, k):
    if k % 2:
        return [value * k for value in arr]
    return [value + k for value in arr]

# 전체 코드 줄별 설명
# def solution(arr, k):  # def는 함수 정의. 정수 리스트와 변환 기준 입력.
#     if k % 2:  # if는 조건, %는 나머지. k가 홀수인지 확인.
#         return [value * k for value in arr]  # 리스트 내포로 각 원소에 k를 곱함.
#     return [value + k for value in arr]  # k가 짝수이면 각 원소에 k를 더한 리스트 반환.

# 풀이 요약
# k의 홀짝은 한 번만 검사하고 전체 원소에 같은 연산을 적용합니다.
# 