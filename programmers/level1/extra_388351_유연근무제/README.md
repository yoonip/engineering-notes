# 유연근무제

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/388351) · Level 1 · Python3

유형: 구현 · 시간 변환

## 풀이 원리

시각을 시×60+분으로 바꿔 희망 시각에 10분을 더한다. 요일을 나머지 연산으로 계산해 주말은 건너뛰고, 모든 평일에 제한 시각 이내로 출근한 직원만 센다. 7시 55분에 10을 바로 더하면 7시 65분이 되므로 분 단위 계산이 필요하다.

직원 수 N: 7일씩 확인하므로 시간 O(N), 보조 공간 O(1).

## 공식 예제

입력 인수: `[[700, 800, 1100], [[710, 2359, 1050, 700, 650, 631, 659], [800, 801, 805, 800, 759, 810, 809], [1105, 1001, 1002, 600, 1059, 1001, 1100]], 5]`

반환값: `3`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(schedules, timelogs, startday):
    answer = 0
    for i in range(len(schedules)):
        scheduled = schedules[i]
        limit = (scheduled // 100) * 60 + scheduled % 100 + 10
        eligible = True
        for day in range(7):
            weekday = (startday + day - 1) % 7 + 1
            if weekday >= 6:
                continue
            arrival = timelogs[i][day]
            arrival_minutes = (arrival // 100) * 60 + arrival % 100
            if arrival_minutes > limit:
                eligible = False
                break
        if eligible:
            answer += 1
    return answer

# 전체 코드 줄별 설명
# def solution(schedules, timelogs, startday):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 희망 출근 시각·일주일 기록·시작 요일을 입력받음.
#     answer = 0  # =는 값 저장. 상품 받을 직원 수 초기화.
#     for i in range(len(schedules)):  # for·in은 원소를 차례로 꺼내는 반복문. len은 길이. range는 끝값 직전까지 정수 순서 생성. 직원 번호를 차례로 확인.
#         scheduled = schedules[i]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 직원의 희망 출근 시각을 읽음.
#         limit = (scheduled // 100) * 60 + scheduled % 100 + 10  # //는 내림한 정수 몫. %는 나머지. =는 값 저장. 시·분 표기를 총 분으로 바꾼 후 10분을 더함.
#         eligible = True  # =는 값 저장. True·False는 참·거짓. 해당 직원이 조건을 만족한다고 가정.
#         for day in range(7):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. 7일의 기록을 순회.
#             weekday = (startday + day - 1) % 7 + 1  # %는 나머지. =는 값 저장. 시작 요일을 반영해 월요일 1부터 일요일 7까지 계산.
#             if weekday >= 6:  # if는 조건이 참일 때 실행. >=는 이상 비교. 토요일 또는 일요일인지 확인.
#                 continue  # continue는 다음 반복으로 이동. 주말 기록은 지각 검사에서 제외.
#             arrival = timelogs[i][day]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 직원·날짜에 해당하는 출근 시각을 읽음.
#             arrival_minutes = (arrival // 100) * 60 + arrival % 100  # //는 내림한 정수 몫. %는 나머지. =는 값 저장. 출근 시각도 분 단위로 변환.
#             if arrival_minutes > limit:  # if는 조건이 참일 때 실행. >는 큼 비교. 허용 시각보다 늦게 도착했는지 확인.
#                 eligible = False  # =는 값 저장. True·False는 참·거짓. 이 직원은 상품 대상에서 제외.
#                 break  # break는 가장 가까운 반복문 종료. 남은 날짜 검사를 중단.
#         if eligible:  # if는 조건이 참일 때 실행. 모든 평일 검사를 통과했는지 확인.
#             answer += 1  # +=는 더하거나 연결한 값을 저장. 상품 받을 직원 수 증가.
#     return answer  # return은 결과를 돌려주고 함수 종료. 최종 직원 수 반환.

# 풀이 요약
# 시각을 시×60+분으로 바꿔 희망 시각에 10분을 더한다. 요일을 나머지 연산으로 계산해 주말은 건너뛰고, 모든 평일에 제한 시각 이내로 출근한 직원만 센다. 7시 55분에 10을 바로 더하면 7시 65분이 되므로 분 단위 계산이 필요하다.
# 직원 수 N: 7일씩 확인하므로 시간 O(N), 보조 공간 O(1).
```

## 확인한 범위

2026-10-15 23:34:46의 Python3 제출 내역에서 정답 100/100을 확인했다. 원본은 그대로 보관했다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
