# n보다 커질 때까지 더하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181884) · Level 0 · Python3

## 풀이

합이 n 이상이 아닌 n 초과가 될 때 멈춥니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(numbers, n):
    total = 0
    for value in numbers:
        total += value
        if total > n:
            return total

# 전체 코드 줄별 설명
# def solution(numbers, n):  # def는 함수 정의. 양의 정수 리스트와 합계 기준 입력.
#     total = 0  # 누적 합계 초기화.
#     for value in numbers:  # for로 원소를 앞에서부터 순회.
#         total += value  # +=는 더해 저장. 현재 원소 누적.
#         if total > n:  # if는 조건, >는 초과 비교. 기준과 같을 때는 계속 더함.
#             return total  # 기준보다 커진 첫 순간의 합을 반환하고 종료.

# 풀이 요약
# 합이 n 이상이 아닌 n 초과가 될 때 멈춥니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
