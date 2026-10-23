# 약수의 개수와 덧셈

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/77884) · Level 1 · Python3

유형: 정수론 · 약수

## 풀이 원리

각 수를 1부터 자기 자신까지 나눠 나머지가 0인 약수를 셉니다. 약수 개수가 짝수면 더하고 홀수면 뺍니다. 이 제출본은 제곱수 판정 공식 대신 약수를 직접 세는 구현입니다.

구간 [L,R]: 시간 상한 O((R-L+1)R), 보조 공간 O(1).

## 공식 예제

입력 인수: `[13, 17]`

반환값: `43`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(left, right):
    answer = 0
    for number in range(left, right + 1):
        count = 0
        for divisor in range(1, number + 1):
            if number % divisor == 0:
                count += 1
        if count % 2 == 0:
            answer += number
        else:
            answer -= number
    return answer

# 전체 코드 줄별 설명
# def solution(left, right):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def로 함수를 정의합니다. 두 매개변수로 검사할 구간의 양 끝값을 받습니다.
#     answer = 0  # =는 값 저장. 더하고 뺀 결과를 저장할 변수입니다.
#     for number in range(left, right + 1):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. range는 끝값을 제외하므로 +1하여 right까지 포함합니다.
#         count = 0  # =는 값 저장. 현재 수의 약수 개수입니다. number가 바뀔 때마다 0으로 초기화합니다.
#         for divisor in range(1, number + 1):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. 1부터 현재 수까지 하나씩 나눠 봅니다.
#             if number % divisor == 0:  # if는 조건이 참일 때 실행. ==는 같음 비교. %는 나머지. %는 나머지 연산입니다. 나머지가 0이면 divisor는 약수입니다.
#                 count += 1  # +=는 더하거나 연결한 값을 저장. count = count + 1과 같습니다. 약수 개수를 늘립니다.
#         if count % 2 == 0:  # if는 조건이 참일 때 실행. ==는 같음 비교. %는 나머지. 약수 개수를 2로 나눈 나머지가 0이면 짝수입니다.
#             answer += number  # +=는 더하거나 연결한 값을 저장. 약수 개수가 아니라 원래 수를 결과에 더합니다.
#         else:  # else는 앞 조건들에 해당하지 않는 경우. 약수 개수가 홀수일 때 실행합니다.
#             answer -= number  # -=는 빼서 저장. answer = answer - number와 같습니다.
#     return answer  # return은 결과를 돌려주고 함수 종료. 모든 수를 처리한 뒤 결과를 반환하고 함수를 종료합니다.

# 풀이 요약
# 각 수를 1부터 자기 자신까지 나눠 나머지가 0인 약수를 센다. 약수 개수가 짝수면 더하고 홀수면 뺀다. 이 제출본은 제곱수 판정 공식 대신 약수를 직접 세는 구현이다.
# 구간 [L,R]: 시간 상한 O((R-L+1)R), 보조 공간 O(1).
```

## 확인한 범위

2026-10-16 01:51:44의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
