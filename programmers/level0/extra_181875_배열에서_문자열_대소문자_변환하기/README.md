# 배열에서 문자열 대소문자 변환하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181875) · Level 0 · Python3

## 풀이

0부터 세는 인덱스가 짝수면 소문자, 홀수면 대문자로 변환합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(strArr):
    return [text.upper() if i % 2 else text.lower() for i, text in enumerate(strArr)]

# 전체 코드 줄별 설명
# def solution(strArr):  # def는 함수 정의. 문자열 리스트 입력.
#     return [text.upper() if i % 2 else text.lower() for i, text in enumerate(strArr)]  # enumerate는 인덱스와 값 제공. %2가 1인 홀수 인덱스는 upper, 짝수는 lower 적용하는 리스트 내포.

# 풀이 요약
# 0부터 세는 인덱스가 짝수면 소문자, 홀수면 대문자로 변환합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
