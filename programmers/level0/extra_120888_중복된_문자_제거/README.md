# 중복된 문자 제거

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120888) · Level 0 · Python3

## 풀이

딕셔너리의 키는 중복되지 않고 삽입 순서가 유지되므로 첫 문자만 남길 수 있습니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(my_string):
    return ''.join(dict.fromkeys(my_string))

# 전체 코드 줄별 설명
# def solution(my_string):  # def는 함수 정의. 공백과 대소문자를 포함한 문자열 입력.
#     return ''.join(dict.fromkeys(my_string))  # dict.fromkeys는 문자를 키로 만드는 딕셔너리 생성. 중복은 제거하고 첫 등장 순서 유지. join으로 연결.

# 풀이 요약
# 딕셔너리의 키는 중복되지 않고 삽입 순서가 유지되므로 첫 문자만 남길 수 있습니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
