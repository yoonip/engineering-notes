# 배열의 유사도

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120903) · Level 0 · Python3

## 풀이

두 집합에 모두 포함된 원소의 개수를 구합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(s1, s2):
    return len(set(s1) & set(s2))

# 전체 코드 줄별 설명
# def solution(s1, s2):  # def는 함수 정의. 중복 없는 두 문자열 리스트 입력.
#     return len(set(s1) & set(s2))  # set은 중복 없는 집합, &는 교집합, len은 원소 개수. 공통 원소 수 반환.

# 풀이 요약
# 두 집합에 모두 포함된 원소의 개수를 구합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
