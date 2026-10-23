# 배열 조각하기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181893) · Level 0 · Python3

## 풀이

각 쿼리는 이전 작업 후 남은 리스트의 인덱스를 기준으로 적용합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(arr, query):
    for i, cut in enumerate(query):
        arr = arr[:cut + 1] if i % 2 == 0 else arr[cut:]
    return arr

# 전체 코드 줄별 설명
# def solution(arr, query):  # def는 함수 정의. 원본 리스트와 자를 위치 쿼리 입력.
#     for i, cut in enumerate(query):  # enumerate는 쿼리 순서와 자를 위치를 함께 제공.
#         arr = arr[:cut + 1] if i % 2 == 0 else arr[cut:]  # %는 나머지. 짝수 순서는 뒤를 버리고, 홀수 순서는 앞을 버림. 기준 원소는 보존.
#     return arr  # 순서대로 잘라 남은 리스트 반환.

# 풀이 요약
# 각 쿼리는 이전 작업 후 남은 리스트의 인덱스를 기준으로 적용합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
