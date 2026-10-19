# 시저 암호
# 분류: 문자 코드 / 나머지 연산
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/12926
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

def solution(s, n):
    answer = []

    for char in s:
        if char == " ":
            answer.append(char)
        elif char.isupper():
            shifted = (ord(char) - ord("A") + n) % 26
            answer.append(chr(ord("A") + shifted))
        else:
            shifted = (ord(char) - ord("a") + n) % 26
            answer.append(chr(ord("a") + shifted))

    return "".join(answer)


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# def solution(s, n):  # def로 함수를 정의합니다. s는 입력 문자열, n은 이동 칸 수를 받는 매개변수입니다.
#     answer = []  # 변환된 한 글자 문자열들을 차례로 저장할 빈 리스트입니다.
#
#     for char in s:  # for로 문자열의 글자를 하나씩 꺼냅니다.
#         if char == " ":  # ==는 같은지 비교입니다. 따옴표 안에 공백 하나가 있는 문자열과 비교합니다.
#             answer.append(char)  # append()로 공백을 그대로 리스트 뒤에 추가합니다.
#         elif char.isupper():  # elif는 앞 조건이 거짓일 때 검사합니다. isupper()는 대문자인지 확인합니다.
#             shifted = (ord(char) - ord("A") + n) % 26  # ord()는 문자 코드 정수를 구합니다. A를 빼서 0~25로 바꾸고 n을 더한 뒤 나머지로 순환시킵니다.
#             answer.append(chr(ord("A") + shifted))  # chr()는 문자 코드 정수를 문자로 바꿉니다. A의 코드에 새 위치를 더해 대문자로 복원합니다.
#         else:  # 입력은 영문자와 공백뿐이므로 남은 경우는 소문자입니다.
#             shifted = (ord(char) - ord("a") + n) % 26  # 소문자는 a의 코드를 기준으로 동일하게 계산합니다. %는 나머지 연산입니다.
#             answer.append(chr(ord("a") + shifted))  # 계산한 위치를 소문자로 바꾸어 리스트 뒤에 추가합니다.
#
#     return "".join(answer)  # join()은 리스트의 문자열들을 연결합니다. ""를 구분자로 쓰므로 사이에 아무것도 넣지 않고 합쳐 반환합니다.
#
