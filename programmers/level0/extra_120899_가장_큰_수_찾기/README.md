# 가장 큰 수 찾기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120899) · Level 0 · Python3

## 풀이

최댓값을 구한 다음 그 값이 있는 위치를 찾습니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(array):
    largest = max(array)
    return [largest, array.index(largest)]

# 전체 코드 줄별 설명
# def solution(array):  # def는 함수 정의. 중복 없는 정수 리스트 입력.
#     largest = max(array)  # max는 최댓값. 가장 큰 원소 저장.
#     return [largest, array.index(largest)]  # []는 리스트 생성, index는 값의 위치 조회. 최대값과 인덱스 반환.

# 풀이 요약
# 최댓값을 구한 다음 그 값이 있는 위치를 찾습니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
