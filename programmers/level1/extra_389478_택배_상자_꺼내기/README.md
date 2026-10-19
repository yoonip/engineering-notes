# 택배 상자 꺼내기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/389478) · Level 1 · Python3

유형: 구현 · 좌표 변환

## 풀이 원리

상자 번호에서 행과 열을 구하되 홀수 행은 오른쪽부터 쌓이므로 열을 뒤집는다. 목표 상자와 같은 열에서 위쪽 행의 상자 번호를 계산한다. 마지막 행에서 n을 넘는 번호는 빈칸이므로 세지 않는다.

행 수 R=ceil(n/w): 시간 O(R), 보조 공간 O(1).

## 공식 예제

입력 인수: `[22, 6, 8]`

반환값: `3`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(n, w, num):
    row = (num - 1) // w
    col = (num - 1) % w
    if row % 2 == 1:
        col = w - 1 - col
    answer = 0
    for r in range(row, (n + w - 1) // w):
        if r % 2 == 0:
            box = r * w + col + 1
        else:
            box = (r + 1) * w - col
        if box <= n:
            answer += 1
    return answer

# 전체 코드 줄별 설명
# def solution(n, w, num):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 상자 총수·가로 칸 수·찾을 번호를 입력받음.
#     row = (num - 1) // w  # //는 내림한 정수 몫. =는 값 저장. 상자 번호를 0부터 시작하는 행 번호로 변환.
#     col = (num - 1) % w  # %는 나머지. =는 값 저장. 행 안의 순서 번호 계산.
#     if row % 2 == 1:  # if는 조건이 참일 때 실행. ==는 같음 비교. %는 나머지. 지그재그에서 홀수 행인지 검사.
#         col = w - 1 - col  # =는 값 저장. 오른쪽부터 쌓은 행의 순서를 실제 열로 변환.
#     answer = 0  # =는 값 저장. 꺼낼 상자 수 초기화.
#     for r in range(row, (n + w - 1) // w):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. //는 내림한 정수 몫. 목표 행부터 마지막 상자 행까지 같은 열을 확인.
#         if r % 2 == 0:  # if는 조건이 참일 때 실행. ==는 같음 비교. %는 나머지. 왼쪽에서 오른쪽으로 쌓은 행인지 검사.
#             box = r * w + col + 1  # =는 값 저장. 이 행·열에 해당하는 상자 번호 계산.
#         else:  # else는 앞 조건들에 해당하지 않는 경우. 오른쪽에서 왼쪽으로 쌓은 행인 경우.
#             box = (r + 1) * w - col  # =는 값 저장. 반대 방향의 상자 번호 계산.
#         if box <= n:  # if는 조건이 참일 때 실행. <=는 이하 비교. 마지막 불완전한 행에서도 실제 상자가 있는지 확인.
#             answer += 1  # +=는 더하거나 연결한 값을 저장. 목표 상자와 그 위의 상자를 한 개 셈.
#     return answer  # return은 결과를 돌려주고 함수 종료. 꺼내야 하는 상자 수 반환.

# 풀이 요약
# 상자 번호에서 행과 열을 구하되 홀수 행은 오른쪽부터 쌓이므로 열을 뒤집는다. 목표 상자와 같은 열에서 위쪽 행의 상자 번호를 계산한다. 마지막 행에서 n을 넘는 번호는 빈칸이므로 세지 않는다.
# 행 수 R=ceil(n/w): 시간 O(R), 보조 공간 O(1).
```

## 확인한 범위

2026-10-15 23:38:08의 Python3 제출 내역에서 정답 100/100을 확인했다. 원본은 그대로 보관했다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
