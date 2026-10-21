# 문자열 다루기 기본

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12918) · Level 1 · Python3

## 풀이

문자열 길이가 4 또는 6이라는 조건과 숫자로만 구성된 조건을 모두 검사합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(s):
    return len(s) in (4, 6) and s.isdigit()

# 전체 코드 줄별 설명
# def solution(s):  # def는 함수 정의. 검사할 문자열 입력.
#     return len(s) in (4, 6) and s.isdigit()  # len은 길이, in은 튜플 포함 검사, and는 모두 참, isdigit은 모든 문자가 숫자인지 검사.

# 풀이 요약
# 문자열 길이가 4 또는 6이라는 조건과 숫자로만 구성된 조건을 모두 검사합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
