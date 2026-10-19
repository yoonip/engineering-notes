# 주사위 게임 2

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181930) · Level 0 · Python3

## 풀이

중복 눈의 개수에 따라 1차 합, 제곱 합, 세제곱 합을 차례로 곱합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(a, b, c):
    distinct = len({a, b, c})
    score = a + b + c
    if distinct <= 2:
        score *= a ** 2 + b ** 2 + c ** 2
    if distinct == 1:
        score *= a ** 3 + b ** 3 + c ** 3
    return score

# 전체 코드 줄별 설명
# def solution(a, b, c):  # def는 함수 정의. 세 주사위 눈 입력.
#     distinct = len({a, b, c})  # {}는 집합, 중복 원소 제거. len은 서로 다른 눈 개수.
#     score = a + b + c  # 1차 항의 합으로 점수 시작.
#     if distinct <= 2:  # if는 조건, <=는 이하 비교. 같은 눈이 하나 이상 존재하는지 검사.
#         score *= a ** 2 + b ** 2 + c ** 2  # **는 제곱, *=는 곱해 저장. 제곱 합을 점수에 곱함.
#     if distinct == 1:  # ==는 같음 비교. 세 눈이 모두 같을 때 실행.
#         score *= a ** 3 + b ** 3 + c ** 3  # 세제곱 합을 추가로 곱함.
#     return score  # 최종 점수 반환.

# 풀이 요약
# 중복 눈의 개수에 따라 1차 합, 제곱 합, 세제곱 합을 차례로 곱합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
