# [1차] 다트 게임

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/17682) · Level 1 · Python3

유형: 문자열 · 파싱 · 스택

## 풀이 원리

숫자 문자는 자리값을 누적해 10도 읽습니다. S·D·T를 만나면 해당 제곱을 점수 리스트에 저장합니다. 별표는 현재 점수와 이전 점수를 각각 2배, 아차상은 현재 점수만 음수로 바꿉니다. 세 점수를 합해 답을 만듭니다.

문자열 길이 L: 시간 O(L), 점수 저장 O(1). 던진 횟수는 3회입니다.

## 공식 예제

입력 인수: `["1S2D*3T"]`

반환값: `37`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
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

# 전체 코드 줄별 설명
# def solution(dartResult):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def로 함수를 정의합니다. dartResult는 입력 문자열을 받습니다.
#     scores = []  # []는 리스트. =는 값 저장. 각 회차의 점수를 저장할 빈 리스트입니다.
#     number = 0  # =는 값 저장. 다음 회차의 숫자를 읽기 위해 초기화합니다.
#     powers = {"S": 1, "D": 2, "T": 3}  # {}는 키:값을 저장하는 딕셔너리. =는 값 저장. 딕셔너리입니다. 보너스 문자와 제곱 횟수를 연결합니다.
#     for char in dartResult:  # for·in은 원소를 차례로 꺼내는 반복문. 문자열에서 문자를 하나씩 꺼냅니다.
#         if char.isdigit():  # if는 조건이 참일 때 실행. isdigit은 숫자 문자 여부 검사. isdigit()은 숫자 문자인지 확인합니다.
#             number = number * 10 + int(char)  # int는 정수 변환. =는 값 저장. int()로 정수로 바꿉니다. "1" 다음 "0"을 읽으면 1*10+0=10이 됩니다.
#         elif char in powers:  # elif는 앞 조건이 거짓일 때 검사할 다음 조건. in은 포함 여부. elif는 앞 조건이 거짓일 때 검사합니다. in으로 딕셔너리에 해당 키가 있는지 확인합니다.
#             scores.append(number ** powers[char])  # append는 리스트 끝에 추가. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. **는 거듭제곱. **는 거듭제곱입니다. 예: 2**3은 8입니다. append()로 계산 결과를 추가합니다.
#             number = 0  # =는 값 저장. 다음 회차의 숫자를 읽기 위해 초기화합니다.
#         elif char == "*":  # elif는 앞 조건이 거짓일 때 검사할 다음 조건. ==는 같음 비교. ==로 스타상 문자인지 비교합니다.
#             scores[-1] *= 2  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. *=는 곱해 저장. [-1]은 마지막 원소입니다. *= 2는 기존 값에 2를 곱해 저장합니다.
#             if len(scores) >= 2:  # if는 조건이 참일 때 실행. len은 길이. >=는 이상 비교. len()으로 직전 회차가 존재하는지 확인합니다.
#                 scores[-2] *= 2  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. *=는 곱해 저장. [-2]는 뒤에서 두 번째 원소입니다. 직전 점수도 두 배로 만듭니다.
#         elif char == "#":  # elif는 앞 조건이 거짓일 때 검사할 다음 조건. ==는 같음 비교. 아차상 문자일 때 실행합니다.
#             scores[-1] *= -1  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. *=는 곱해 저장. 현재 점수에 -1을 곱해 부호를 바꿉니다.
#     return sum(scores)  # return은 결과를 돌려주고 함수 종료. sum은 원소 합. sum()으로 세 점수를 더해 반환하고 함수를 종료합니다.

# 풀이 요약
# 숫자 문자는 자리값을 누적해 10도 읽는다. S·D·T를 만나면 해당 제곱을 점수 리스트에 저장한다. 별표는 현재 점수와 이전 점수를 각각 2배, 아차상은 현재 점수만 음수로 바꾼다. 세 점수를 합해 답을 만든다.
# 문자열 길이 L: 시간 O(L), 점수 저장 O(1). 던진 횟수는 3회다.
```

## 확인한 범위

2026-10-16 02:11:12의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
