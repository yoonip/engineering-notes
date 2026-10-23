def solution(arr):
    answer = []
    for value in arr:
        answer.extend([value] * value)
    return answer

# 전체 코드 줄별 설명
# def solution(arr):  # def는 함수 정의. 양의 정수 리스트 입력.
#     answer = []  # []는 빈 리스트. 반복한 원소를 모음.
#     for value in arr:  # for로 각 원소를 순서대로 순회.
#         answer.extend([value] * value)  # [value]*value는 같은 값을 value개 가진 리스트. extend는 그 원소들을 끝에 추가.
#     return answer  # 완성된 리스트 반환.

# 풀이 요약
# 각 수 a를 a번 반복한 묶음을 입력 순서대로 연결합니다.
# 