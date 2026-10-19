# 문자열 밀기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120921) · Level 0 · Python3

## 풀이

오른쪽으로 한 칸씩 회전해 목표 문자열과 처음 같아지는 횟수를 찾습니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(A, B):
    for count in range(len(A)):
        if A == B:
            return count
        A = A[-1] + A[:-1]
    return -1

# 전체 코드 줄별 설명
# def solution(A, B):  # def는 함수 정의. 회전할 문자열과 목표 문자열 입력.
#     for count in range(len(A)):  # len은 길이, range는 0부터 길이-1까지 정수 생성. 가능한 최소 회전 횟수부터 검사.
#         if A == B:  # if는 조건, ==는 문자열 같음 비교.
#             return count  # 처음 일치한 횟수가 최소이므로 즉시 반환.
#         A = A[-1] + A[:-1]  # -1은 마지막 문자, [:-1]은 마지막 전까지의 슬라이싱. 마지막 문자를 맨 앞으로 옮김.
#     return -1  # 한 바퀴 안에 일치하지 않으면 만들 수 없으므로 -1 반환.

# 풀이 요약
# 오른쪽으로 한 칸씩 회전해 목표 문자열과 처음 같아지는 횟수를 찾습니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
