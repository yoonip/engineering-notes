# 순서쌍의 개수

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120836) · Level 0 · Python3

## 풀이

약수 하나가 정해지면 다른 수는 n을 그 약수로 나눈 값입니다. 같은 두 수인 경우만 한 번 셉니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(n):
    count, divisor = 0, 1
    while divisor * divisor <= n:
        if n % divisor == 0:
            count += 1 if divisor * divisor == n else 2
        divisor += 1
    return count

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 두 자연수의 곱이 될 정수 입력.
#     count, divisor = 0, 1  # 순서쌍 개수와 약수 후보 초기화.
#     while divisor * divisor <= n:  # while은 조건 반복. 제곱근 이하의 약수만 검사.
#         if n % divisor == 0:  # %는 나머지, ==는 값 비교. 약수인지 확인.
#             count += 1 if divisor * divisor == n else 2  # 제곱근 약수는 같은 한 쌍, 나머지는 (a,b)와 (b,a)의 두 순서쌍 추가.
#         divisor += 1  # 다음 약수 후보로 이동.
#     return count  # 순서를 구분한 전체 약수 쌍 개수 반환.

# 풀이 요약
# 약수 하나가 정해지면 다른 수는 n을 그 약수로 나눈 값입니다. 같은 두 수인 경우만 한 번 셉니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
