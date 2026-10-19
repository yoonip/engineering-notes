# 신규 아이디 추천
# 분류: 문자열 처리
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/72410
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

def solution(new_id):
    new_id = new_id.lower()
    answer = ""

    for char in new_id:
        if char.isalnum() or char in "-_.":
            answer += char

    while ".." in answer:
        answer = answer.replace("..", ".")

    answer = answer.strip(".")

    if not answer:
        answer = "a"

    answer = answer[:15].rstrip(".")

    while len(answer) < 3:
        answer += answer[-1]

    return answer


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# def solution(new_id):  # def로 함수를 정의합니다. new_id는 입력 문자열을 받는 매개변수입니다.
#     new_id = new_id.lower()  # [1단계] lower()는 소문자로 바꾼 새 문자열을 반환합니다. =로 다시 저장합니다.
#     answer = ""  # ""는 빈 문자열입니다. 허용된 글자들을 붙일 변수입니다.
#
#     for char in new_id:  # for로 문자열의 글자를 하나씩 꺼내 char에 넣으며 반복합니다.
#         if char.isalnum() or char in "-_.":  # [2단계] isalnum()은 문자나 숫자인지 검사합니다. or는 둘 중 하나가 참이면 참, in은 포함 여부입니다.
#             answer += char  # answer = answer + char와 같습니다. 허용된 글자를 뒤에 붙입니다.
#
#     while ".." in answer:  # [3단계] 연속된 두 마침표가 존재하는 동안 반복합니다. while은 조건이 참인 동안 반복하는 문법입니다.
#         answer = answer.replace("..", ".")  # replace(기존,새값)로 두 마침표를 하나로 바꿉니다. 결과는 새 문자열이므로 다시 대입합니다.
#
#     answer = answer.strip(".")  # [4단계] strip(".")은 문자열 양끝의 마침표를 제거합니다. 중간 마침표는 남깁니다.
#
#     if not answer:  # [5단계] 빈 문자열은 조건에서 거짓입니다. not으로 뒤집으면 비었을 때 참입니다.
#         answer = "a"  # 비어 있으면 문자열 "a"를 대입합니다.
#
#     answer = answer[:15].rstrip(".")  # [6단계] [:15]는 처음부터 인덱스 14까지의 슬라이싱입니다. rstrip(".")은 자른 결과의 오른쪽 끝 마침표를 제거합니다.
#
#     while len(answer) < 3:  # [7단계] len()은 문자열 길이입니다. 길이가 3 미만인 동안 반복합니다.
#         answer += answer[-1]  # [-1]은 마지막 글자입니다. 그 글자를 끝에 하나 더 붙입니다.
#
#     return answer  # 완성된 추천 아이디를 반환하고 함수를 종료합니다.
#
