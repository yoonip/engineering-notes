def solution(n):
    answer = 0
    for digit in str(n):
        answer += int(digit)
    return answer

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def로 함수를 정의합니다. n은 입력 자연수를 받는 매개변수입니다.
#     answer = 0  # =는 값 저장. 자릿수 합을 0으로 시작합니다.
#     for digit in str(n):  # for·in은 원소를 차례로 꺼내는 반복문. str은 문자열 변환. str()로 정수를 문자열로 바꾸고, 글자를 하나씩 꺼냅니다.
#         answer += int(digit)  # int는 정수 변환. +=는 더하거나 연결한 값을 저장. int()로 글자를 정수로 바꾸어 더합니다. answer = answer + int(digit)과 같습니다.
#     return answer  # return은 결과를 돌려주고 함수 종료. 반복이 끝나면 자릿수 합을 반환하고 함수를 종료합니다.

# 풀이 요약
# 정수를 문자열로 바꾸면 각 자릿수를 하나씩 읽을 수 있다. 한 자리 문자를 int로 바꿔 누적하면 자릿수의 합이 된다.
# 자릿수 D: 시간·문자열 공간 O(D).
