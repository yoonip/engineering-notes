# 배열 비교하기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181856) · Level 0 · Python3

## 풀이

길이를 먼저, 같을 때 합계를 비교하므로 (길이,합계) 튜플로 비교할 수 있습니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(arr1, arr2):
    a = (len(arr1), sum(arr1))
    b = (len(arr2), sum(arr2))
    return int(a > b) - int(a < b)

# 전체 코드 줄별 설명
# def solution(arr1, arr2):  # def는 함수 정의. 비교할 두 정수 리스트 입력.
#     a = (len(arr1), sum(arr1))  # ()는 튜플. len은 길이, sum은 합계. 비교 우선순위대로 두 기준 저장.
#     b = (len(arr2), sum(arr2))  # 두 번째 리스트의 비교 기준도 같은 순서로 저장.
#     return int(a > b) - int(a < b)  # 튜플은 앞 항목부터 비교. int는 참·거짓을 1·0으로 변환. 크면 1, 작으면 -1, 같으면 0.

# 풀이 요약
# 길이를 먼저, 같을 때 합계를 비교하므로 (길이,합계) 튜플로 비교할 수 있습니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
