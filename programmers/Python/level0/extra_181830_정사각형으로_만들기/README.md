# 정사각형으로 만들기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181830) · Level 0 · Python3

## 풀이

행·열 중 큰 길이를 기준으로 부족한 열과 행만 0으로 채웁니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(arr):
    size = max(len(arr), len(arr[0]))
    answer = [row + [0] * (size - len(row)) for row in arr]
    answer.extend([[0] * size for _ in range(size - len(arr))])
    return answer

# 전체 코드 줄별 설명
# def solution(arr):  # def는 함수 정의. 직사각형 이차원 리스트 입력.
#     size = max(len(arr), len(arr[0]))  # len은 길이, max는 최댓값. 행·열 중 큰 수를 정사각형 한 변으로 선택.
#     answer = [row + [0] * (size - len(row)) for row in arr]  # 리스트 내포로 각 행 끝에 부족한 개수의 0 추가. +는 리스트 연결.
#     answer.extend([[0] * size for _ in range(size - len(arr))])  # 부족한 행만큼 독립적인 0 행을 생성. extend로 여러 행 추가.
#     return answer  # 0으로 채운 정사각형 행렬 반환.

# 풀이 요약
# 행·열 중 큰 길이를 기준으로 부족한 열과 행만 0으로 채웁니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
