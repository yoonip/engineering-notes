# 문자열의 앞의 n글자

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181907) · Level 0 · Python3

## 풀이

슬라이싱의 끝 인덱스는 포함되지 않으므로 n을 그대로 사용합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(my_string, n):
    return my_string[:n]

# 전체 코드 줄별 설명
# def solution(my_string, n):  # def는 함수 정의. 문자열과 가져올 글자 수 입력.
#     return my_string[:n]  # [:n]은 처음부터 인덱스 n 직전까지 잘라 앞 n글자 반환.

# 풀이 요약
# 슬라이싱의 끝 인덱스는 포함되지 않으므로 n을 그대로 사용합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
