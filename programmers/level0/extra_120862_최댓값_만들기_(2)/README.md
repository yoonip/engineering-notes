# 최댓값 만들기 (2)

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120862) · Level 0 · Python3

## 풀이

큰 양수 두 개 또는 절댓값이 큰 음수 두 개의 곱이 최대 후보입니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(numbers):
    values = sorted(numbers)
    return max(values[0] * values[1], values[-1] * values[-2])

# 전체 코드 줄별 설명
# def solution(numbers):  # def는 함수 정의. 음수도 가능한 정수 리스트 입력.
#     values = sorted(numbers)  # sorted는 오름차순 정렬한 새 리스트 반환.
#     return max(values[0] * values[1], values[-1] * values[-2])  # 0·1은 가장 작은 두 수, -1·-2는 가장 큰 두 수. max로 두 곱 중 큰 값 선택.

# 풀이 요약
# 큰 양수 두 개 또는 절댓값이 큰 음수 두 개의 곱이 최대 후보입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
