# 키패드 누르기

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/67256) · Level 1 · Python3

유형: 구현 · 맨해튼 거리

## 풀이 원리

각 숫자를 행·열 좌표로 바꿉니다. 왼쪽 열은 왼손, 오른쪽 열은 오른손으로 누르고 가운데 열은 두 손의 행 차이+열 차이를 비교합니다. 거리가 같을 때만 주로 쓰는 손을 고릅니다. 사용한 손의 위치는 목표 숫자 위치로 갱신합니다.

입력 숫자 N개: 시간 O(N), 결과 포함 공간 O(N).

## 공식 예제

입력 인수: `[[1, 3, 4, 5, 8, 2, 1, 4, 5, 9, 5], "right"]`

반환값: `"LRLLLRLLRRL"`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(numbers, hand):
    positions = {
        1: (0, 0), 2: (0, 1), 3: (0, 2),
        4: (1, 0), 5: (1, 1), 6: (1, 2),
        7: (2, 0), 8: (2, 1), 9: (2, 2),
        0: (3, 1)
    }
    left_pos = (3, 0)
    right_pos = (3, 2)
    answer = []
    for number in numbers:
        target = positions[number]
        if number in (1, 4, 7):
            used_hand = "L"
        elif number in (3, 6, 9):
            used_hand = "R"
        else:
            left_distance = abs(left_pos[0] - target[0]) + abs(left_pos[1] - target[1])
            right_distance = abs(right_pos[0] - target[0]) + abs(right_pos[1] - target[1])
            if left_distance < right_distance:
                used_hand = "L"
            elif left_distance > right_distance:
                used_hand = "R"
            elif hand == "left":
                used_hand = "L"
            else:
                used_hand = "R"
        if used_hand == "L":
            left_pos = target
        else:
            right_pos = target
        answer.append(used_hand)
    return "".join(answer)

# 전체 코드 줄별 설명
# def solution(numbers, hand):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. numbers: 누를 번호 목록, hand: "left" 또는 "right"
#     positions = {  # {}는 키:값을 저장하는 딕셔너리. =는 값 저장. 각 숫자와 그 숫자의 (행, 열) 좌표를 연결한 딕셔너리
#         1: (0, 0), 2: (0, 1), 3: (0, 2),  # ()로 묶은 여러 값은 변경 불가 튜플. 첫 번째 행의 숫자와 좌표
#         4: (1, 0), 5: (1, 1), 6: (1, 2),  # ()로 묶은 여러 값은 변경 불가 튜플. 두 번째 행의 숫자와 좌표
#         7: (2, 0), 8: (2, 1), 9: (2, 2),  # ()로 묶은 여러 값은 변경 불가 튜플. 세 번째 행의 숫자와 좌표
#         0: (3, 1)  # ()로 묶은 여러 값은 변경 불가 튜플. 숫자 0은 마지막 행의 가운데에 있음
#     }  # 딕셔너리 정의의 닫는 중괄호. 딕셔너리 정의 끝
#     left_pos = (3, 0)  # ()로 묶은 여러 값은 변경 불가 튜플. =는 값 저장. 왼손 시작 위치: "*"의 좌표
#     right_pos = (3, 2)  # ()로 묶은 여러 값은 변경 불가 튜플. =는 값 저장. 오른손 시작 위치: "#"의 좌표
#     answer = []  # []는 리스트. =는 값 저장. 번호를 누를 때마다 사용한 손 "L" 또는 "R"을 저장
#     for number in numbers:  # for·in은 원소를 차례로 꺼내는 반복문. 눌러야 할 번호를 순서대로 하나씩 꺼냄
#         target = positions[number]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 현재 누를 번호의 좌표. 예: 번호 5 → (1, 1)
#         if number in (1, 4, 7):  # if는 조건이 참일 때 실행. in은 포함 여부. ()로 묶은 여러 값은 변경 불가 튜플. 현재 번호가 왼쪽 열의 숫자라면
#             used_hand = "L"  # =는 값 저장. 왼손을 선택
#         elif number in (3, 6, 9):  # elif는 앞 조건이 거짓일 때 검사할 다음 조건. in은 포함 여부. ()로 묶은 여러 값은 변경 불가 튜플. 현재 번호가 오른쪽 열의 숫자라면
#             used_hand = "R"  # =는 값 저장. 오른손을 선택
#         else:  # else는 앞 조건들에 해당하지 않는 경우. 이번 번호를 오른손으로 눌렀다면
#             left_distance = abs(left_pos[0] - target[0]) + abs(left_pos[1] - target[1])  # abs는 절댓값. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 왼손 거리
#             right_distance = abs(right_pos[0] - target[0]) + abs(right_pos[1] - target[1])  # abs는 절댓값. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 오른손 거리
#             if left_distance < right_distance:  # if는 조건이 참일 때 실행. <는 작음 비교. 왼손이 더 가까우면
#                 used_hand = "L"  # =는 값 저장. 왼손을 선택
#             elif left_distance > right_distance:  # elif는 앞 조건이 거짓일 때 검사할 다음 조건. >는 큼 비교. 오른손이 더 가까우면
#                 used_hand = "R"  # =는 값 저장. 오른손을 선택
#             elif hand == "left":  # elif는 앞 조건이 거짓일 때 검사할 다음 조건. ==는 같음 비교. 두 거리가 같고, 왼손잡이라면
#                 used_hand = "L"  # =는 값 저장. 왼손을 선택
#             else:  # else는 앞 조건들에 해당하지 않는 경우. 이번 번호를 오른손으로 눌렀다면
#                 used_hand = "R"  # =는 값 저장. 오른손을 선택
#         if used_hand == "L":  # if는 조건이 참일 때 실행. ==는 같음 비교. 이번 번호를 왼손으로 눌렀다면
#             left_pos = target  # =는 값 저장. 왼손 위치만 누른 번호의 좌표로 변경
#         else:  # else는 앞 조건들에 해당하지 않는 경우. 이번 번호를 오른손으로 눌렀다면
#             right_pos = target  # =는 값 저장. 오른손 위치만 누른 번호의 좌표로 변경
#         answer.append(used_hand)  # append는 리스트 끝에 추가. 이번에 사용한 손을 결과 리스트 맨 뒤에 추가
#     return "".join(answer)  # return은 결과를 돌려주고 함수 종료. join은 문자열들을 구분자로 연결. ["L", "R", "L"]처럼 저장된 결과를 "LRL"로 연결해서 반환

# 풀이 요약
# 각 숫자를 행·열 좌표로 바꾼다. 왼쪽 열은 왼손, 오른쪽 열은 오른손으로 누르고 가운데 열은 두 손의 행 차이+열 차이를 비교한다. 거리가 같을 때만 주로 쓰는 손을 고른다. 사용한 손의 위치는 목표 숫자 위치로 갱신한다.
# 입력 숫자 N개: 시간 O(N), 결과 포함 공간 O(N).
```

## 확인한 범위

2026-10-16 02:01:43의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
