def solution(arr):
    return sum(arr) / len(arr)


# 같은 정답 코드 + 줄별 문법 설명
# 아래는 전체가 주석이므로 실행되지 않습니다.

# def solution(arr):  # def로 함수를 정의합니다. arr는 정수 리스트를 받는 매개변수입니다.
#     return sum(arr) / len(arr)  # sum()으로 합을 구하고 len()으로 개수를 구해 나눈 뒤 반환합니다.

# sum([1, 2, 3, 4])는 10입니다.
# len([1, 2, 3, 4])는 4입니다.
# /는 소수 부분을 유지하는 나눗셈이므로 10 / 4는 2.5입니다.