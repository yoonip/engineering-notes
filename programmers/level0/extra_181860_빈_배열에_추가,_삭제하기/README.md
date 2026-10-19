# 빈 배열에 추가, 삭제하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181860) · Level 0 · Python3

## 풀이

flag가 참이면 지정 개수를 추가하고 거짓이면 끝에서 지정 개수를 삭제합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(arr, flag):
    answer = []
    for value, keep in zip(arr, flag):
        if keep:
            answer.extend([value] * (value * 2))
        else:
            del answer[-value:]
    return answer

# 전체 코드 줄별 설명
# def solution(arr, flag):  # def는 함수 정의. 값 리스트와 추가·삭제 여부 입력.
#     answer = []  # []는 빈 리스트. 작업할 배열 초기화.
#     for value, keep in zip(arr, flag):  # zip은 같은 위치의 값과 참·거짓을 묶어 순회.
#         if keep:  # if는 조건. 참이면 추가 작업.
#             answer.extend([value] * (value * 2))  # 리스트 * 횟수는 반복, extend는 원소들을 끝에 추가. value를 2*value개 삽입.
#         else:  # 거짓이면 삭제 작업.
#             del answer[-value:]  # del은 삭제, [-value:]는 마지막 value개 구간. 해당 원소들 제거.
#     return answer  # 추가·삭제를 순서대로 적용한 리스트 반환.

# 풀이 요약
# flag가 참이면 지정 개수를 추가하고 거짓이면 끝에서 지정 개수를 삭제합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
