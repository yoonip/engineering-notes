# 유한소수 판별하기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120878) · Level 0 · Python3

## 풀이

약분한 분모에서 2와 5를 모두 제거했을 때 1이 남으면 유한소수입니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
from math import gcd

def solution(a, b):
    denominator = b // gcd(a, b)
    for prime in (2, 5):
        while denominator % prime == 0:
            denominator //= prime
    return 1 if denominator == 1 else 2

# 전체 코드 줄별 설명
# from math import gcd  # from 모듈 import 이름은 도구 가져오기. math는 수학 모듈, gcd는 두 정수의 최대공약수 계산 함수.
# 
# def solution(a, b):  # def는 함수 정의. 분자와 분모 입력.
#     denominator = b // gcd(a, b)  # //는 정수 나눗셈. 분자·분모를 최대공약수로 약분한 뒤 분모만 남김.
#     for prime in (2, 5):  # ()는 튜플. 유한소수에 허용되는 두 소인수 순회.
#         while denominator % prime == 0:  # while은 조건 반복, %는 나머지. 해당 인수로 나누어떨어지는 동안 반복.
#             denominator //= prime  # //=는 정수 나눗셈 후 저장. 해당 소인수 하나 제거.
#     return 1 if denominator == 1 else 2  # 조건 표현식. 다른 소인수가 남지 않으면 유한소수 1, 아니면 2 반환.

# 풀이 요약
# 약분한 분모에서 2와 5를 모두 제거했을 때 1이 남으면 유한소수입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
