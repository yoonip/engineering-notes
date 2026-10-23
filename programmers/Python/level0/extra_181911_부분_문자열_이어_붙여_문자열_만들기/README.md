# 부분 문자열 이어 붙여 문자열 만들기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181911) · Level 0 · Python3

## 풀이

문자열과 해당 범위를 짝지어 부분 문자열들을 순서대로 이어 붙입니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(my_strings, parts):
    return ''.join(text[start:end + 1] for text, (start, end) in zip(my_strings, parts))

# 전체 코드 줄별 설명
# def solution(my_strings, parts):  # def는 함수 정의. 문자열 리스트와 각 부분 범위 입력.
#     return ''.join(text[start:end + 1] for text, (start, end) in zip(my_strings, parts))  # zip은 같은 위치 원소를 묶음, 튜플 분해로 범위를 받음. 슬라이싱 후 join으로 연결.

# 풀이 요약
# 문자열과 해당 범위를 짝지어 부분 문자열들을 순서대로 이어 붙입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
