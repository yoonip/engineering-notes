# A로 B 만들기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120886) · Level 0 · Python3

## 풀이

문자 순서를 바꿔 만들 수 있으려면 각 문자의 개수가 같아야 합니다. 정렬하면 이를 비교할 수 있습니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(before, after):
    return int(sorted(before) == sorted(after))

# 전체 코드 줄별 설명
# def solution(before, after):  # def는 함수 정의. 순서를 바꾸기 전과 목표 문자열 입력.
#     return int(sorted(before) == sorted(after))  # sorted는 각 문자열의 문자를 정렬한 리스트 반환. ==로 문자와 개수 일치 비교, int로 1·0 반환.

# 풀이 요약
# 문자 순서를 바꿔 만들 수 있으려면 각 문자의 개수가 같아야 합니다. 정렬하면 이를 비교할 수 있습니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
