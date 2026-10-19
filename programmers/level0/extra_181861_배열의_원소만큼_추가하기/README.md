# 배열의 원소만큼 추가하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181861) · Level 0 · Python3

## 풀이

각 수 a를 a번 반복한 묶음을 입력 순서대로 연결합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(arr):
    answer = []
    for value in arr:
        answer.extend([value] * value)
    return answer

# 전체 코드 줄별 설명
# def solution(arr):  # def는 함수 정의. 양의 정수 리스트 입력.
#     answer = []  # []는 빈 리스트. 반복한 원소를 모음.
#     for value in arr:  # for로 각 원소를 순서대로 순회.
#         answer.extend([value] * value)  # [value]*value는 같은 값을 value개 가진 리스트. extend는 그 원소들을 끝에 추가.
#     return answer  # 완성된 리스트 반환.

# 풀이 요약
# 각 수 a를 a번 반복한 묶음을 입력 순서대로 연결합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
