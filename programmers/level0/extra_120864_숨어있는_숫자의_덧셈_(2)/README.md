# 숨어있는 숫자의 덧셈 (2)

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120864) · Level 0 · Python3

## 풀이

연속된 숫자는 유지하고 글자만 공백으로 바꿔 여러 자리 자연수 단위로 더합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(my_string):
    separated = ''.join(char if char.isdigit() else ' ' for char in my_string)
    return sum(map(int, separated.split()))

# 전체 코드 줄별 설명
# def solution(my_string):  # def는 함수 정의. 문자와 여러 자리 숫자가 섞인 문자열 입력.
#     separated = ''.join(char if char.isdigit() else ' ' for char in my_string)  # isdigit은 숫자 문자 검사. 조건 표현식으로 문자만 공백으로 바꿔 숫자 구간을 분리.
#     return sum(map(int, separated.split()))  # split은 공백 기준 숫자 묶음 분리, map(int, ...)는 각 묶음을 정수 변환, sum은 합계.

# 풀이 요약
# 연속된 숫자는 유지하고 글자만 공백으로 바꿔 여러 자리 자연수 단위로 더합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
