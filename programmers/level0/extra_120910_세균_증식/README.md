# 세균 증식

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120910) · Level 0 · Python3

## 풀이

매 시간 두 배로 증가하므로 n×2^t입니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(n, t):
    return n * 2 ** t

# 전체 코드 줄별 설명
# def solution(n, t):  # def는 함수 정의. 처음 세균 수와 경과 시간 입력.
#     return n * 2 ** t  # **는 거듭제곱, *는 곱셈. 시간마다 두 배이므로 최초 개수에 2의 t제곱을 곱함.

# 풀이 요약
# 매 시간 두 배로 증가하므로 n×2^t입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
