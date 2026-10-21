# 문자열 정수의 합

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181849) · Level 0 · Python3

## 풀이

전체를 하나의 정수로 바꾸지 않고 각 자릿수를 더합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(num_str):
    return sum(map(int, num_str))

# 전체 코드 줄별 설명
# def solution(num_str):  # def는 함수 정의. 숫자 문자열 입력.
#     return sum(map(int, num_str))  # map(int,문자열)은 각 숫자를 정수로 변환. sum은 변환된 자릿수의 합 계산.

# 풀이 요약
# 전체를 하나의 정수로 바꾸지 않고 각 자릿수를 더합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
