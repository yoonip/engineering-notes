# 삼각형의 완성조건 (1)

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120889) · Level 0 · Python3

## 풀이

전체 합에서 가장 긴 변을 뺀 값이 가장 긴 변보다 큰지 확인합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(sides):
    return 1 if sum(sides) > 2 * max(sides) else 2

# 전체 코드 줄별 설명
# def solution(sides):  # def는 함수 정의. 세 변의 길이 리스트 입력.
#     return 1 if sum(sides) > 2 * max(sides) else 2  # sum은 합계, max는 최댓값. 가장 긴 변보다 나머지 두 변의 합이 크면 1, 아니면 2 반환.

# 풀이 요약
# 전체 합에서 가장 긴 변을 뺀 값이 가장 긴 변보다 큰지 확인합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
