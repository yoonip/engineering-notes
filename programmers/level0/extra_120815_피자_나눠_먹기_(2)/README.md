# 피자 나눠 먹기 (2)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120815) · Level 0 · Python3

## 풀이

총 조각 수가 사람 수와 6 모두의 배수여야 하므로 최소공배수를 이용합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
from math import gcd

def solution(n):
    return n // gcd(n, 6)

# 전체 코드 줄별 설명
# from math import gcd  # from 모듈 import 이름은 도구 가져오기. math는 수학 모듈, gcd는 최대공약수 계산 함수.
# 
# def solution(n):  # def는 함수 정의. 똑같이 나누어 먹을 사람 수 입력.
#     return n // gcd(n, 6)  # n과 6의 최소공배수는 n*6/gcd. 이를 판당 6조각으로 나누면 n/gcd 판이 필요.

# 풀이 요약
# 총 조각 수가 사람 수와 6 모두의 배수여야 하므로 최소공배수를 이용합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
