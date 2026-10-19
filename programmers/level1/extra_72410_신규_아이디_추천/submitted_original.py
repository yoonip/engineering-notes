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


# 같은 정답 코드 + 줄별 문법 설명
# 아래는 전체가 주석이므로 실행되지 않습니다.

# def solution(new_id):  # def로 함수를 정의합니다. new_id는 입력 문자열을 받습니다.
#     new_id = new_id.lower()  # [1단계] lower()로 소문자로 바꾼 문자열을 만들어 다시 저장합니다.
#     answer = ""  # 허용된 글자들을 모을 빈 문자열입니다.
#
#     for char in new_id:  # 입력 문자열에서 글자를 하나씩 꺼냅니다.
#         if char.isalnum() or char in "-_.":  # [2단계] 문자·숫자인지, 또는 허용 특수문자인지 검사합니다. or는 둘 중 하나가 참이면 참입니다.
#             answer += char  # 허용된 글자를 뒤에 붙입니다. answer = answer + char와 같습니다.
#
#     while ".." in answer:  # [3단계] ".."가 포함되어 있는 동안 반복합니다.
#         answer = answer.replace("..", ".")  # 두 마침표를 하나로 교체한 새 문자열을 다시 저장합니다.
#
#     answer = answer.strip(".")  # [4단계] strip(".")은 양끝의 마침표를 제거합니다. 중간은 그대로 둡니다.
#
#     if not answer:  # [5단계] 빈 문자열은 거짓으로 취급됩니다. not으로 뒤집어 비었을 때 실행합니다.
#         answer = "a"  # 빈 문자열 대신 "a"를 저장합니다.
#
#     answer = answer[:15].rstrip(".")  # [6단계] [:15]로 앞의 15글자를 남기고, rstrip(".")으로 오른쪽 끝 마침표를 제거합니다.
#
#     while len(answer) < 3:  # [7단계] len()은 길이입니다. 3글자 미만인 동안 반복합니다.
#         answer += answer[-1]  # [-1]은 마지막 글자입니다. 그 글자를 끝에 하나 더 붙입니다.
#
#     return answer  # 완성된 추천 아이디를 반환하고 함수를 종료합니다.