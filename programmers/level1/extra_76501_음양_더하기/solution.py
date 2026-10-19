def solution(absolutes, signs):
    answer = 0
    for number, positive in zip(absolutes, signs):
        if positive:
            answer += number
        else:
            answer -= number
    return answer

# 전체 코드 줄별 설명
# def solution(absolutes, signs):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def로 함수를 정의합니다. 절댓값 리스트와 부호 리스트를 받습니다.
#     answer = 0  # =는 값 저장. =는 대입입니다. 합계를 0으로 시작합니다.
#     for number, positive in zip(absolutes, signs):  # for·in은 원소를 차례로 꺼내는 반복문. zip은 같은 위치의 값들을 짝지음. ()로 묶은 여러 값은 변경 불가 튜플. zip은 같은 위치의 숫자와 부호를 묶습니다. 두 값을 각각 변수로 받습니다.
#         if positive:  # if는 조건이 참일 때 실행. positive는 True 또는 False입니다. True이면 아래 코드를 실행합니다.
#             answer += number  # +=는 더하거나 연결한 값을 저장. answer = answer + number와 같습니다.
#         else:  # else는 앞 조건들에 해당하지 않는 경우. positive가 False이면 실행합니다.
#             answer -= number  # -=는 빼서 저장. answer = answer - number와 같습니다.
#     return answer  # return은 결과를 돌려주고 함수 종료. 반복이 끝나면 합계를 반환하고 함수를 종료합니다.

# 풀이 요약
# zip으로 절댓값과 부호를 같은 위치끼리 읽는다. 부호가 참이면 더하고 거짓이면 빼서 원래 정수들의 합을 복원한다.
# 원소 N개: 시간 O(N), 보조 공간 O(1).
