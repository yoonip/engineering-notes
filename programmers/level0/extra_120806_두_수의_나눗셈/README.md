# 두 수의 나눗셈

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120806) · Level 0 · Python3

## 풀이

실수 계산 없이 num1*1000을 num2로 정수 나누기 합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(num1, num2):
    return num1 * 1000 // num2

# 전체 코드 줄별 설명
# def solution(num1, num2):  # def는 함수 정의. 나눌 두 양의 정수 입력.
#     return num1 * 1000 // num2  # *는 곱셈, //는 정수 나눗셈. 먼저 1000을 곱해 나눈 값의 정수 부분을 정확히 계산.

# 풀이 요약
# 실수 계산 없이 num1*1000을 num2로 정수 나누기 합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
