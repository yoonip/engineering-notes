# [PCCE 기출문제] 6번 / 물 부족

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/340202) · Level 0 · Python3

## 풀이

월 사용량은 누적량이 아닌 직전 달 사용량을 기준으로 바꿉니다. 사용량 계산 한 줄만 수정하는 문제입니다.

## 코드와 줄별 설명

빈칸 채우기·한 줄 수정 형식이라 사이트에는 지정된 부분만 제출했습니다. 아래 전체 주석본은 학습용으로 보관합니다.

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(storage, usage, change):
    total_usage = 0
    for i in range(len(change)):
        usage = usage * (100 + change[i]) // 100
        total_usage += usage
        if total_usage > storage:
            return i
    return -1

# 전체 코드 줄별 설명
# def solution(storage, usage, change):  # def는 함수 정의. storage는 저장량, usage는 지난달 사용량, change는 월별 증감률 리스트.
#     total_usage = 0  # 누적 사용량을 0으로 초기화.
#     for i in range(len(change)):  # len은 길이, range는 0부터 길이-1까지 생성하여 월 번호 순회.
#         usage = usage * (100 + change[i]) // 100  # []는 인덱스 접근, *는 곱셈, //는 정수 나눗셈. 전월 사용량에 증감률을 적용하고 소수점 버림.
#         total_usage += usage  # +=는 기존 값에 더해 저장. 이번 달 사용량 누적.
#         if total_usage > storage:  # if는 조건문, >는 큼 비교. 저장량을 초과했는지 검사.
#             return i  # return은 함수 종료와 결과 반환. 0부터 세는 부족 발생 월 반환.
#     return -1  # 모든 달에 물이 충분하면 -1 반환.

# 풀이 요약
# 월 사용량은 누적량이 아닌 직전 달 사용량을 기준으로 바꿉니다. 사용량 계산 한 줄만 수정하는 문제입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
