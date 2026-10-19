# 분수의 덧셈

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120808) · Level 0 · Python3

## 풀이

통분하여 더한 뒤 최대공약수로 분자와 분모를 나누어 약분합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
from math import gcd

def solution(numer1, denom1, numer2, denom2):
    numerator = numer1 * denom2 + numer2 * denom1
    denominator = denom1 * denom2
    common = gcd(numerator, denominator)
    return [numerator // common, denominator // common]

# 전체 코드 줄별 설명
# from math import gcd  # from 모듈 import 이름은 도구 가져오기. gcd는 두 정수의 최대공약수를 구하는 수학 함수.
# 
# def solution(numer1, denom1, numer2, denom2):  # def는 함수 정의. 두 분수의 분자·분모 입력.
#     numerator = numer1 * denom2 + numer2 * denom1  # *는 곱셈. 두 분수를 통분한 분자 합 계산.
#     denominator = denom1 * denom2  # 두 분모의 곱으로 공통 분모 계산.
#     common = gcd(numerator, denominator)  # 분자와 분모의 최대공약수 계산.
#     return [numerator // common, denominator // common]  # //는 정수 나눗셈. 분자·분모를 같은 공약수로 나누어 기약분수 리스트 반환.

# 풀이 요약
# 통분하여 더한 뒤 최대공약수로 분자와 분모를 나누어 약분합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
