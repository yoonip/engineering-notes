# a와 b 출력하기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181951) · Level 0 · Python3

## 풀이

두 정수를 입력받아 각각 a = 값, b = 값 형식으로 출력합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
a, b = map(int, input().split())
print(f"a = {a}")
print(f"b = {b}")

# 전체 코드 줄별 설명
# a, b = map(int, input().split())  # input은 한 줄 입력, split은 공백으로 분리, map(int, ...)는 각각 정수로 변환. 두 변수에 나누어 저장.
# print(f"a = {a}")  # f 문자열은 중괄호 안 표현식의 값을 삽입. print로 이름과 값 출력.
# print(f"b = {b}")  # 두 번째 변수도 요구된 형식과 공백에 맞춰 출력.

# 풀이 요약
# 두 정수를 입력받아 각각 a = 값, b = 값 형식으로 출력합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
