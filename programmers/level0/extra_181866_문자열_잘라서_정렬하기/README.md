# 문자열 잘라서 정렬하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181866) · Level 0 · Python3

## 풀이

x로 나눈 뒤 빈 조각은 버리고 남은 문자열을 정렬합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(myString):
    return sorted(part for part in myString.split('x') if part)

# 전체 코드 줄별 설명
# def solution(myString):  # def는 함수 정의. x로 나눌 문자열 입력.
#     return sorted(part for part in myString.split('x') if part)  # split은 분리, if part는 빈 문자열 제외, sorted는 사전순 정렬.

# 풀이 요약
# x로 나눈 뒤 빈 조각은 버리고 남은 문자열을 정렬합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
