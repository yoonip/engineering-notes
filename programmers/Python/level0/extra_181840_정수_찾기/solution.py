def solution(num_list, n):
    return int(n in num_list)

# 전체 코드 줄별 설명
# def solution(num_list, n):  # def는 함수 정의. 정수 리스트와 찾을 수 입력.
#     return int(n in num_list)  # in은 리스트에 값이 있는지 검사. int는 참을 1·거짓을 0으로 변환.

# 풀이 요약
# 멤버십 연산 in으로 정수의 존재 여부를 확인합니다.
# 