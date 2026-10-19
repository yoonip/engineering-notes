# 배열 원소의 길이

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120854) · Level 0 · Python3

## 풀이

각 문자열의 길이를 입력 순서대로 반환합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(strlist):
    return [len(text) for text in strlist]

# 전체 코드 줄별 설명
# def solution(strlist):  # def는 함수 정의. 문자열 리스트 입력.
#     return [len(text) for text in strlist]  # 리스트 내포로 문자열을 순회하며 len으로 각 문자열 길이 계산.

# 풀이 요약
# 각 문자열의 길이를 입력 순서대로 반환합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
