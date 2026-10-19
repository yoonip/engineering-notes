# 이차원 배열 대각선 순회하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181829) · Level 0 · Python3

## 풀이

행과 열의 인덱스 합이 기준 이하인 위치만 더합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(board, k):
    return sum(value for i, row in enumerate(board) for j, value in enumerate(row) if i + j <= k)

# 전체 코드 줄별 설명
# def solution(board, k):  # def는 함수 정의. 이차원 리스트와 인덱스 합 기준 입력.
#     return sum(value for i, row in enumerate(board) for j, value in enumerate(row) if i + j <= k)  # enumerate는 위치와 값 제공. 중첩 생성기에서 행+열 인덱스가 k 이하인 칸만 골라 sum으로 합산.

# 풀이 요약
# 행과 열의 인덱스 합이 기준 이하인 위치만 더합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
