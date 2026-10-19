# 문자열을 정수로 바꾸기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12925) · Level 1 · Python3

유형: 기초 문법 · 자료형 변환

## 풀이 원리

int는 숫자로 된 문자열을 정수로 해석하며 앞의 + 또는 - 부호도 처리합니다. 별도로 부호를 잘라 계산하지 않아도 됩니다.

입력 문자열 길이 L을 읽어 변환합니다. 문제의 짧은 정수 범위에서 시간 O(L).

## 공식 예제

입력 인수: `["1234"]`

반환값: `1234`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(s):
    number = int(s)
    return number

# 전체 코드 줄별 설명
# def solution(s):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 부호를 포함할 수 있는 숫자 문자열을 입력받음.
#     number = int(s)  # int는 정수 변환. =는 값 저장. 문자열을 정수로 해석.
#     return number  # return은 결과를 돌려주고 함수 종료. 변환한 정수를 반환.

# 풀이 요약
# int는 숫자로 된 문자열을 정수로 해석하며 앞의 + 또는 - 부호도 처리한다. 별도로 부호를 잘라 계산하지 않아도 된다.
# 입력 문자열 길이 L을 읽어 변환한다. 문제의 짧은 정수 범위에서 시간 O(L).
```

## 확인한 범위

2026-10-16 13:01:53의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
