# 배열 만들기 3

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181895) · Level 0 · Python3

## 풀이

두 닫힌 구간을 잘라낸 뒤 주어진 순서대로 붙입니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(arr, intervals):
    (a, b), (c, d) = intervals
    return arr[a:b + 1] + arr[c:d + 1]

# 전체 코드 줄별 설명
# def solution(arr, intervals):  # def는 함수 정의. 원본 리스트와 두 구간 입력.
#     (a, b), (c, d) = intervals  # 중첩 분해 대입. 두 구간의 양 끝 인덱스를 각각 받음.
#     return arr[a:b + 1] + arr[c:d + 1]  # 슬라이싱의 끝은 제외라 1을 더함. +는 두 부분 리스트 연결.

# 풀이 요약
# 두 닫힌 구간을 잘라낸 뒤 주어진 순서대로 붙입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
