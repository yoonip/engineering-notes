# 중앙값 구하기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120811) · Level 0 · Python3

## 풀이

정렬 후 0부터 세는 가운데 인덱스의 값을 가져옵니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(array):
    return sorted(array)[len(array) // 2]

# 전체 코드 줄별 설명
# def solution(array):  # def는 함수 정의. 길이가 홀수인 정수 리스트 입력.
#     return sorted(array)[len(array) // 2]  # sorted는 오름차순 정렬, len은 개수, //2는 가운데 인덱스. []로 중앙 원소 조회.

# 풀이 요약
# 정렬 후 0부터 세는 가운데 인덱스의 값을 가져옵니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
