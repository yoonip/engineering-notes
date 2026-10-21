# 간단한 논리 연산

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181917) · Level 0 · Python3

## 풀이

논리합 기호 ∨는 or, 논리곱 기호 ∧는 and에 대응합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(x1, x2, x3, x4):
    return (x1 or x2) and (x3 or x4)

# 전체 코드 줄별 설명
# def solution(x1, x2, x3, x4):  # def는 함수 정의. 네 참·거짓 값 입력.
#     return (x1 or x2) and (x3 or x4)  # or는 하나라도 참, and는 모두 참. 괄호로 두 OR 조건을 먼저 계산.

# 풀이 요약
# 논리합 기호 ∨는 or, 논리곱 기호 ∧는 and에 대응합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
