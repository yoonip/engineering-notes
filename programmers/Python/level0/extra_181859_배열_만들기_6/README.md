# 배열 만들기 6

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181859) · Level 0 · Python3

## 풀이

새 값과 마지막 값이 같으면 마지막 값을 제거하고, 다르면 추가합니다. 각 입력을 한 번씩 처리합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(arr):
    stack = []
    for value in arr:
        if stack and stack[-1] == value:
            stack.pop()
        else:
            stack.append(value)
    return stack or [-1]

# 전체 코드 줄별 설명
# def solution(arr):  # def는 함수 정의. 0과 1로 구성된 리스트 입력.
#     stack = []  # []는 빈 리스트. 마지막 값을 기준으로 처리하는 스택.
#     for value in arr:  # for로 입력 값을 순서대로 순회.
#         if stack and stack[-1] == value:  # and는 모두 참. 비어 있지 않고 끝 값이 현재 값과 같은지 확인.
#             stack.pop()  # pop은 마지막 원소 제거. 같은 두 값을 상쇄.
#         else:  # 스택이 비었거나 마지막 값이 다른 경우.
#             stack.append(value)  # append는 현재 값을 끝에 추가.
#     return stack or [-1]  # or는 스택이 비어 있으면 [-1] 선택. return으로 결과 반환.

# 풀이 요약
# 새 값과 마지막 값이 같으면 마지막 값을 제거하고, 다르면 추가합니다. 각 입력을 한 번씩 처리합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
