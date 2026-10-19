# 크레인 인형뽑기 게임

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/64061) · Level 1 · Python3

유형: 스택 · 격자 탐색

## 풀이 원리

선택한 열을 위에서 아래로 보며 첫 인형을 꺼내고 보드 칸을 0으로 바꾼다. 바구니 맨 위와 같으면 둘을 없애고 제거 수를 2 늘린다. 다르면 스택 끝에 넣는다. 한 번 꺼냈으면 열 탐색을 중단한다.

보드 높이 N, 이동 M번: 시간 O(NM), 바구니 공간 O(M). 보드를 직접 바꾼다.

## 공식 예제

입력 인수: `[[[0, 0, 0, 0, 0], [0, 0, 1, 0, 3], [0, 2, 5, 0, 1], [4, 2, 4, 4, 2], [3, 5, 1, 3, 1]], [1, 5, 3, 5, 1, 2, 1, 4]]`

반환값: `4`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있다.

## 코드와 줄별 설명

원본에는 `solution`이 3번 정의돼 있다. Python은 나중에 나온 같은 이름의 정의를 사용하므로 마지막 함수가 실제로 호출된다. 위 실행 부분도 원본의 정의 순서를 유지했다.

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(board, moves):
    basket = []
    answer = 0
    n = len(board)
    for move in moves:
        col = move - 1
        for row in range(n):
            if board[row][col] != 0:
                doll = board[row][col]
                board[row][col] = 0
                if len(basket) == 0:
                    basket.append(doll)
                else:
                    if basket[-1] == doll:
                        basket.pop()
                        answer += 2
                    else:
                        basket.append(doll)
                break
    return answer

def solution(board, moves):
    basket = []
    answer = 0
    n = len(board)
    for move in moves:
        col = move -1
        for row in range(n):
            if board[row][col] !=0:
                doll = board[row][col]
                board[row][col] = 0
                if len(basket) == 0:
                    basket.append(doll)
                else:
                    if basket[-1] ==doll:
                        basket.pop()
                        answer +=2
                    else:
                        basket.append(doll)
                break
    return answer

def solution(board, moves):
    basket = []
    answer = 0
    n = len(board)
    for move in moves:
        col = move -1
        for row in range(n):
            if board[row][col] !=0:
                doll = board[row][col]
                board[row][col] = 0
                if len(basket) == 0:
                    basket.append(doll)
                else:
                    if basket[-1] == doll:
                        basket.pop()
                        answer +=2
                    else:
                        basket.append(doll)
                break
    return answer

# 전체 코드 줄별 설명
# def solution(board, moves):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def로 함수를 정의합니다. 인형 배치와 크레인 명령 리스트를 받습니다.
#     basket = []  # []는 리스트. =는 값 저장. 빈 리스트입니다. 끝에 넣고 빼는 스택으로 사용합니다.
#     answer = 0  # =는 값 저장. 사라진 인형 수를 저장합니다.
#     n = len(board)  # len은 길이. =는 값 저장. len()으로 행 수를 구합니다.
#     for move in moves:  # for·in은 원소를 차례로 꺼내는 반복문. 크레인 명령을 순서대로 하나씩 꺼냅니다.
#         col = move - 1  # =는 값 저장. 명령의 열 번호는 1부터, 리스트 인덱스는 0부터이므로 1을 뺍니다.
#         for row in range(n):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. 0번 행부터 n-1번 행까지 위에서 아래로 검사합니다.
#             if board[row][col] != 0:  # if는 조건이 참일 때 실행. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. !=는 다름 비교. 선택한 열에서 비어 있지 않은 첫 칸인지 확인.
#                 doll = board[row][col]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 발견한 인형의 값을 저장합니다.
#                 board[row][col] = 0  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 뽑은 자리를 빈칸으로 바꿉니다.
#                 if len(basket) == 0:  # if는 조건이 참일 때 실행. len은 길이. ==는 같음 비교. 바구니에 인형이 하나도 없는지 확인.
#                     basket.append(doll)  # append는 리스트 끝에 추가. append()로 새 인형을 맨 뒤에 추가합니다.
#                 else:  # else는 앞 조건들에 해당하지 않는 경우. 바구니가 비었거나 마지막 인형이 다르면 실행합니다.
#                     if basket[-1] == doll:  # if는 조건이 참일 때 실행. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. ==는 같음 비교. 바구니 맨 위와 새 인형의 종류가 같은지 확인.
#                         basket.pop()  # pop은 지정 위치를 꺼내고 삭제, 생략하면 마지막. pop()으로 바구니의 마지막 인형을 제거합니다. 새 인형은 추가하지 않습니다.
#                         answer += 2  # +=는 더하거나 연결한 값을 저장. 기존 인형과 새 인형, 총 두 개가 사라지므로 2를 더합니다.
#                     else:  # else는 앞 조건들에 해당하지 않는 경우. 바구니가 비었거나 마지막 인형이 다르면 실행합니다.
#                         basket.append(doll)  # append는 리스트 끝에 추가. append()로 새 인형을 맨 뒤에 추가합니다.
#                 break  # break는 가장 가까운 반복문 종료. 안쪽 행 검사 반복문을 종료합니다. 한 명령에서 하나만 뽑고 다음 명령으로 갑니다.
#     return answer  # return은 결과를 돌려주고 함수 종료. 모든 명령을 처리한 뒤 사라진 인형 수를 반환합니다.
# 
# def solution(board, moves):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def로 함수를 정의합니다. 인형 배치와 크레인 명령 리스트를 받습니다.
#     basket = []  # []는 리스트. =는 값 저장. 빈 리스트입니다. 끝에 넣고 빼는 스택으로 사용합니다.
#     answer = 0  # =는 값 저장. 사라진 인형 수를 저장합니다.
#     n = len(board)  # len은 길이. =는 값 저장. len()으로 행 수를 구합니다.
#     for move in moves:  # for·in은 원소를 차례로 꺼내는 반복문. 크레인 명령을 순서대로 하나씩 꺼냅니다.
#         col = move -1  # =는 값 저장. 명령의 열 번호는 1부터, 리스트 인덱스는 0부터이므로 1을 뺍니다.
#         for row in range(n):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. 0번 행부터 n-1번 행까지 위에서 아래로 검사합니다.
#             if board[row][col] !=0:  # if는 조건이 참일 때 실행. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. !=는 다름 비교. 선택한 열에서 실제 인형이 있는지 확인.
#                 doll = board[row][col]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 발견한 인형의 값을 저장합니다.
#                 board[row][col] = 0  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 뽑은 자리를 빈칸으로 바꿉니다.
#                 if len(basket) == 0:  # if는 조건이 참일 때 실행. len은 길이. ==는 같음 비교. 바구니가 비었는지 확인.
#                     basket.append(doll)  # append는 리스트 끝에 추가. append()로 새 인형을 맨 뒤에 추가합니다.
#                 else:  # else는 앞 조건들에 해당하지 않는 경우. 바구니가 비었거나 마지막 인형이 다르면 실행합니다.
#                     if basket[-1] ==doll:  # if는 조건이 참일 때 실행. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. ==는 같음 비교. 맨 위 인형과 새 인형이 같은지 확인.
#                         basket.pop()  # pop은 지정 위치를 꺼내고 삭제, 생략하면 마지막. pop()으로 바구니의 마지막 인형을 제거합니다. 새 인형은 추가하지 않습니다.
#                         answer +=2  # +=는 더하거나 연결한 값을 저장. 기존 인형과 새 인형, 총 두 개가 사라지므로 2를 더합니다.
#                     else:  # else는 앞 조건들에 해당하지 않는 경우. 바구니가 비었거나 마지막 인형이 다르면 실행합니다.
#                         basket.append(doll)  # append는 리스트 끝에 추가. append()로 새 인형을 맨 뒤에 추가합니다.
#                 break  # break는 가장 가까운 반복문 종료. 안쪽 행 검사 반복문을 종료합니다. 한 명령에서 하나만 뽑고 다음 명령으로 갑니다.
#     return answer  # return은 결과를 돌려주고 함수 종료. 모든 명령을 처리한 뒤 사라진 인형 수를 반환합니다.
# 
# def solution(board, moves):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def로 함수를 정의합니다. 인형 배치와 크레인 명령 리스트를 받습니다.
#     basket = []  # []는 리스트. =는 값 저장. 빈 리스트입니다. 끝에 넣고 빼는 스택으로 사용합니다.
#     answer = 0  # =는 값 저장. 사라진 인형 수를 저장합니다.
#     n = len(board)  # len은 길이. =는 값 저장. len()으로 행 수를 구합니다.
#     for move in moves:  # for·in은 원소를 차례로 꺼내는 반복문. 크레인 명령을 순서대로 하나씩 꺼냅니다.
#         col = move -1  # =는 값 저장. 명령의 열 번호는 1부터, 리스트 인덱스는 0부터이므로 1을 뺍니다.
#         for row in range(n):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. 0번 행부터 n-1번 행까지 위에서 아래로 검사합니다.
#             if board[row][col] !=0:  # if는 조건이 참일 때 실행. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. !=는 다름 비교. 선택한 열의 첫 인형을 찾음.
#                 doll = board[row][col]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 발견한 인형의 값을 저장합니다.
#                 board[row][col] = 0  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 뽑은 자리를 빈칸으로 바꿉니다.
#                 if len(basket) == 0:  # if는 조건이 참일 때 실행. len은 길이. ==는 같음 비교. 바구니에 인형이 없는지 확인.
#                     basket.append(doll)  # append는 리스트 끝에 추가. append()로 새 인형을 맨 뒤에 추가합니다.
#                 else:  # else는 앞 조건들에 해당하지 않는 경우. 바구니가 비었거나 마지막 인형이 다르면 실행합니다.
#                     if basket[-1] == doll:  # if는 조건이 참일 때 실행. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. ==는 같음 비교. 바구니 맨 위와 새 인형을 비교.
#                         basket.pop()  # pop은 지정 위치를 꺼내고 삭제, 생략하면 마지막. pop()으로 바구니의 마지막 인형을 제거합니다. 새 인형은 추가하지 않습니다.
#                         answer +=2  # +=는 더하거나 연결한 값을 저장. 기존 인형과 새 인형, 총 두 개가 사라지므로 2를 더합니다.
#                     else:  # else는 앞 조건들에 해당하지 않는 경우. 바구니가 비었거나 마지막 인형이 다르면 실행합니다.
#                         basket.append(doll)  # append는 리스트 끝에 추가. append()로 새 인형을 맨 뒤에 추가합니다.
#                 break  # break는 가장 가까운 반복문 종료. 안쪽 행 검사 반복문을 종료합니다. 한 명령에서 하나만 뽑고 다음 명령으로 갑니다.
#     return answer  # return은 결과를 돌려주고 함수 종료. 모든 명령을 처리한 뒤 사라진 인형 수를 반환합니다.

# 풀이 요약
# 선택한 열을 위에서 아래로 보며 첫 인형을 꺼내고 보드 칸을 0으로 바꾼다. 바구니 맨 위와 같으면 둘을 없애고 제거 수를 2 늘린다. 다르면 스택 끝에 넣는다. 한 번 꺼냈으면 열 탐색을 중단한다.
# 보드 높이 N, 이동 M번: 시간 O(NM), 바구니 공간 O(M). 보드를 직접 바꾼다.
```

## 확인한 범위

2026-10-16 22:03:20의 Python3 제출 내역에서 정답 100/100을 확인했다. 원본은 그대로 보관했다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
