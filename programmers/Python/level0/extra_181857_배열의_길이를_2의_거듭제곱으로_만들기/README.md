# 배열의 길이를 2의 거듭제곱으로 만들기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181857) · Level 0 · Python3

## 풀이

현재 길이 이상인 가장 작은 2의 거듭제곱을 찾고 그 차이만큼 0을 추가합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(arr):
    size = 1
    while size < len(arr):
        size *= 2
    return arr + [0] * (size - len(arr))

# 전체 코드 줄별 설명
# def solution(arr):  # def는 함수 정의. 정수 리스트 입력.
#     size = 1  # 2의 0제곱부터 목표 길이 시작.
#     while size < len(arr):  # while은 조건 반복, len은 길이. 현재 길이 이상인 거듭제곱을 찾음.
#         size *= 2  # *=는 곱해 저장. 1,2,4,8 순서로 목표 길이 증가.
#     return arr + [0] * (size - len(arr))  # 부족한 길이만큼 0 리스트를 만들어 +로 뒤에 연결.

# 풀이 요약
# 현재 길이 이상인 가장 작은 2의 거듭제곱을 찾고 그 차이만큼 0을 추가합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
