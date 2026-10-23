# 자릿수 더하기

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12931) · Level 1 · Python3

유형: 문자열 · 자릿수 합

## 풀이 원리

정수를 문자열로 바꾸면 각 자릿수를 하나씩 읽을 수 있습니다. 한 자리 문자를 int로 바꿔 누적하면 자릿수의 합이 됩니다.

자릿수 D: 시간·문자열 공간 O(D).

## 공식 예제

입력 인수: `[123]`

반환값: `6`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(n):
    answer = 0
    for digit in str(n):
        answer += int(digit)
    return answer

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def로 함수를 정의합니다. n은 입력 자연수를 받는 매개변수입니다.
#     answer = 0  # =는 값 저장. 자릿수 합을 0으로 시작합니다.
#     for digit in str(n):  # for·in은 원소를 차례로 꺼내는 반복문. str은 문자열 변환. str()로 정수를 문자열로 바꾸고, 글자를 하나씩 꺼냅니다.
#         answer += int(digit)  # int는 정수 변환. +=는 더하거나 연결한 값을 저장. int()로 글자를 정수로 바꾸어 더합니다. answer = answer + int(digit)과 같습니다.
#     return answer  # return은 결과를 돌려주고 함수 종료. 반복이 끝나면 자릿수 합을 반환하고 함수를 종료합니다.

# 풀이 요약
# 정수를 문자열로 바꾸면 각 자릿수를 하나씩 읽을 수 있다. 한 자리 문자를 int로 바꿔 누적하면 자릿수의 합이 된다.
# 자릿수 D: 시간·문자열 공간 O(D).
```

## 확인한 범위

2026-10-16 02:55:12의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
