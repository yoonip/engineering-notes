# 문자열 내림차순으로 배치하기

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12917) · Level 1 · Python3

## 풀이

파이썬 문자 정렬 순서가 문제의 대소문자 크기 정의와 같으므로 내림차순 정렬합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(s):
    return ''.join(sorted(s, reverse=True))

# 전체 코드 줄별 설명
# def solution(s):  # def는 함수 정의. 영문 대소문자 문자열 입력.
#     return ''.join(sorted(s, reverse=True))  # sorted는 문자 정렬, reverse=True는 내림차순, join은 문자열 연결. 문자 코드상 소문자가 대문자보다 큼.

# 풀이 요약
# 파이썬 문자 정렬 순서가 문제의 대소문자 크기 정의와 같으므로 내림차순 정렬합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
