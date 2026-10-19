def solution(arr):
    stack = []
    for value in arr:
        if stack and stack[-1] == value:
            stack.pop()
        else:
            stack.append(value)
    return stack or [-1]

# 전체 코드 줄별 설명
# def solution(arr):  # def는 함수 정의. 0과 1로 구성된 리스트 입력.
#     stack = []  # []는 빈 리스트. 마지막 값을 기준으로 처리하는 스택.
#     for value in arr:  # for로 입력 값을 순서대로 순회.
#         if stack and stack[-1] == value:  # and는 모두 참. 비어 있지 않고 끝 값이 현재 값과 같은지 확인.
#             stack.pop()  # pop은 마지막 원소 제거. 같은 두 값을 상쇄.
#         else:  # 스택이 비었거나 마지막 값이 다른 경우.
#             stack.append(value)  # append는 현재 값을 끝에 추가.
#     return stack or [-1]  # or는 스택이 비어 있으면 [-1] 선택. return으로 결과 반환.

# 풀이 요약
# 새 값과 마지막 값이 같으면 마지막 값을 제거하고, 다르면 추가합니다. 각 입력을 한 번씩 처리합니다.
# 