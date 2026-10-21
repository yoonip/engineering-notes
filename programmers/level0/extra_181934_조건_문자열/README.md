# 조건 문자열

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181934) · Level 0 · Python3

## 풀이

같은 수일 때 등호 여부를 먼저 처리하고, 나머지는 부등호 방향만 비교합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(ineq, eq, n, m):
    if n == m:
        return int(eq == '=')
    return int(n > m if ineq == '>' else n < m)

# 전체 코드 줄별 설명
# def solution(ineq, eq, n, m):  # def는 함수 정의. 부등호·등호 포함 여부·두 정수 입력.
#     if n == m:  # if는 조건, ==는 값 같음 비교.
#         return int(eq == '=')  # 같은 수라면 등호가 포함된 비교만 참. int로 1 또는 0 반환.
#     return int(n > m if ineq == '>' else n < m)  # 조건 표현식으로 부등호 방향 선택. >·<는 대소 비교, int는 참·거짓을 정수로 변환.

# 풀이 요약
# 같은 수일 때 등호 여부를 먼저 처리하고, 나머지는 부등호 방향만 비교합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
