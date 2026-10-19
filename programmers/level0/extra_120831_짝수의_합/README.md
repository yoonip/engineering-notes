# 짝수의 합

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120831) · Level 0 · Python3

## 풀이

2,4,6 순서로 짝수만 만들어 더합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(n):
    return sum(range(2, n + 1, 2))

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 더할 짝수의 상한 입력.
#     return sum(range(2, n + 1, 2))  # range는 2부터 n까지 2칸 간격 정수 생성. sum은 수열의 합계.

# 풀이 요약
# 2,4,6 순서로 짝수만 만들어 더합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
