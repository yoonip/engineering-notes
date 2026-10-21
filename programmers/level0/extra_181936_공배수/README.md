# 공배수

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181936) · Level 0 · Python3

## 풀이

두 수 모두로 나누어떨어지는지 검사합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(number, n, m):
    return int(number % n == 0 and number % m == 0)

# 전체 코드 줄별 설명
# def solution(number, n, m):  # def는 함수 정의. 검사할 정수와 두 배수 기준 입력.
#     return int(number % n == 0 and number % m == 0)  # %는 나머지, and는 모두 참일 때 참, int는 참·거짓을 1·0으로 변환.

# 풀이 요약
# 두 수 모두로 나누어떨어지는지 검사합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
