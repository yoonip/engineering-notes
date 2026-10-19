# 약수 구하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120897) · Level 0 · Python3

## 풀이

1부터 n까지 검사해 나누어떨어지는 약수를 오름차순으로 모읍니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(n):
    return [value for value in range(1, n + 1) if n % value == 0]

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 약수를 구할 정수 입력.
#     return [value for value in range(1, n + 1) if n % value == 0]  # range는 1부터 n까지 순회. %는 나머지, 리스트 내포의 if로 n을 나누어떨어지게 하는 수만 선택.

# 풀이 요약
# 1부터 n까지 검사해 나누어떨어지는 약수를 오름차순으로 모읍니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
