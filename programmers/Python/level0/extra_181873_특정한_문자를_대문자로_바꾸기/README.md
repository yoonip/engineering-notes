# 특정한 문자를 대문자로 바꾸기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181873) · Level 0 · Python3

## 풀이

지정된 문자만 대문자로 치환합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(my_string, alp):
    return my_string.replace(alp, alp.upper())

# 전체 코드 줄별 설명
# def solution(my_string, alp):  # def는 함수 정의. 원본 문자열과 대문자로 바꿀 문자 입력.
#     return my_string.replace(alp, alp.upper())  # upper는 대문자 변환, replace는 해당 문자를 모두 새 값으로 치환.

# 풀이 요약
# 지정된 문자만 대문자로 치환합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
