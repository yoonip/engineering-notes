# 배열의 원소 삭제하기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181844) · Level 0 · Python3

## 풀이

삭제 대상 집합에 없는 원소만 원래 순서대로 남깁니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(arr, delete_list):
    removed = set(delete_list)
    return [value for value in arr if value not in removed]

# 전체 코드 줄별 설명
# def solution(arr, delete_list):  # def는 함수 정의. 원본 값과 삭제할 값 리스트 입력.
#     removed = set(delete_list)  # set은 중복 없는 집합. 삭제 대상 값을 빠르게 조회할 수 있게 변환.
#     return [value for value in arr if value not in removed]  # 리스트 내포의 for는 순회, if는 필터. not in으로 삭제 대상이 아닌 값만 보존.

# 풀이 요약
# 삭제 대상 집합에 없는 원소만 원래 순서대로 남깁니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
