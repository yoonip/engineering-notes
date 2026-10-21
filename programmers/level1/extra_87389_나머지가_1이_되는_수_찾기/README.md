# 나머지가 1이 되는 수 찾기

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/87389) · Level 1 · Python3

유형: 완전탐색 · 나머지

## 풀이 원리

2부터 증가시키며 n을 나눈 나머지가 1인지 검사합니다. 처음 만족하는 수를 바로 반환하므로 가장 작은 답입니다. 문제의 n≥3 조건에서 n-1은 항상 후보가 되어 답이 존재합니다.

입력 N: 시간 상한 O(N), 보조 공간 O(1).

## 공식 예제

입력 인수: `[10]`

반환값: `3`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(n):
    for x in range(2, n):
        if n % x == 1:
            return x

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def로 함수를 정의합니다. n은 입력 정수를 받는 매개변수입니다.
#     for x in range(2, n):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. range(시작, 끝)은 끝을 제외합니다. x에 2부터 n-1까지 차례로 넣습니다.
#         if n % x == 1:  # if는 조건이 참일 때 실행. ==는 같음 비교. %는 나머지. %는 나머지 연산, ==는 같은지 비교하는 연산입니다.
#             return x  # return은 결과를 돌려주고 함수 종료. x를 반환하고 함수 전체를 종료합니다. 처음 찾은 값이 가장 작은 값입니다.

# 풀이 요약
# 2부터 증가시키며 n을 나눈 나머지가 1인지 검사한다. 처음 만족하는 수를 바로 반환하므로 가장 작은 답이다. 문제의 n≥3 조건에서 n-1은 항상 후보가 되어 답이 존재한다.
# 입력 N: 시간 상한 O(N), 보조 공간 O(1).
```

## 확인한 범위

2026-10-16 01:40:43의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
