# 자릿수 더하기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120906) · Level 0 · Python3

## 풀이

정수를 문자열로 바꿔 각 자릿수를 따로 더합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(n):
    return sum(int(char) for char in str(n))

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 자릿수를 더할 정수 입력.
#     return sum(int(char) for char in str(n))  # str로 정수를 문자열로 변환. 각 문자를 int로 바꾸는 생성기 표현식을 sum으로 합산.

# 풀이 요약
# 정수를 문자열로 바꿔 각 자릿수를 따로 더합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
