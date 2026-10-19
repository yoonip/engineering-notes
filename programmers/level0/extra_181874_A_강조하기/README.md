# A 강조하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181874) · Level 0 · Python3

## 풀이

모두 소문자로 바꾼 다음 a만 다시 대문자로 바꾸면 A만 강조됩니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(myString):
    return myString.lower().replace('a', 'A')

# 전체 코드 줄별 설명
# def solution(myString):  # def는 함수 정의. 문자열 입력.
#     return myString.lower().replace('a', 'A')  # lower로 전체 소문자 변환 후 replace(이전,새값)로 a만 대문자 A로 바꿈.

# 풀이 요약
# 모두 소문자로 바꾼 다음 a만 다시 대문자로 바꾸면 A만 강조됩니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
