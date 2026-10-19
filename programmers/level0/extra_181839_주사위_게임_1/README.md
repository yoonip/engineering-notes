# 주사위 게임 1

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181839) · Level 0 · Python3

## 풀이

둘 다 홀수·하나만 홀수·둘 다 짝수를 순서대로 처리합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(a, b):
    if a % 2 and b % 2:
        return a ** 2 + b ** 2
    if a % 2 or b % 2:
        return 2 * (a + b)
    return abs(a - b)

# 전체 코드 줄별 설명
# def solution(a, b):  # def는 함수 정의. 두 주사위 눈 입력.
#     if a % 2 and b % 2:  # %는 나머지, and는 모두 참. 두 수가 모두 홀수인지 확인.
#         return a ** 2 + b ** 2  # **는 거듭제곱. 두 눈의 제곱 합 반환.
#     if a % 2 or b % 2:  # or는 하나라도 참. 앞 경우를 제외했으므로 하나만 홀수인지 검사.
#         return 2 * (a + b)  # *는 곱셈. 두 눈 합의 두 배 반환.
#     return abs(a - b)  # abs는 절댓값. 둘 다 짝수이면 차이의 절댓값 반환.

# 풀이 요약
# 둘 다 홀수·하나만 홀수·둘 다 짝수를 순서대로 처리합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
