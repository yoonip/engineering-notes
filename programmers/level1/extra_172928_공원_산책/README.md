# 공원 산책

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/172928) · Level 1 · Python3

유형: 구현 · 격자 시뮬레이션

## 풀이 원리

시작점을 찾고 방향별 행·열 변화량을 저장합니다. 명령은 임시 좌표에서 한 칸씩 시험합니다. 중간에 경계나 장애물을 만나면 명령 전체를 무효로 하고, 전부 통과했을 때만 실제 좌표를 바꿉니다. 도착점만 검사하면 중간 장애물을 놓칩니다.

지도 H×W, 명령 거리 합 D: 시간 O(HW+D), 보조 공간 O(1).

## 공식 예제

입력 인수: `[["SOO", "OOO", "OOO"], ["E 2", "S 2", "W 1"]]`

반환값: `[2, 1]`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(park, routes):
    height = len(park)
    width = len(park[0])
    row, col = 0, 0
    for r, line in enumerate(park):
        if "S" in line:
            row, col = r, line.index("S")
            break
    directions = {
        "N": (-1, 0),
        "S": (1, 0),
        "W": (0, -1),
        "E": (0, 1),
    }
    for route in routes:
        direction, distance = route.split()
        distance = int(distance)
        dr, dc = directions[direction]
        next_row, next_col = row, col
        valid = True
        for _ in range(distance):
            next_row += dr
            next_col += dc
            if not (0 <= next_row < height and 0 <= next_col < width):
                valid = False
                break
            if park[next_row][next_col] == "X":
                valid = False
                break
        if valid:
            row, col = next_row, next_col
    return [row, col]

# 전체 코드 줄별 설명
# def solution(park, routes):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 공원 지도와 이동 명령을 입력받음.
#     height = len(park)  # len은 길이. =는 값 저장. 지도 행 수.
#     width = len(park[0])  # len은 길이. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 지도 열 수.
#     row, col = 0, 0  # =는 값 저장. 시작 좌표를 담을 변수 초기화.
#     for r, line in enumerate(park):  # for·in은 원소를 차례로 꺼내는 반복문. enumerate는 인덱스·값을 함께 제공. ()로 묶은 여러 값은 변경 불가 튜플. 각 행 번호와 문자열을 순회.
#         if "S" in line:  # if는 조건이 참일 때 실행. in은 포함 여부. 해당 행에 시작 표시 S가 있는지 확인.
#             row, col = r, line.index("S")  # index는 값이 처음 나오는 위치. ()로 묶은 여러 값은 변경 불가 튜플. =는 값 저장. S의 행·열 좌표 저장.
#             break  # break는 가장 가까운 반복문 종료. 시작점을 찾았으므로 탐색 종료.
#     directions = {  # {}는 키:값을 저장하는 딕셔너리. =는 값 저장. 방향 이름을 행·열 변화량에 연결할 딕셔너리.
#         "N": (-1, 0),  # ()로 묶은 여러 값은 변경 불가 튜플. 북쪽은 행 -1, 열 0.
#         "S": (1, 0),  # ()로 묶은 여러 값은 변경 불가 튜플. 남쪽은 행 +1, 열 0.
#         "W": (0, -1),  # ()로 묶은 여러 값은 변경 불가 튜플. 서쪽은 행 0, 열 -1.
#         "E": (0, 1),  # ()로 묶은 여러 값은 변경 불가 튜플. 동쪽은 행 0, 열 +1.
#     }  # 딕셔너리 정의의 닫는 중괄호. 방향 정의 마침.
#     for route in routes:  # for·in은 원소를 차례로 꺼내는 반복문. 이동 명령을 순서대로 처리.
#         direction, distance = route.split()  # split은 구분자로 문자열 분리. ()로 묶은 여러 값은 변경 불가 튜플. =는 값 저장. 명령을 방향 문자열과 거리 문자열로 나눔.
#         distance = int(distance)  # int는 정수 변환. =는 값 저장. 거리를 계산 가능한 정수로 바꿈.
#         dr, dc = directions[direction]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 해당 방향의 행·열 변화량을 읽음.
#         next_row, next_col = row, col  # =는 값 저장. 명령을 시험할 임시 위치를 현재 위치로 시작.
#         valid = True  # =는 값 저장. True·False는 참·거짓. 이동 가능하다고 가정.
#         for _ in range(distance):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. 명령 거리만큼 한 칸씩 시험 이동.
#             next_row += dr  # +=는 더하거나 연결한 값을 저장. 임시 행 좌표 이동.
#             next_col += dc  # +=는 더하거나 연결한 값을 저장. 임시 열 좌표 이동.
#             if not (0 <= next_row < height and 0 <= next_col < width):  # if는 조건이 참일 때 실행. not은 참·거짓 반전. and는 두 조건 모두 참. <=는 이하 비교. <는 작음 비교. 지도를 벗어났는지 확인.
#                 valid = False  # =는 값 저장. True·False는 참·거짓. 명령을 무효로 표시.
#                 break  # break는 가장 가까운 반복문 종료. 남은 시험 이동 중단.
#             if park[next_row][next_col] == "X":  # if는 조건이 참일 때 실행. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. ==는 같음 비교. 도중에 장애물 X를 만났는지 확인.
#                 valid = False  # =는 값 저장. True·False는 참·거짓. 이 명령을 무효로 표시.
#                 break  # break는 가장 가까운 반복문 종료. 남은 시험 이동 중단.
#         if valid:  # if는 조건이 참일 때 실행. 모든 중간 칸을 지나갈 수 있는지 확인.
#             row, col = next_row, next_col  # =는 값 저장. 성공한 명령에만 실제 위치를 갱신.
#     return [row, col]  # return은 결과를 돌려주고 함수 종료. []는 리스트. 마지막 행·열 좌표를 리스트로 반환.

# 풀이 요약
# 시작점을 찾고 방향별 행·열 변화량을 저장한다. 명령은 임시 좌표에서 한 칸씩 시험한다. 중간에 경계나 장애물을 만나면 명령 전체를 무효로 하고, 전부 통과했을 때만 실제 좌표를 바꾼다. 도착점만 검사하면 중간 장애물을 놓친다.
# 지도 H×W, 명령 거리 합 D: 시간 O(HW+D), 보조 공간 O(1).
```

## 확인한 범위

2026-10-16 00:16:17의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
