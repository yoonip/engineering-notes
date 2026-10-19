# 합성수 찾기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120846) · Level 0 · Python3

## 풀이

2부터 n까지의 각 수에서 1과 자기 자신 외의 약수가 존재하는지 검사합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(n):
    return sum(any(value % divisor == 0 for divisor in range(2, value)) for value in range(2, n + 1))

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 합성수를 셀 상한 입력.
#     return sum(any(value % divisor == 0 for divisor in range(2, value)) for value in range(2, n + 1))  # range는 정수 순회, %는 나머지. 1과 자기 자신 외의 약수가 하나라도 있으면 any가 참. sum으로 합성수 개수 집계.

# 풀이 요약
# 2부터 n까지의 각 수에서 1과 자기 자신 외의 약수가 존재하는지 검사합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
