# 문자열 섞기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181942) · Level 0 · Python3

## 풀이

같은 위치의 문자 두 개를 먼저 붙인 뒤 그 쌍들을 순서대로 연결합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(str1, str2):
    return ''.join(a + b for a, b in zip(str1, str2))

# 전체 코드 줄별 설명
# def solution(str1, str2):  # def는 함수 정의. 길이가 같은 두 문자열 입력.
#     return ''.join(a + b for a, b in zip(str1, str2))  # zip은 같은 위치 문자를 묶음, for는 생성기 표현식, +는 문자 연결, join은 모두 이어 붙임.

# 풀이 요약
# 같은 위치의 문자 두 개를 먼저 붙인 뒤 그 쌍들을 순서대로 연결합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
