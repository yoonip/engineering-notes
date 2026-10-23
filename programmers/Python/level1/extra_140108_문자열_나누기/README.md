# 문자열 나누기

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/140108) · Level 1 · Python3

유형: 문자열 · 개수 비교

## 풀이 원리

현재 조각의 첫 문자와 같은 글자 수, 다른 글자 수를 셉니다. 두 수가 같아지는 즉시 조각 하나를 확정하고 두 개수를 초기화합니다. 끝까지 남은 조각은 개수가 달라도 한 조각으로 셉니다.

문자 수 N: 시간 O(N), 보조 공간 O(1).

## 공식 예제

입력 인수: `["banana"]`

반환값: `3`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(s):
    answer = 0
    same = 0
    diff = 0
    first = ""
    for ch in s:
        if same == 0 and diff == 0:
            first = ch
        if ch == first:
            same += 1
        else:
            diff += 1
        if same == diff:
            answer += 1
            same = 0
            diff = 0
    if same > 0 or diff > 0:
        answer += 1
    return answer

# 전체 코드 줄별 설명
# def solution(s):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 문자열 s를 입력받는 함수
#     answer = 0  # =는 값 저장. 나눈 문자열의 개수를 저장
#     same = 0  # =는 값 저장. 다음 구간을 위해 같은 문자 개수 초기화
#     diff = 0  # =는 값 저장. 다음 구간을 위해 다른 문자 개수 초기화
#     first = ""  # =는 값 저장. 현재 구간의 첫 문자를 저장
#     for ch in s:  # for·in은 원소를 차례로 꺼내는 반복문. 문자열 s에서 문자를 하나씩 꺼내 반복
#         if same == 0 and diff == 0:  # if는 조건이 참일 때 실행. and는 두 조건 모두 참. ==는 같음 비교. 새로운 구간이 시작되었다면
#             first = ch  # =는 값 저장. 현재 문자를 새로운 구간의 기준 문자로 지정
#         if ch == first:  # if는 조건이 참일 때 실행. ==는 같음 비교. 현재 문자가 기준 문자와 같으면
#             same += 1  # +=는 더하거나 연결한 값을 저장. 같은 문자 개수를 1 증가
#         else:  # else는 앞 조건들에 해당하지 않는 경우. 기준 문자와 다르면
#             diff += 1  # +=는 더하거나 연결한 값을 저장. 다른 문자 개수를 1 증가
#         if same == diff:  # if는 조건이 참일 때 실행. ==는 같음 비교. 같은 문자와 다른 문자 개수가 같아지면
#             answer += 1  # +=는 더하거나 연결한 값을 저장. 남은 문자열도 하나의 구간으로 계산
#             same = 0  # =는 값 저장. 다음 구간을 위해 같은 문자 개수 초기화
#             diff = 0  # =는 값 저장. 다음 구간을 위해 다른 문자 개수 초기화
#     if same > 0 or diff > 0:  # if는 조건이 참일 때 실행. or는 한 조건 이상 참. >는 큼 비교. 반복 종료 후 아직 나누지 않은 문자열이 남았다면
#         answer += 1  # +=는 더하거나 연결한 값을 저장. 남은 문자열도 하나의 구간으로 계산
#     return answer  # return은 결과를 돌려주고 함수 종료. 나눈 문자열의 총개수 반환

# 풀이 요약
# 현재 조각의 첫 문자와 같은 글자 수, 다른 글자 수를 센다. 두 수가 같아지는 즉시 조각 하나를 확정하고 두 개수를 초기화한다. 끝까지 남은 조각은 개수가 달라도 한 조각으로 센다.
# 문자 수 N: 시간 O(N), 보조 공간 O(1).
```

## 확인한 범위

2026-10-16 00:29:29의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
