# 문자열안에 문자열

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120908) · Level 0 · Python3

## 풀이

문제에서 미포함 결과를 0이 아닌 2로 요구하는 점을 주의합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(str1, str2):
    return 1 if str2 in str1 else 2

# 전체 코드 줄별 설명
# def solution(str1, str2):  # def는 함수 정의. 원본 문자열과 찾을 부분 문자열 입력.
#     return 1 if str2 in str1 else 2  # in은 연속 부분 문자열 포함 검사. 조건 표현식으로 포함되면 1, 없으면 2 반환.

# 풀이 요약
# 문제에서 미포함 결과를 0이 아닌 2로 요구하는 점을 주의합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
