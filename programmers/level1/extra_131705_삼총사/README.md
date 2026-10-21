# 삼총사

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/131705) · Level 1 · Python3

유형: 완전탐색 · 조합

## 풀이 원리

인덱스를 i<j<k로 골라 서로 다른 세 학생의 모든 조합을 한 번씩 확인합니다. 세 수의 합이 0일 때만 셉니다. 순서를 바꾼 같은 세 사람을 다시 세지 않도록 각 반복의 시작값을 다음 인덱스로 둡니다.

학생 수 N: 시간 O(N³), 보조 공간 O(1).

## 공식 예제

입력 인수: `[[-2, 3, 0, 2, -5]]`

반환값: `2`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(number):
    n = len(number)
    answer = 0
    for i in range(n - 2):
        for j in range(i + 1, n - 1):
            for k in range(j + 1, n):
                if number[i] + number[j] + number[k] == 0:
                    answer += 1
    return answer

# 전체 코드 줄별 설명
# def solution(number):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def로 함수를 정의합니다. number는 학생 번호 리스트를 받습니다.
#     n = len(number)  # len은 길이. =는 값 저장. len()으로 학생 수를 구해 n에 저장합니다.
#     answer = 0  # =는 값 저장. 조건을 만족하는 조합의 개수를 0으로 시작합니다.
#     for i in range(n - 2):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. range(끝)은 끝을 제외합니다. 뒤에 두 명을 남기고 첫 학생을 고릅니다.
#         for j in range(i + 1, n - 1):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. i 다음 위치부터 고릅니다. 뒤에 한 명을 남깁니다.
#             for k in range(j + 1, n):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. j 다음 위치부터 마지막 인덱스 n-1까지 고릅니다.
#                 if number[i] + number[j] + number[k] == 0:  # if는 조건이 참일 때 실행. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. ==는 같음 비교. [인덱스]로 값을 읽습니다. ==는 같은지 비교합니다.
#                     answer += 1  # +=는 더하거나 연결한 값을 저장. answer = answer + 1과 같습니다.
#     return answer  # return은 결과를 돌려주고 함수 종료. 모든 반복이 끝난 뒤 개수를 반환하고 함수를 종료합니다.

# 풀이 요약
# 인덱스를 i<j<k로 골라 서로 다른 세 학생의 모든 조합을 한 번씩 확인한다. 세 수의 합이 0일 때만 센다. 순서를 바꾼 같은 세 사람을 다시 세지 않도록 각 반복의 시작값을 다음 인덱스로 둔다.
# 학생 수 N: 시간 O(N³), 보조 공간 O(1).
```

## 확인한 범위

2026-10-16 01:05:12의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
