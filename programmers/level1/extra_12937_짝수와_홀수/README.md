# 짝수와 홀수

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12937) · Level 1 · Python3

유형: 기초 문법 · 조건 · 나머지

## 풀이 원리

2로 나눈 나머지가 0이면 짝수이고 아니면 홀수입니다. 문제에서 정한 문자열 Even 또는 Odd를 대소문자 그대로 반환합니다.

문제의 정수 범위에서 시간·보조 공간 O(1).

## 공식 예제

입력 인수: `[3]`

반환값: `"Odd"`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(num):
    if num % 2 == 0:
        return "Even"
    else:
        return "Odd"

# 전체 코드 줄별 설명
# def solution(num):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def로 함수를 정의합니다. num은 입력 정수를 받는 매개변수입니다.
#     if num % 2 == 0:  # if는 조건이 참일 때 실행. ==는 같음 비교. %는 나머지. %는 나머지 연산, ==는 같은지 비교입니다. 나머지가 0이면 짝수입니다.
#         return "Even"  # return은 결과를 돌려주고 함수 종료. 문자열 "Even"을 반환하고 함수를 종료합니다.
#     else:  # else는 앞 조건들에 해당하지 않는 경우. if 조건이 거짓, 즉 홀수일 때 실행합니다.
#         return "Odd"  # return은 결과를 돌려주고 함수 종료. 문자열 "Odd"를 반환하고 함수를 종료합니다.

# 풀이 요약
# 2로 나눈 나머지가 0이면 짝수이고 아니면 홀수다. 문제에서 정한 문자열 Even 또는 Odd를 대소문자 그대로 반환한다.
# 문제의 정수 범위에서 시간·보조 공간 O(1).
```

## 확인한 범위

2026-10-16 02:37:38의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
