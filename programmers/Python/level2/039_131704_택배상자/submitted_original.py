def solution(order):
    stack = []
    answer = 0
    for box in range(1, len(order) + 1):
        stack.append(box)
        while stack and stack[-1] == order[answer]:
            stack.pop()
            answer += 1
    return answer

# 전체 코드 줄별 설명
# def solution(order):  # def는 함수 정의. order는 원하는 적재 순서 입력.
#     stack = []  # []는 빈 리스트. 마지막에 넣은 상자부터 꺼내는 보조 벨트 스택.
#     answer = 0  # =는 대입. 적재한 개수이자 다음 요청의 인덱스.
#     for box in range(1, len(order) + 1):  # len은 길이, range는 끝 미포함. 상자가 1번부터 차례로 도착.
#         stack.append(box)  # append는 리스트 끝에 추가. 도착한 상자를 보조 벨트 위에 놓음.
#         while stack and stack[-1] == order[answer]:  # while은 반복, and는 둘 다 참, [-1]은 스택 위. 다음 요청과 같으면 적재 가능.
#             stack.pop()  # pop은 마지막 원소를 꺼내 삭제. 상자를 트럭으로 옮김.
#             answer += 1  # +=는 더해 저장. 적재 수를 늘리고 다음 요청으로 이동.
#     return answer  # return으로 순서대로 적재한 상자 수 반환.

# 풀이 요약
# 상자를 순서대로 스택에 넣고, 스택 위가 다음 요청이면 즉시 적재합니다. 마지막 도착 뒤에도 못 꺼낸 상자는 적재 불가입니다.
# 예: [4,3,1,2,5]에서는 4·3만 적재해 2. 각 상자는 한 번씩 들어가고 나오므로 시간·공간 O(N).
