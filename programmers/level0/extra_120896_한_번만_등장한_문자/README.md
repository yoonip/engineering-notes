# 한 번만 등장한 문자

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120896) · Level 0 · Python3

## 풀이

각 문자의 출현 횟수가 1인지 검사한 뒤 사전순으로 연결합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(s):
    return ''.join(sorted(char for char in set(s) if s.count(char) == 1))

# 전체 코드 줄별 설명
# def solution(s):  # def는 함수 정의. 소문자 문자열 입력.
#     return ''.join(sorted(char for char in set(s) if s.count(char) == 1))  # set은 서로 다른 문자, count는 출현 횟수, if는 한 번 나온 문자 필터, sorted는 정렬, join은 문자열 연결.

# 풀이 요약
# 각 문자의 출현 횟수가 1인지 검사한 뒤 사전순으로 연결합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
