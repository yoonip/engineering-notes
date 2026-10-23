def solution(survey, choices):
    points = {char: 0 for char in "RTCFJMAN"}

    for pair, choice in zip(survey, choices):
        if choice < 4:
            points[pair[0]] += 4 - choice
        elif choice > 4:
            points[pair[1]] += choice - 4

    answer = ""

    for first, second in ["RT", "CF", "JM", "AN"]:
        if points[first] >= points[second]:
            answer += first
        else:
            answer += second

    return answer


# 같은 정답 코드 + 줄별 문법 설명
# 아래는 전체가 주석이므로 실행되지 않습니다.

# def solution(survey, choices):  # def는 함수 정의입니다. 질문과 응답 리스트를 매개변수로 받습니다.
#     points = {char: 0 for char in "RTCFJMAN"}  # 딕셔너리 컴프리헨션입니다. 각 글자를 키로, 0을 값으로 저장합니다.
#
#     for pair, choice in zip(survey, choices):  # zip은 같은 위치의 질문과 응답을 묶습니다. 두 값을 각각 변수로 받습니다.
#         if choice < 4:  # <는 작다는 비교입니다. 응답이 1, 2, 3이면 실행합니다.
#             points[pair[0]] += 4 - choice  # pair[0]은 질문의 첫 글자입니다. 해당 유형에 각각 3, 2, 1점을 더합니다.
#         elif choice > 4:  # elif는 앞 조건이 거짓일 때 검사합니다. 응답이 4면 어느 분기도 실행하지 않습니다.
#             points[pair[1]] += choice - 4  # pair[1]은 둘째 글자입니다. 응답 5, 6, 7에 각각 1, 2, 3점을 더합니다.
#
#     answer = ""  # 결과를 담을 빈 문자열입니다.
#
#     for first, second in ["RT", "CF", "JM", "AN"]:  # 두 글자 문자열을 각각 변수에 나눠 받습니다. 예: first="R", second="T".
#         if points[first] >= points[second]:  # >=는 크거나 같다는 비교입니다. 첫 글자가 사전순으로 앞서므로 동점도 처리합니다.
#             answer += first  # 문자열을 뒤에 붙여 저장합니다. answer = answer + first와 같습니다.
#         else:  # 둘째 유형의 점수가 더 높으면 실행합니다.
#             answer += second  # 둘째 글자를 결과 뒤에 붙입니다.
#
#     return answer  # 모든 비교가 끝나면 네 글자 문자열을 반환하고 함수를 종료합니다.