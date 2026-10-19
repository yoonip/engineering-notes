# 부분 문자열인지 확인하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181843) · Level 0 · Python3

## 풀이

target이 my_string 안에 연속해서 나타나는지 검사합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(my_string, target):
    return int(target in my_string)

# 전체 코드 줄별 설명
# def solution(my_string, target):  # def는 함수 정의. 원본과 부분 문자열 후보 입력.
#     return int(target in my_string)  # in은 연속 부분 문자열 포함 검사, int는 참을 1·거짓을 0으로 변환.

# 풀이 요약
# target이 my_string 안에 연속해서 나타나는지 검사합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
