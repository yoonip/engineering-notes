# 첫 번째로 나오는 음수

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181896) · Level 0 · Python3

## 풀이

앞에서부터 검사하면 처음 찾은 음수가 가장 먼저 등장한 음수입니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(num_list):
    for index, value in enumerate(num_list):
        if value < 0:
            return index
    return -1

# 전체 코드 줄별 설명
# def solution(num_list):  # def는 함수 정의. 정수 리스트 입력.
#     for index, value in enumerate(num_list):  # enumerate는 원소 위치와 값을 함께 제공.
#         if value < 0:  # if는 조건, <는 미만 비교. 음수인지 검사.
#             return index  # 처음 발견한 음수의 인덱스를 반환하고 종료.
#     return -1  # 음수가 없으면 -1 반환.

# 풀이 요약
# 앞에서부터 검사하면 처음 찾은 음수가 가장 먼저 등장한 음수입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
