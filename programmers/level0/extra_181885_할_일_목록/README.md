# 할 일 목록

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181885) · Level 0 · Python3

## 풀이

할 일과 완료 여부를 짝지은 뒤 완료되지 않은 일만 원래 순서대로 남깁니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(todo_list, finished):
    return [task for task, done in zip(todo_list, finished) if not done]

# 전체 코드 줄별 설명
# def solution(todo_list, finished):  # def는 함수 정의. 할 일과 완료 여부 리스트 입력.
#     return [task for task, done in zip(todo_list, finished) if not done]  # zip은 같은 위치 원소를 묶음. 리스트 내포에서 not으로 미완료인 일만 선택.

# 풀이 요약
# 할 일과 완료 여부를 짝지은 뒤 완료되지 않은 일만 원래 순서대로 남깁니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
