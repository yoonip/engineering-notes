# 햄버거 만들기
# 분류: 스택
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/133502
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

def solution(ingredient):
    stack = []
    answer = 0

    for item in ingredient:
        stack.append(item)

        if stack[-4:] == [1, 2, 3, 1]:
            del stack[-4:]
            answer += 1

    return answer


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# def solution(ingredient):  # def로 함수를 정의합니다. ingredient는 재료 숫자들이 들어 있는 리스트를 받습니다.
#     stack = []  # []는 빈 리스트입니다. 끝에 넣고 끝에서 빼는 스택 용도로 사용합니다.
#     answer = 0  # =는 대입입니다. 만든 햄버거 개수를 0으로 시작합니다.
#
#     for item in ingredient:  # for로 리스트의 재료를 하나씩 꺼내 item에 넣으며 반복합니다.
#         stack.append(item)  # 리스트.append(값)는 리스트 맨 뒤에 원소 하나를 추가합니다.
#
#         if stack[-4:] == [1, 2, 3, 1]:  # [-4:]는 끝의 최대 네 원소를 읽는 슬라이싱입니다. ==로 리스트의 값과 순서가 같은지 비교합니다.
#             del stack[-4:]  # del은 삭제 문법입니다. 슬라이싱으로 지정한 마지막 네 원소를 원래 리스트에서 지웁니다.
#             answer += 1  # answer = answer + 1과 같습니다. 완성한 개수를 하나 늘립니다.
#
#     return answer  # for문 바깥에서 최종 개수를 반환하고 함수를 종료합니다.
#
