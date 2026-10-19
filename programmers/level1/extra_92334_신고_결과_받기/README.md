# 신고 결과 받기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/92334) · Level 1 · Python3

유형: 집합 · 해시 · 중복 제거

## 풀이 원리

같은 사람이 같은 대상을 여러 번 신고해도 한 번이므로 신고 문자열을 집합으로 만듭니다. 중복을 제거한 신고에서 대상별 횟수를 구하고, 정지 기준에 도달한 대상의 신고자에게만 메일을 하나씩 더합니다. 결과는 원래 ID 순서로 꺼냅니다.

신고 R개, 사용자 U명: 평균 시간 O(R+U), 공간 O(R+U).

## 공식 예제

입력 인수: `[["muzi", "frodo", "apeach", "neo"], ["muzi frodo", "apeach frodo", "frodo neo", "muzi neo", "apeach muzi"], 2]`

반환값: `[2, 1, 1, 0]`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(id_list, report, k):
    unique_reports = set(report)
    reported_count = {user: 0 for user in id_list}
    mail_count = {user: 0 for user in id_list}
    for record in unique_reports:
        reporter, target = record.split()
        reported_count[target] += 1
    for record in unique_reports:
        reporter, target = record.split()
        if reported_count[target] >= k:
            mail_count[reporter] += 1
    return [mail_count[user] for user in id_list]

# 전체 코드 줄별 설명
# def solution(id_list, report, k):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def로 함수를 정의합니다. 이용자 목록, 신고 기록, 정지 기준을 받습니다.
#     unique_reports = set(report)  # set은 중복 없는 집합. =는 값 저장. set은 중복을 허용하지 않는 집합입니다. 같은 신고 문자열을 하나만 남깁니다.
#     reported_count = {user: 0 for user in id_list}  # in은 포함 여부. {}는 키:값을 저장하는 딕셔너리. 내포문은 반복하면서 원소를 구성. =는 값 저장. 딕셔너리 컴프리헨션입니다. ID를 키로, 신고당한 횟수 0을 값으로 저장합니다.
#     mail_count = {user: 0 for user in id_list}  # in은 포함 여부. {}는 키:값을 저장하는 딕셔너리. 내포문은 반복하면서 원소를 구성. =는 값 저장. 각 이용자가 받을 메일 개수를 0으로 시작합니다.
#     for record in unique_reports:  # for·in은 원소를 차례로 꺼내는 반복문. 모든 신고 횟수를 계산한 뒤 기록을 다시 확인합니다.
#         reporter, target = record.split()  # split은 구분자로 문자열 분리. ()로 묶은 여러 값은 변경 불가 튜플. =는 값 저장. 예: "muzi frodo"이면 reporter="muzi", target="frodo"입니다.
#         reported_count[target] += 1  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. +=는 더하거나 연결한 값을 저장. 딕셔너리[키]의 값을 1 증가시킵니다. 신고 대상의 횟수를 늘립니다.
#     for record in unique_reports:  # for·in은 원소를 차례로 꺼내는 반복문. 모든 신고 횟수를 계산한 뒤 기록을 다시 확인합니다.
#         reporter, target = record.split()  # split은 구분자로 문자열 분리. ()로 묶은 여러 값은 변경 불가 튜플. =는 값 저장. 예: "muzi frodo"이면 reporter="muzi", target="frodo"입니다.
#         if reported_count[target] >= k:  # if는 조건이 참일 때 실행. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. >=는 이상 비교. >=는 크거나 같다는 비교입니다. 정확히 k번 신고되어도 정지됩니다.
#             mail_count[reporter] += 1  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. +=는 더하거나 연결한 값을 저장. 해당 상대를 신고한 사람의 메일 개수를 1 늘립니다.
#     return [mail_count[user] for user in id_list]  # return은 결과를 돌려주고 함수 종료. in은 포함 여부. []는 리스트. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. 내포문은 반복하면서 원소를 구성. 리스트 컴프리헨션으로 입력 ID 순서대로 메일 수를 모아 반환합니다.

# 풀이 요약
# 같은 사람이 같은 대상을 여러 번 신고해도 한 번이므로 신고 문자열을 집합으로 만든다. 중복을 제거한 신고에서 대상별 횟수를 구하고, 정지 기준에 도달한 대상의 신고자에게만 메일을 하나씩 더한다. 결과는 원래 ID 순서로 꺼낸다.
# 신고 R개, 사용자 U명: 평균 시간 O(R+U), 공간 O(R+U).
```

## 확인한 범위

2026-10-16 01:25:31의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
