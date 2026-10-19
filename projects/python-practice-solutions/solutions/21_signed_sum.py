# 음양 더하기
# 분류: 반복 / 조건
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/76501
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

def solution(absolutes, signs):
    answer = 0

    for number, positive in zip(absolutes, signs):
        if positive:
            answer += number
        else:
            answer -= number

    return answer


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# def solution(absolutes, signs):  # def로 함수를 정의합니다. 절댓값 리스트와 부호 리스트를 매개변수로 받습니다.
#     answer = 0  # =는 대입입니다. 합계를 0으로 시작합니다.
#
#     for number, positive in zip(absolutes, signs):  # zip은 같은 위치의 두 원소를 튜플로 묶습니다. 숫자와 부호를 각각 변수로 받는 언패킹입니다.
#         if positive:  # positive는 True 또는 False인 bool 값입니다. True이면 아래 코드를 실행합니다.
#             answer += number  # answer = answer + number와 같습니다. 양수이므로 더합니다.
#         else:  # positive가 False이면 실행합니다.
#             answer -= number  # answer = answer - number와 같습니다. 음수이므로 절댓값을 뺍니다.
#
#     return answer  # 반복문 바깥에서 합계를 반환하고 함수를 종료합니다.
#
