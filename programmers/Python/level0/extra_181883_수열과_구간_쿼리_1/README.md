# 수열과 구간 쿼리 1

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181883) · Level 0 · Python3

## 풀이

각 닫힌 구간에 속한 원소를 모두 1씩 증가시킵니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(arr, queries):
    for start, end in queries:
        for i in range(start, end + 1):
            arr[i] += 1
    return arr

# 전체 코드 줄별 설명
# def solution(arr, queries):  # def는 함수 정의. 정수 리스트와 구간 쿼리 입력.
#     for start, end in queries:  # 각 쿼리의 시작과 끝 위치를 나누어 받음.
#         for i in range(start, end + 1):  # range는 끝 제외. end까지 포함하도록 1을 더해 순회.
#             arr[i] += 1  # []로 원소 접근, +=는 더해 저장. 구간의 각 원소 증가.
#     return arr  # 모든 쿼리를 적용한 리스트 반환.

# 풀이 요약
# 각 닫힌 구간에 속한 원소를 모두 1씩 증가시킵니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
