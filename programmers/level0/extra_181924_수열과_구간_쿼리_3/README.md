# 수열과 구간 쿼리 3

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181924) · Level 0 · Python3

## 풀이

각 인덱스 쌍의 값을 주어진 순서대로 맞바꿉니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(arr, queries):
    for i, j in queries:
        arr[i], arr[j] = arr[j], arr[i]
    return arr

# 전체 코드 줄별 설명
# def solution(arr, queries):  # def는 함수 정의. 정수 리스트와 교환할 위치 쌍 리스트 입력.
#     for i, j in queries:  # for로 각 쿼리를 순회하고 두 인덱스를 나누어 받음.
#         arr[i], arr[j] = arr[j], arr[i]  # 다중 대입은 오른쪽 값을 먼저 읽어 두 위치의 원소를 안전하게 교환.
#     return arr  # 모든 교환을 마친 리스트 반환.

# 풀이 요약
# 각 인덱스 쌍의 값을 주어진 순서대로 맞바꿉니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
