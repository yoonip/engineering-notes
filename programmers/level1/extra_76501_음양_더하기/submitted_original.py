def solution(absolutes, signs):
    answer = 0

    for number, positive in zip(absolutes, signs):
        if positive:
            answer += number
        else:
            answer -= number

    return answer


# 같은 정답 코드 + 줄별 문법 설명
# 아래는 전체가 주석이므로 실행되지 않습니다.

# def solution(absolutes, signs):  # def로 함수를 정의합니다. 절댓값 리스트와 부호 리스트를 받습니다.
#     answer = 0  # =는 대입입니다. 합계를 0으로 시작합니다.
#
#     for number, positive in zip(absolutes, signs):  # zip은 같은 위치의 숫자와 부호를 묶습니다. 두 값을 각각 변수로 받습니다.
#         if positive:  # positive는 True 또는 False입니다. True이면 아래 코드를 실행합니다.
#             answer += number  # answer = answer + number와 같습니다.
#         else:  # positive가 False이면 실행합니다.
#             answer -= number  # answer = answer - number와 같습니다.
#
#     return answer  # 반복이 끝나면 합계를 반환하고 함수를 종료합니다.