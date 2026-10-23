# 가까운 수

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120890) · Level 0 · Python3

## 풀이

거리 차이를 먼저 비교하고 거리가 같으면 더 작은 원소를 고릅니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(array, n):
    return min(array, key=lambda x: (abs(x - n), x))

# 전체 코드 줄별 설명
# def solution(array, n):  # def는 함수 정의. 후보 정수 리스트와 기준 정수 입력.
#     return min(array, key=lambda x: (abs(x - n), x))  # min은 기준이 가장 작은 원소 선택, lambda는 익명 함수, abs는 절댓값. 튜플로 거리 우선·값 작은 순 기준 지정.

# 풀이 요약
# 거리 차이를 먼저 비교하고 거리가 같으면 더 작은 원소를 고릅니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
