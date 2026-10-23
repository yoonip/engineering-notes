# 배열 뒤집기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120821) · Level 0 · Python3

## 풀이

문자열과 마찬가지로 리스트도 역순 슬라이싱할 수 있습니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(num_list):
    return num_list[::-1]

# 전체 코드 줄별 설명
# def solution(num_list):  # def는 함수 정의. 뒤집을 정수 리스트 입력.
#     return num_list[::-1]  # [::-1]은 마지막 원소부터 첫 원소까지 역순으로 복사한 리스트.

# 풀이 요약
# 문자열과 마찬가지로 리스트도 역순 슬라이싱할 수 있습니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
