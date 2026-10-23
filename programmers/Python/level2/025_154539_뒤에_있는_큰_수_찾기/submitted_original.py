def solution(numbers):
    answer = [-1] * len(numbers)
    stack = []
    for index, value in enumerate(numbers):
        while stack and numbers[stack[-1]] < value:
            previous = stack.pop()
            answer[previous] = value
        stack.append(index)
    return answer

# 전체 코드 줄별 설명
# def solution(numbers):  # def로 함수 정의. numbers는 정수 리스트 입력.
#     answer = [-1] * len(numbers)  # []는 리스트, *는 반복, len은 길이. 큰 수가 없는 경우의 -1로 초기화.
#     stack = []  # 아직 뒷 큰수를 못 찾은 인덱스를 보관하는 스택.
#     for index, value in enumerate(numbers):  # enumerate는 (인덱스,값)을 제공. for로 순서대로 순회.
#         while stack and numbers[stack[-1]] < value:  # while은 반복, and는 둘 다 참, [-1]은 마지막 원소. 스택 위 값이 현재보다 작은 동안 처리.
#             previous = stack.pop()  # pop은 마지막 인덱스를 꺼내 삭제.
#             answer[previous] = value  # [인덱스]에 대입. 현재 값이 이전 원소의 가장 가까운 뒷 큰수.
#         stack.append(index)  # append로 현재 인덱스를 마지막에 추가.
#     return answer  # return으로 각 원소의 뒷 큰수 목록 반환.

# 풀이 요약
# 아직 답을 못 찾은 인덱스를 값이 비증가하는 스택에 모읍니다. 더 큰 값이 나타나면 작은 원소의 답을 확정합니다.
# 예: [2,3,3,5]는 [3,5,5,-1]. 같은 수는 큰 수가 아니므로 빼지 않습니다. 시간·공간 O(N).
