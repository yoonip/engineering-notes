# 숫자 찾기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120904) · Level 0 · Python3

## 풀이

정수를 문자열로 바꾸어 숫자 문자의 첫 위치를 찾습니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(num, k):
    position = str(num).find(str(k))
    return position + 1 if position != -1 else -1

# 전체 코드 줄별 설명
# def solution(num, k):  # def는 함수 정의. 검사할 정수와 찾을 한 자리 숫자 입력.
#     position = str(num).find(str(k))  # str은 문자열 변환, find는 처음 나타난 인덱스 반환. 없으면 -1.
#     return position + 1 if position != -1 else -1  # 조건 표현식, !=는 다름 비교. 찾았을 때만 0부터 세는 인덱스를 1부터 세는 순번으로 변환.

# 풀이 요약
# 정수를 문자열로 바꾸어 숫자 문자의 첫 위치를 찾습니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
