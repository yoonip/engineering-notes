# 둘만의 암호
# 분류: 문자열 / 나머지 연산
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/155652
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

def solution(s, skip, index):
    alphabet = ""

    for char in "abcdefghijklmnopqrstuvwxyz":
        if char not in skip:
            alphabet += char

    answer = ""

    for char in s:
        position = alphabet.index(char)
        next_position = (position + index) % len(alphabet)
        answer += alphabet[next_position]

    return answer


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# def solution(s, skip, index):  # def로 함수를 정의합니다. 괄호 안의 세 변수는 입력을 받는 매개변수입니다.
#     alphabet = ""  # =는 대입입니다. ""는 글자가 하나도 없는 빈 문자열입니다.
#
#     for char in "abcdefghijklmnopqrstuvwxyz":  # for로 문자열의 글자를 하나씩 꺼내 char에 넣으며 반복합니다.
#         if char not in skip:  # not in은 포함되지 않았는지 검사합니다. skip에 없는 글자일 때만 실행합니다.
#             alphabet += char  # 문자열을 이어 붙여 다시 저장합니다. alphabet = alphabet + char와 같습니다.
#
#     answer = ""  # 변환한 글자들을 차례로 붙일 빈 문자열을 만듭니다.
#
#     for char in s:  # 입력 문자열 s에서 글자를 하나씩 꺼냅니다. 중복된 글자도 각각 처리합니다.
#         position = alphabet.index(char)  # 문자열.index(글자)는 그 글자의 위치 번호를 반환합니다. 위치는 0부터 시작합니다.
#         next_position = (position + index) % len(alphabet)  # len은 길이, %는 나머지입니다. 예: 길이가 22면 위치 22는 0으로 돌아옵니다.
#         answer += alphabet[next_position]  # 문자열[위치]로 글자 하나를 읽어 정답 문자열 뒤에 붙입니다.
#
#     return answer  # return은 완성된 문자열을 반환하고 함수 전체를 종료합니다. 두 번째 for문 바깥에 둡니다.
