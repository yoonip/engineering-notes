# 편지

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120898) · Level 0 · Python3

## 풀이

공백도 한 글자로 세어 전체 문자열 길이에 2를 곱합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(message):
    return len(message) * 2

# 전체 코드 줄별 설명
# def solution(message):  # def는 함수 정의. 편지 문자열 입력.
#     return len(message) * 2  # len은 공백을 포함한 문자 개수. 글자당 2cm이므로 두 배 반환.

# 풀이 요약
# 공백도 한 글자로 세어 전체 문자열 길이에 2를 곱합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
