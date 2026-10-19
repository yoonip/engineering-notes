# 홀짝에 따라 다른 값 반환하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181935) · Level 0 · Python3

## 풀이

홀수이면 홀수 합, 짝수이면 짝수 제곱 합을 구합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(n):
    if n % 2:
        return sum(range(1, n + 1, 2))
    return sum(x ** 2 for x in range(2, n + 1, 2))

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 상한 정수 n 입력.
#     if n % 2:  # if는 조건, %는 나머지. 나머지 1은 참이므로 홀수일 때 실행.
#         return sum(range(1, n + 1, 2))  # range(시작,끝,간격)는 끝 제외 수열 생성. sum은 홀수들의 합.
#     return sum(x ** 2 for x in range(2, n + 1, 2))  # **는 거듭제곱. 생성기 표현식으로 짝수 제곱을 만들고 sum으로 합산.

# 풀이 요약
# 홀수이면 홀수 합, 짝수이면 짝수 제곱 합을 구합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
