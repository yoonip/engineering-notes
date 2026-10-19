# 소인수분해

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120852) · Level 0 · Python3

## 풀이

작은 인수부터 나누되 같은 인수는 모두 제거한 후 한 번만 기록합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(n):
    answer = []
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            answer.append(divisor)
            while n % divisor == 0:
                n //= divisor
        divisor += 1
    if n > 1:
        answer.append(n)
    return answer

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 소인수분해할 자연수 입력.
#     answer = []  # []는 빈 리스트. 서로 다른 소인수 저장.
#     divisor = 2  # 가장 작은 소수인 2부터 나누어 봄.
#     while divisor * divisor <= n:  # while은 조건 반복. 남은 수의 제곱근 이하까지만 후보 검사.
#         if n % divisor == 0:  # %는 나머지, ==는 같음 비교. 현재 후보가 인수인지 검사.
#             answer.append(divisor)  # append는 소인수 한 번만 추가.
#             while n % divisor == 0:  # 같은 소인수가 여러 번 있으면 모두 제거.
#                 n //= divisor  # //=는 정수 나눗셈 후 저장. 인수 한 개 제거.
#         divisor += 1  # +=는 더해 저장. 다음 후보 검사.
#     if n > 1:  # 모든 작은 인수를 제거하고 남은 수가 있는지 확인.
#         answer.append(n)  # 남은 수는 소수이므로 마지막 소인수로 추가.
#     return answer  # 중복 없이 오름차순으로 모은 소인수 리스트 반환.

# 풀이 요약
# 작은 인수부터 나누되 같은 인수는 모두 제거한 후 한 번만 기록합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
