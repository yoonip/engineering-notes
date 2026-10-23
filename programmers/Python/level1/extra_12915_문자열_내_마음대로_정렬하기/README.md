# 문자열 내 마음대로 정렬하기

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12915) · Level 1 · Python3

## 풀이

정렬 키를 (지정 문자,전체 문자열)로 만들면 동률일 때의 사전순 조건도 반영됩니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(strings, n):
    return sorted(strings, key=lambda word: (word[n], word))

# 전체 코드 줄별 설명
# def solution(strings, n):  # def는 함수 정의. 문자열 리스트와 정렬할 글자 인덱스 입력.
#     return sorted(strings, key=lambda word: (word[n], word))  # sorted는 정렬, lambda는 익명 기준 함수. 튜플의 첫 기준은 n번째 문자, 같으면 전체 단어 사전순.

# 풀이 요약
# 정렬 키를 (지정 문자,전체 문자열)로 만들면 동률일 때의 사전순 조건도 반영됩니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
