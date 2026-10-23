# 연속된 수의 합

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120923) · Level 0 · Python3

## 풀이

연속된 수를 시작값+x로 표현하고 0부터 num-1까지의 합을 빼 시작값을 역산합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(num, total):
    start = (total - num * (num - 1) // 2) // num
    return list(range(start, start + num))

# 전체 코드 줄별 설명
# def solution(num, total):  # def는 함수 정의. 연속된 정수 개수와 합계 입력.
#     start = (total - num * (num - 1) // 2) // num  # //는 정수 나눗셈. 합계=시작값*num+0부터 num-1까지의 합을 이용해 시작값 계산.
#     return list(range(start, start + num))  # range는 끝 제외 연속 정수 생성, list는 리스트 변환. num개 정수 반환.

# 풀이 요약
# 연속된 수를 시작값+x로 표현하고 0부터 num-1까지의 합을 빼 시작값을 역산합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
