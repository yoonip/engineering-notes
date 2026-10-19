def solution(todo_list, finished):
    return [task for task, done in zip(todo_list, finished) if not done]

# 전체 코드 줄별 설명
# def solution(todo_list, finished):  # def는 함수 정의. 할 일과 완료 여부 리스트 입력.
#     return [task for task, done in zip(todo_list, finished) if not done]  # zip은 같은 위치 원소를 묶음. 리스트 내포에서 not으로 미완료인 일만 선택.

# 풀이 요약
# 할 일과 완료 여부를 짝지은 뒤 완료되지 않은 일만 원래 순서대로 남깁니다.
# 