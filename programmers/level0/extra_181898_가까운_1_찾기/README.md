# 가까운 1 찾기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181898) · Level 0 · Python3

## 풀이

시작 인덱스부터 오른쪽으로 탐색해 처음 만나는 1의 위치를 반환합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(arr, idx):
    for i in range(idx, len(arr)):
        if arr[i] == 1:
            return i
    return -1

# 전체 코드 줄별 설명
# def solution(arr, idx):  # def는 함수 정의. 0·1 리스트와 탐색 시작 위치 입력.
#     for i in range(idx, len(arr)):  # len은 길이, range는 idx부터 마지막 인덱스까지 순회.
#         if arr[i] == 1:  # if는 조건, []는 인덱스 접근, ==는 값 같음 비교.
#             return i  # 처음 찾은 1의 위치를 반환하며 함수 종료.
#     return -1  # 조건에 맞는 위치가 없으면 -1 반환.

# 풀이 요약
# 시작 인덱스부터 오른쪽으로 탐색해 처음 만나는 1의 위치를 반환합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
