# 공백으로 구분하기 2

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181868) · Level 0 · Python3

## 풀이

split에 구분자를 지정하지 않으면 여러 공백과 양 끝 공백을 한 번에 처리합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(my_string):
    return my_string.split()

# 전체 코드 줄별 설명
# def solution(my_string):  # def는 함수 정의. 여러 공백을 포함할 수 있는 문자열 입력.
#     return my_string.split()  # 인자 없는 split은 연속된 공백을 하나의 구분자로 취급하고 앞뒤 공백도 무시.

# 풀이 요약
# split에 구분자를 지정하지 않으면 여러 공백과 양 끝 공백을 한 번에 처리합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
