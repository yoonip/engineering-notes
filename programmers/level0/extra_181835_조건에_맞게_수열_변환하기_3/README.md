# 조건에 맞게 수열 변환하기 3

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181835) · Level 0 · Python3

## 풀이

k의 홀짝은 한 번만 검사하고 전체 원소에 같은 연산을 적용합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(arr, k):
    if k % 2:
        return [value * k for value in arr]
    return [value + k for value in arr]

# 전체 코드 줄별 설명
# def solution(arr, k):  # def는 함수 정의. 정수 리스트와 변환 기준 입력.
#     if k % 2:  # if는 조건, %는 나머지. k가 홀수인지 확인.
#         return [value * k for value in arr]  # 리스트 내포로 각 원소에 k를 곱함.
#     return [value + k for value in arr]  # k가 짝수이면 각 원소에 k를 더한 리스트 반환.

# 풀이 요약
# k의 홀짝은 한 번만 검사하고 전체 원소에 같은 연산을 적용합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
