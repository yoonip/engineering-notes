def solution(n):
    answer = 0

    for digit in str(n):
        answer += int(digit)

    return answer


# 같은 정답 코드 + 줄별 문법 설명
# 아래는 전체가 주석이므로 실행되지 않습니다.

# def solution(n):  # def로 함수를 정의합니다. n은 입력 자연수를 받는 매개변수입니다.
#     answer = 0  # 자릿수 합을 0으로 시작합니다.
#
#     for digit in str(n):  # str()로 정수를 문자열로 바꾸고, 글자를 하나씩 꺼냅니다.
#         answer += int(digit)  # int()로 글자를 정수로 바꾸어 더합니다. answer = answer + int(digit)과 같습니다.
#
#     return answer  # 반복이 끝나면 자릿수 합을 반환하고 함수를 종료합니다.