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


# 같은 정답 코드 + 줄별 문법 설명
# 아래는 전체가 주석이므로 실행되지 않습니다.

# def solution(dartResult):  # def로 함수를 정의합니다. dartResult는 입력 문자열을 받습니다.
#     scores = []  # 각 회차의 점수를 저장할 빈 리스트입니다.
#     number = 0  # 읽은 숫자를 저장할 변수입니다.
#     powers = {"S": 1, "D": 2, "T": 3}  # 딕셔너리입니다. 보너스 문자와 제곱 횟수를 연결합니다.
#
#     for char in dartResult:  # 문자열에서 문자를 하나씩 꺼냅니다.
#         if char.isdigit():  # isdigit()은 숫자 문자인지 확인합니다.
#             number = number * 10 + int(char)  # int()로 정수로 바꿉니다. "1" 다음 "0"을 읽으면 1*10+0=10이 됩니다.
#         elif char in powers:  # elif는 앞 조건이 거짓일 때 검사합니다. in으로 딕셔너리에 해당 키가 있는지 확인합니다.
#             scores.append(number ** powers[char])  # **는 거듭제곱입니다. 예: 2**3은 8입니다. append()로 계산 결과를 추가합니다.
#             number = 0  # 다음 회차의 숫자를 읽기 위해 초기화합니다.
#         elif char == "*":  # ==로 스타상 문자인지 비교합니다.
#             scores[-1] *= 2  # [-1]은 마지막 원소입니다. *= 2는 기존 값에 2를 곱해 저장합니다.
#             if len(scores) >= 2:  # len()으로 직전 회차가 존재하는지 확인합니다.
#                 scores[-2] *= 2  # [-2]는 뒤에서 두 번째 원소입니다. 직전 점수도 두 배로 만듭니다.
#         elif char == "#":  # 아차상 문자일 때 실행합니다.
#             scores[-1] *= -1  # 현재 점수에 -1을 곱해 부호를 바꿉니다.
#
#     return sum(scores)  # sum()으로 세 점수를 더해 반환하고 함수를 종료합니다.