# 수열과 구간 쿼리 2

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181923) · Level 0 · Python3

## 풀이

각 범위에서 k보다 큰 값만 고른 뒤 최솟값을 구합니다. 후보가 없으면 -1입니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(arr, queries):
    answer = []
    for start, end, k in queries:
        value = min((x for x in arr[start:end + 1] if x > k), default=-1)
        answer.append(value)
    return answer

# 전체 코드 줄별 설명
# def solution(arr, queries):  # def는 함수 정의. 정수 리스트와 범위·기준 쿼리 리스트 입력.
#     answer = []  # []는 빈 리스트. 쿼리별 결과 저장.
#     for start, end, k in queries:  # 각 쿼리의 세 정수를 나누어 받음.
#         value = min((x for x in arr[start:end + 1] if x > k), default=-1)  # 슬라이싱의 끝은 제외라 end+1 사용. 생성기에서 k 초과 값만 골라 min 계산, 없으면 default의 -1.
#         answer.append(value)  # append는 끝에 추가. 현재 쿼리 결과 저장.
#     return answer  # 쿼리 순서의 결과 리스트 반환.

# 풀이 요약
# 각 범위에서 k보다 큰 값만 고른 뒤 최솟값을 구합니다. 후보가 없으면 -1입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
