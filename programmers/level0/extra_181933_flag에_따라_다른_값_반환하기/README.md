# flag에 따라 다른 값 반환하기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181933) · Level 0 · Python3

## 풀이

flag가 참이면 더하고 거짓이면 뺍니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(a, b, flag):
    return a + b if flag else a - b

# 전체 코드 줄별 설명
# def solution(a, b, flag):  # def는 함수 정의. 두 정수와 불리언 True·False 입력.
#     return a + b if flag else a - b  # 조건 표현식은 조건이 참이면 앞 값, 거짓이면 뒤 값 선택. return으로 반환.

# 풀이 요약
# flag가 참이면 더하고 거짓이면 뺍니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
