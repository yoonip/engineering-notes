# [PCCE 기출문제] 9번 / 지폐 접기

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/340199) · Level 1 · Python3

유형: 구현 · 시뮬레이션

## 풀이 원리

지갑과 지폐의 두 변을 각각 정렬하면 회전한 경우까지 짧은 변끼리, 긴 변끼리 비교할 수 있습니다. 들어가지 않으면 현재 지폐의 긴 변을 절반으로 접고 다시 정렬합니다. 두 변이 모두 지갑 이하가 되는 첫 순간에 멈춥니다.

접는 횟수 F: 시간 O(F), 보조 공간 O(1). 입력 리스트를 직접 정렬합니다.

## 공식 예제

입력 인수: `[[30, 15], [26, 17]]`

반환값: `1`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(wallet, bill):
    wallet.sort()
    bill.sort()
    answer = 0
    while bill[0] > wallet[0] or bill[1] > wallet[1]:
        bill[1] //= 2
        bill.sort()
        answer += 1
    return answer

# 전체 코드 줄별 설명
# def solution(wallet, bill):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 지갑과 지폐의 두 변 길이를 입력받음.
#     wallet.sort()  # sort는 원래 리스트 정렬. 지갑의 짧은 변·긴 변 순서로 정렬.
#     bill.sort()  # sort는 원래 리스트 정렬. 지폐도 짧은 변·긴 변 순서로 정렬.
#     answer = 0  # =는 값 저장. 접은 횟수 초기화.
#     while bill[0] > wallet[0] or bill[1] > wallet[1]:  # while은 조건이 참인 동안 반복. or는 한 조건 이상 참. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. >는 큼 비교. 회전해도 한 변이 지갑보다 크면 계속 접음.
#         bill[1] //= 2  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. //=는 정수 몫을 저장. 긴 변을 반으로 접고 소수 부분을 버림.
#         bill.sort()  # sort는 원래 리스트 정렬. 접은 후 다시 짧은 변·긴 변 순서로 정렬.
#         answer += 1  # +=는 더하거나 연결한 값을 저장. 접은 횟수 증가.
#     return answer  # return은 결과를 돌려주고 함수 종료. 지갑 안에 들어갈 때까지 접은 횟수 반환.

# 풀이 요약
# 지갑과 지폐의 두 변을 각각 정렬하면 회전한 경우까지 짧은 변끼리, 긴 변끼리 비교할 수 있다. 들어가지 않으면 현재 지폐의 긴 변을 절반으로 접고 다시 정렬한다. 두 변이 모두 지갑 이하가 되는 첫 순간에 멈춘다.
# 접는 횟수 F: 시간 O(F), 보조 공간 O(1). 입력 리스트를 직접 정렬한다.
```

## 확인한 범위

2026-10-15 23:42:23의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
