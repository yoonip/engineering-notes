# 배열 만들기 4

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181918) · Level 0 · Python3

## 풀이

새 값을 넣기 전에 끝의 크거나 같은 값들을 모두 제거합니다. 각 원소는 최대 한 번 삽입·제거되어 O(N)입니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(arr):
    stack = []
    for value in arr:
        while stack and stack[-1] >= value:
            stack.pop()
        stack.append(value)
    return stack

# 전체 코드 줄별 설명
# def solution(arr):  # def는 함수 정의. 정수 리스트 입력.
#     stack = []  # []는 빈 리스트. 끝에 넣고 끝에서 꺼내는 스택으로 사용.
#     for value in arr:  # for는 입력 원소를 순서대로 순회.
#         while stack and stack[-1] >= value:  # and는 두 조건 모두 참. -1은 마지막 원소. 새 값 이상인 끝 원소가 남아 있는지 검사.
#             stack.pop()  # pop은 마지막 원소를 제거해 반환. 새 값보다 작을 때까지 제거.
#         stack.append(value)  # append는 끝에 추가. 조건에 맞게 새 값을 삽입.
#     return stack  # 최종 스택 반환.

# 풀이 요약
# 새 값을 넣기 전에 끝의 크거나 같은 값들을 모두 제거합니다. 각 원소는 최대 한 번 삽입·제거되어 O(N)입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
