# 나이 출력

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120820) · Level 0 · Python3

## 풀이

현재 실제 연도가 아니라 문제에서 지정한 2022년을 기준으로 계산합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(age):
    return 2022 - age + 1

# 전체 코드 줄별 설명
# def solution(age):  # def는 함수 정의. 문제의 2022년 기준 한국식 나이 입력.
#     return 2022 - age + 1  # 출생 연도=기준 연도-나이+1. 태어난 해에 1살이므로 1을 더함.

# 풀이 요약
# 현재 실제 연도가 아니라 문제에서 지정한 2022년을 기준으로 계산합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
