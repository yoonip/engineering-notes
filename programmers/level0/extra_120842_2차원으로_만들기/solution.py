def solution(num_list, n):
    return [num_list[i:i + n] for i in range(0, len(num_list), n)]

# 전체 코드 줄별 설명
# def solution(num_list, n):  # def는 함수 정의. 일차원 리스트와 한 행의 원소 수 입력.
#     return [num_list[i:i + n] for i in range(0, len(num_list), n)]  # range의 간격 n으로 시작점 순회. 슬라이싱으로 n개씩 잘라 중첩 리스트 생성.

# 풀이 요약
# 앞에서 n개씩 자른 리스트를 한 행씩 모읍니다.
# 