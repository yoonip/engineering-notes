# 정수 내림차순으로 배치하기

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12933) · Level 1 · Python3

유형: 문자열 · 정렬

## 풀이 원리

자릿수 문자를 리스트에 모아 오름차순 정렬한 뒤 뒤집습니다. 같은 자릿수들을 큰 수부터 앞에 배치해야 가장 큰 수가 됩니다. 이어 붙인 문자열을 int로 바꿔 반환합니다.

자릿수 D: 정렬 O(D log D), 반복 문자열 연결까지 고려한 시간 상한 O(D²), 공간 O(D).

## 공식 예제

입력 인수: `[118372]`

반환값: `873211`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(n):
    digits = []
    text = str(n)
    for digit in text:
        digits.append(digit)
    digits.sort()
    digits.reverse()
    answer = ""
    for digit in digits:
        answer = answer + digit
    return int(answer)

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 정수 n을 입력받는 함수
#     digits = []  # []는 리스트. =는 값 저장. 각 자릿수 문자를 모을 리스트.
#     text = str(n)  # str은 문자열 변환. =는 값 저장. 정수를 자릿수 문자열로 변환.
#     for digit in text:  # for·in은 원소를 차례로 꺼내는 반복문. 왼쪽부터 각 자릿수 문자를 읽음.
#         digits.append(digit)  # append는 리스트 끝에 추가. 자릿수 문자를 리스트에 추가.
#     digits.sort()  # sort는 원래 리스트 정렬. 자릿수를 작은 순서로 정렬.
#     digits.reverse()  # reverse는 원래 리스트 순서 반전. 순서를 뒤집어 큰 자릿수가 앞에 오게 함.
#     answer = ""  # =는 값 저장. 결과 문자열 초기화.
#     for digit in digits:  # for·in은 원소를 차례로 꺼내는 반복문. 내림차순 자릿수를 읽음.
#         answer = answer + digit  # =는 값 저장. 현재 자릿수를 결과 뒤에 연결.
#     return int(answer)  # return은 결과를 돌려주고 함수 종료. int는 정수 변환. 완성된 숫자 문자열을 정수로 반환.

# 풀이 요약
# 자릿수 문자를 리스트에 모아 오름차순 정렬한 뒤 뒤집는다. 같은 자릿수들을 큰 수부터 앞에 배치해야 가장 큰 수가 된다. 이어 붙인 문자열을 int로 바꿔 반환한다.
# 자릿수 D: 정렬 O(D log D), 반복 문자열 연결까지 고려한 시간 상한 O(D²), 공간 O(D).
```

## 확인한 범위

2026-10-16 14:01:55의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
