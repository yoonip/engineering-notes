def solution(arr):
    stack = []
    for value in arr:
        while stack and stack[-1] >= value:
            stack.pop()
        stack.append(value)
    return stack

# 전체 코드 줄별 설명
# def solution(arr):  # def는 함수 정의. 정수 리스트 입력.
#     stack = []  # []는 빈 리스트. 끝에 넣고 끝에서 꺼내는 스택으로 사용.
#     for value in arr:  # for는 입력 원소를 순서대로 순회.
#         while stack and stack[-1] >= value:  # and는 두 조건 모두 참. -1은 마지막 원소. 새 값 이상인 끝 원소가 남아 있는지 검사.
#             stack.pop()  # pop은 마지막 원소를 제거해 반환. 새 값보다 작을 때까지 제거.
#         stack.append(value)  # append는 끝에 추가. 조건에 맞게 새 값을 삽입.
#     return stack  # 최종 스택 반환.

# 풀이 요약
# 새 값을 넣기 전에 끝의 크거나 같은 값들을 모두 제거합니다. 각 원소는 최대 한 번 삽입·제거되어 O(N)입니다.
# 