# 하샤드 수

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12947) · Level 1 · Python3

유형: 수학 · 자릿수 합

## 풀이 원리

숫자를 문자열로 바꿔 자릿수마다 정수로 변환한 뒤 더합니다. 원래 수를 자릿수 합으로 나눈 나머지가 0이면 하샤드 수입니다. 비교식 자체가 True 또는 False를 만듭니다.

자릿수 D: 시간 O(D), 문자열 저장 공간 O(D).

## 공식 예제

입력 인수: `[10]`

반환값: `true`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(x):
    digit_sum = sum(map(int, str(x)))
    answer = (x % digit_sum == 0)
    return answer

# 전체 코드 줄별 설명
# def solution(x):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 자연수 x를 입력받는 함수
#     digit_sum = sum(map(int, str(x)))  # str은 문자열 변환. sum은 원소 합. map은 각 원소에 함수 적용. =는 값 저장. x를 문자열로 바꾸고, 각 문자를 정수로 변환한 뒤 모두 더함
#     answer = (x % digit_sum == 0)  # ==는 같음 비교. %는 나머지. =는 값 저장. x를 자릿수의 합으로 나눈 나머지가 0이면 True, 아니면 False
#     return answer  # return은 결과를 돌려주고 함수 종료. 하샤드 수인지 판단한 결과 반환

# 풀이 요약
# 숫자를 문자열로 바꿔 자릿수마다 정수로 변환한 뒤 더한다. 원래 수를 자릿수 합으로 나눈 나머지가 0이면 하샤드 수다. 비교식 자체가 True 또는 False를 만든다.
# 자릿수 D: 시간 O(D), 문자열 저장 공간 O(D).
```

## 확인한 범위

2026-10-16 02:46:25의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
