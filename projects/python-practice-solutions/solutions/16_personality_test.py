# 성격 유형 검사하기
# 분류: 해시 / 집계
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/118666
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

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


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# def solution(survey, choices):  # def로 함수를 정의합니다. 두 매개변수로 질문 리스트와 응답 리스트를 받습니다.
#     points = {char: 0 for char in "RTCFJMAN"}  # 딕셔너리 컴프리헨션입니다. 글자를 키, 숫자 0을 값으로 저장합니다. 예: {"R":0, "T":0, ...}.
#
#     for pair, choice in zip(survey, choices):  # zip은 두 리스트의 같은 위치 원소들을 튜플로 묶습니다. 두 값을 각각 pair와 choice로 받습니다.
#         if choice < 4:  # <는 작다는 비교입니다. 1,2,3을 선택했을 때 실행합니다.
#             points[pair[0]] += 4 - choice  # pair[0]은 질문의 첫 글자입니다. 해당 키의 점수에 3,2,1 중 하나를 더합니다.
#         elif choice > 4:  # elif는 앞 조건이 거짓일 때 검사합니다. 응답이 4면 두 분기 모두 실행하지 않습니다.
#             points[pair[1]] += choice - 4  # pair[1]은 둘째 글자입니다. 해당 키의 점수에 1,2,3 중 하나를 더합니다.
#
#     answer = ""  # ""는 빈 문자열입니다. 결과 글자 네 개를 여기에 붙입니다.
#
#     for first, second in ["RT", "CF", "JM", "AN"]:  # 두 글자 문자열을 각각 first와 second에 언패킹합니다. 예: "RT" → first="R", second="T".
#         if points[first] >= points[second]:  # >=는 크거나 같다는 비교입니다. 각 쌍의 첫 글자가 사전순으로 앞서므로 동점도 여기서 처리합니다.
#             answer += first  # 문자열 +=는 이어 붙여 다시 저장합니다. answer = answer + first와 같습니다.
#         else:  # 앞 조건이 거짓, 즉 둘째 유형의 점수가 더 높을 때 실행합니다.
#             answer += second  # 둘째 글자를 결과 문자열 뒤에 붙입니다.
#
#     return answer  # 두 반복문을 모두 끝낸 뒤 네 글자 문자열을 반환하고 함수를 종료합니다.
#
