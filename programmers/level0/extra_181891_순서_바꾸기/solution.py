def solution(num_list, n):
    return num_list[n:] + num_list[:n]

# 전체 코드 줄별 설명
# def solution(num_list, n):  # def는 함수 정의. 리스트와 앞 묶음의 길이 입력.
#     return num_list[n:] + num_list[:n]  # [n:]은 앞 n개 이후, [:n]은 앞 n개. +는 뒤 묶음을 앞으로 옮겨 연결.

# 풀이 요약
# 앞 n개와 나머지로 나누고 두 묶음의 순서를 바꿉니다.
# 