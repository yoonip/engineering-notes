def solution(ingredient):
    stack = []
    answer = 0

    for item in ingredient:
        stack.append(item)

        if stack[-4:] == [1, 2, 3, 1]:
            del stack[-4:]
            answer += 1

    return answer


# 같은 정답 코드 + 줄별 문법 설명
# 아래는 전체가 주석이므로 실행되지 않습니다.

# def solution(ingredient):  # def로 함수를 정의합니다. ingredient는 재료 리스트를 받는 매개변수입니다.
#     stack = []  # []는 빈 리스트입니다. 맨 뒤에 넣고 빼는 스택으로 사용합니다.
#     answer = 0  # =는 대입입니다. 만든 햄버거 개수를 0으로 시작합니다.
#
#     for item in ingredient:  # 재료를 하나씩 꺼내 item에 넣으며 반복합니다.
#         stack.append(item)  # append()는 리스트 맨 뒤에 원소 하나를 추가합니다.
#
#         if stack[-4:] == [1, 2, 3, 1]:  # [-4:]는 마지막 네 원소를 읽는 슬라이싱입니다. ==로 값과 순서를 비교합니다.
#             del stack[-4:]  # del은 삭제 문법입니다. 원래 리스트에서 마지막 네 원소를 지웁니다.
#             answer += 1  # answer = answer + 1과 같습니다.
#
#     return answer  # 반복이 모두 끝나면 햄버거 개수를 반환하고 함수를 종료합니다.

# 원소가 네 개 미만이어도 [-4:]는 오류 없이 있는 원소만 반환합니다.
# 그 경우 [1, 2, 3, 1]과 같지 않으므로 삭제하지 않습니다.