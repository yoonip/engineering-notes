def solution(arr, delete_list):
    removed = set(delete_list)
    return [value for value in arr if value not in removed]

# 전체 코드 줄별 설명
# def solution(arr, delete_list):  # def는 함수 정의. 원본 값과 삭제할 값 리스트 입력.
#     removed = set(delete_list)  # set은 중복 없는 집합. 삭제 대상 값을 빠르게 조회할 수 있게 변환.
#     return [value for value in arr if value not in removed]  # 리스트 내포의 for는 순회, if는 필터. not in으로 삭제 대상이 아닌 값만 보존.

# 풀이 요약
# 삭제 대상 집합에 없는 원소만 원래 순서대로 남깁니다.
# 