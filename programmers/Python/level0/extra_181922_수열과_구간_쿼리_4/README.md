# 수열과 구간 쿼리 4

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181922) · Level 0 · Python3

## 풀이

값이 아닌 인덱스가 k의 배수인지 검사하고 범위 안의 해당 원소를 증가시킵니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(arr, queries):
    for start, end, k in queries:
        for i in range(start, end + 1):
            if (k != 0 and i % k == 0) or (k == 0 and i == 0):
                arr[i] += 1
    return arr

# 전체 코드 줄별 설명
# def solution(arr, queries):  # def는 함수 정의. 정수 리스트와 범위·배수 쿼리 입력.
#     for start, end, k in queries:  # for로 쿼리를 순서대로 순회하고 세 값을 나누어 받음.
#         for i in range(start, end + 1):  # range는 끝 제외 정수 수열. 양 끝을 포함한 인덱스 순회.
#             if (k != 0 and i % k == 0) or (k == 0 and i == 0):  # and·or는 논리 조건, %는 나머지. 인덱스가 k의 배수인 경우 검사. 0의 배수는 0만 처리.
#                 arr[i] += 1  # []로 인덱스 접근, +=는 더해 저장. 해당 위치 값 1 증가.
#     return arr  # 수정된 리스트 반환.

# 풀이 요약
# 값이 아닌 인덱스가 k의 배수인지 검사하고 범위 안의 해당 원소를 증가시킵니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
