# 문자열 뒤집기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181905) · Level 0 · Python3

## 풀이

앞뒤는 유지하고 가운데 구간만 역순으로 바꿔 연결합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(my_string, s, e):
    return my_string[:s] + my_string[s:e + 1][::-1] + my_string[e + 1:]

# 전체 코드 줄별 설명
# def solution(my_string, s, e):  # def는 함수 정의. 문자열과 뒤집을 양 끝 인덱스 입력.
#     return my_string[:s] + my_string[s:e + 1][::-1] + my_string[e + 1:]  # [:s]는 앞부분, [s:e+1]은 양 끝 포함 구간, [::-1]은 역순, +는 문자열 연결.

# 풀이 요약
# 앞뒤는 유지하고 가운데 구간만 역순으로 바꿔 연결합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
