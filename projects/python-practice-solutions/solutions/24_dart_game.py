# 다트 게임
# 분류: 문자열 파싱
# 공개 문제 링크: https://school.programmers.co.kr/learn/courses/30/lessons/17682
# AI 작성 학습 풀이입니다. 온라인 채점 통과를 확인한 제출물이 아닙니다.

def solution(dartResult):
    scores = []
    number = 0
    powers = {"S": 1, "D": 2, "T": 3}

    for char in dartResult:
        if char.isdigit():
            number = number * 10 + int(char)
        elif char in powers:
            scores.append(number ** powers[char])
            number = 0
        elif char == "*":
            scores[-1] *= 2
            if len(scores) >= 2:
                scores[-2] *= 2
        elif char == "#":
            scores[-1] *= -1

    return sum(scores)


# 같은 코드의 문법 설명: 아래 부분은 전체 주석입니다.
# def solution(dartResult):  # def로 함수를 정의합니다. dartResult는 점수 기록 문자열을 받는 매개변수입니다.
#     scores = []  # []는 빈 리스트입니다. 각 회차의 계산된 점수를 저장합니다.
#     number = 0  # 숫자 문자를 정수로 모을 변수입니다. =는 대입입니다.
#     powers = {"S": 1, "D": 2, "T": 3}  # 딕셔너리입니다. 보너스 문자를 키로, 제곱 횟수를 값으로 연결합니다.
#
#     for char in dartResult:  # for로 문자열의 문자를 하나씩 꺼내 char에 넣으며 반복합니다.
#         if char.isdigit():  # isdigit()은 숫자 문자인지 확인하여 True 또는 False를 반환합니다.
#             number = number * 10 + int(char)  # int()로 문자를 정수로 바꿉니다. "1" 다음 "0"을 읽으면 1*10+0=10이 됩니다.
#         elif char in powers:  # elif는 앞 조건이 거짓일 때 검사합니다. 딕셔너리에서 in은 키가 있는지 확인합니다.
#             scores.append(number ** powers[char])  # **는 거듭제곱 연산입니다. 딕셔너리[키]로 지수를 읽고 append()로 계산 결과를 추가합니다.
#             number = 0  # 다음 회차의 숫자를 읽기 전에 0으로 초기화합니다.
#         elif char == "*":  # ==는 같은지 비교합니다. 스타상 문자일 때 실행합니다.
#             scores[-1] *= 2  # [-1]은 마지막 원소입니다. *= 2는 기존 값에 2를 곱해 다시 저장합니다.
#             if len(scores) >= 2:  # len()은 원소 수입니다. 직전 회차가 존재하는지 확인합니다.
#                 scores[-2] *= 2  # [-2]는 뒤에서 두 번째 원소입니다. 직전 회차 점수도 두 배로 만듭니다.
#         elif char == "#":  # 아차상 문자일 때 실행합니다.
#             scores[-1] *= -1  # 마지막 점수에 -1을 곱해 부호를 반대로 바꿉니다.
#
#     return sum(scores)  # sum()은 리스트 원소들의 합을 구합니다. 그 정수를 반환하고 함수를 종료합니다.
#
