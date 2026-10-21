# 조건에 맞게 수열 변환하기 1

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181882) · Level 0 · Python3

## 풀이

50 이상 짝수는 절반, 50 미만 홀수는 두 배, 나머지는 그대로 둡니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(arr):
    return [x // 2 if x >= 50 and x % 2 == 0 else x * 2 if x < 50 and x % 2 == 1 else x for x in arr]

# 전체 코드 줄별 설명
# def solution(arr):  # def는 함수 정의. 정수 리스트 입력.
#     return [x // 2 if x >= 50 and x % 2 == 0 else x * 2 if x < 50 and x % 2 == 1 else x for x in arr]  # 리스트 내포와 조건 표현식. and는 모두 참, %는 나머지, //는 정수 나눗셈. 조건별로 절반·두 배·원래 값 선택.

# 풀이 요약
# 50 이상 짝수는 절반, 50 미만 홀수는 두 배, 나머지는 그대로 둡니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
