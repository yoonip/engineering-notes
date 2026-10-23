def solution(num_list, n):
    return num_list[n - 1:]

# 전체 코드 줄별 설명
# def solution(num_list, n):  # def는 함수 정의. 리스트와 1부터 세는 시작 순번 입력.
#     return num_list[n - 1:]  # 순번 n은 인덱스 n-1. [시작:] 슬라이싱으로 그 위치부터 끝까지 반환.

# 풀이 요약
# 1부터 세는 순번과 0부터 세는 인덱스를 구분합니다.
# 