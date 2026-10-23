# 노란불 신호등

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/468371) · Level 1 · Python3

유형: 수학 · 최소공배수 · 완전탐색

## 풀이 원리

각 신호등의 상태는 주기마다 반복됩니다. 모든 주기의 최소공배수 L초 뒤에는 전체 상태도 처음으로 돌아가므로 1~L초만 확인하면 충분합니다. (time-1)을 주기로 나눈 나머지가 초록 길이 이상, 초록+노랑 길이 미만이면 노란불입니다. 작은 시각부터 검사해 첫 성공을 반환합니다.

신호등 수 N, 전체 반복 주기 L: 시간 O(NL), 보조 공간 O(1).

## 공식 예제

입력 인수: `[[[2, 1, 2], [5, 1, 1]]]`

반환값: `13`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
from math import gcd

def solution(signals):
    limit = 1
    for green, yellow, red in signals:
        cycle = green + yellow + red
        limit = limit * cycle // gcd(limit, cycle)
    for time in range(1, limit + 1):
        all_yellow = True
        for green, yellow, red in signals:
            cycle = green + yellow + red
            position = (time - 1) % cycle
            if not (green <= position < green + yellow):
                all_yellow = False
                break
        if all_yellow:
            return time
    return -1

# 전체 코드 줄별 설명
# from math import gcd  # from math import는 math 모듈에서 이름을 가져옴. gcd는 최대공약수를 구하는 함수. 신호 주기의 최소공배수 계산에 사용할 최대공약수 함수.
# 
# def solution(signals):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 각 신호등의 초록·노랑·빨강 지속 시간을 입력받음.
#     limit = 1  # =는 값 저장. 전체 반복 주기의 누적값을 1로 시작.
#     for green, yellow, red in signals:  # for·in은 원소를 차례로 꺼내는 반복문. 신호등 하나의 세 지속 시간을 나눠 받음.
#         cycle = green + yellow + red  # =는 값 저장. 이 신호등의 한 주기 길이를 계산.
#         limit = limit * cycle // gcd(limit, cycle)  # gcd는 최대공약수. //는 내림한 정수 몫. =는 값 저장. 두 수의 곱을 최대공약수로 나눠 최소공배수 갱신.
#     for time in range(1, limit + 1):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. 상태가 다시 반복되기 전까지 시각을 작은 순서로 확인.
#         all_yellow = True  # =는 값 저장. True·False는 참·거짓. 이번 시각에는 일단 모든 등이 노랗다고 가정.
#         for green, yellow, red in signals:  # for·in은 원소를 차례로 꺼내는 반복문. 각 신호등을 하나씩 검사.
#             cycle = green + yellow + red  # =는 값 저장. 현재 신호등의 주기 길이 계산.
#             position = (time - 1) % cycle  # %는 나머지. =는 값 저장. 시작 시각이 1초이므로 1을 빼고 주기 내 위치 계산.
#             if not (green <= position < green + yellow):  # if는 조건이 참일 때 실행. not은 참·거짓 반전. <=는 이하 비교. <는 작음 비교. 노란불 구간 밖에 있는 신호등을 발견했는지 확인.
#                 all_yellow = False  # =는 값 저장. True·False는 참·거짓. 모든 등이 노랗다는 가정을 취소.
#                 break  # break는 가장 가까운 반복문 종료. 나머지 신호등 검사를 중단.
#         if all_yellow:  # if는 조건이 참일 때 실행. 모든 신호등의 노란불 조건이 유지됐는지 확인.
#             return time  # return은 결과를 돌려주고 함수 종료. 작은 시각부터 검사했으므로 최초 시각을 반환.
#     return -1  # return은 결과를 돌려주고 함수 종료. 전체 반복 주기에도 없으면 불가능을 나타내는 -1 반환.

# 풀이 요약
# 각 신호등의 상태는 주기마다 반복된다. 모든 주기의 최소공배수 L초 뒤에는 전체 상태도 처음으로 돌아가므로 1~L초만 확인하면 충분하다. (time-1)을 주기로 나눈 나머지가 초록 길이 이상, 초록+노랑 길이 미만이면 노란불이다. 작은 시각부터 검사해 첫 성공을 반환한다.
# 신호등 수 N, 전체 반복 주기 L: 시간 O(NL), 보조 공간 O(1).
```

## 확인한 범위

2026-10-15 23:36:15의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
