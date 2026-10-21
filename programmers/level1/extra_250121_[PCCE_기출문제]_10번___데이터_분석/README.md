# [PCCE 기출문제] 10번 / 데이터 분석

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/250121) · Level 1 · Python3

유형: 필터 · 정렬 · 딕셔너리

## 풀이 원리

항목 이름을 실제 열 번호에 연결합니다. ext 열이 val_ext보다 작은 행만 새 리스트에 넣은 뒤 sort_by 열을 기준으로 정렬합니다. lambda는 행 하나에서 정렬 기준값을 꺼내는 짧은 함수입니다.

입력 N행, 남긴 R행: 시간 O(N+R log R), 공간 O(R).

## 공식 예제

입력 인수: `[[[1, 20300104, 100, 80], [2, 20300804, 847, 37], [3, 20300401, 10, 8]], "date", 20300501, "remain"]`

반환값: `[[3, 20300401, 10, 8], [1, 20300104, 100, 80]]`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(data, ext, val_ext, sort_by):
    columns = {
        "code": 0,
        "date": 1,
        "maximum": 2,
        "remain": 3
    }
    answer = []
    for row in data:
        if row[columns[ext]] < val_ext:
            answer.append(row)
    answer.sort(key=lambda x: x[columns[sort_by]])
    return answer

# 전체 코드 줄별 설명
# def solution(data, ext, val_ext, sort_by):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 데이터·필터 항목·기준값·정렬 항목을 입력받음.
#     columns = {  # {}는 키:값을 저장하는 딕셔너리. =는 값 저장. 항목 이름을 열 번호로 연결할 딕셔너리 시작.
#         "code": 0,  # code 항목은 0번 열.
#         "date": 1,  # date 항목은 1번 열.
#         "maximum": 2,  # maximum 항목은 2번 열.
#         "remain": 3  # remain 항목은 3번 열.
#     }  # 딕셔너리 정의의 닫는 중괄호. 항목별 열 번호 정의를 마침.
#     answer = []  # []는 리스트. =는 값 저장. 남길 행을 저장할 리스트.
#     for row in data:  # for·in은 원소를 차례로 꺼내는 반복문. 데이터의 각 행을 확인.
#         if row[columns[ext]] < val_ext:  # if는 조건이 참일 때 실행. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. <는 작음 비교. 필터 항목의 값이 기준값보다 작은지 확인.
#             answer.append(row)  # append는 리스트 끝에 추가. 조건을 만족하는 행을 결과에 추가.
#     answer.sort(key=lambda x: x[columns[sort_by]])  # sort는 원래 리스트 정렬. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 이름 붙인 인수에 값 지정. lambda는 이름 없는 짧은 함수, key는 정렬 기준. 지정한 열의 값으로 결과 행들을 오름차순 정렬.
#     return answer  # return은 결과를 돌려주고 함수 종료. 필터와 정렬을 마친 행 리스트 반환.

# 풀이 요약
# 항목 이름을 실제 열 번호에 연결한다. ext 열이 val_ext보다 작은 행만 새 리스트에 넣은 뒤 sort_by 열을 기준으로 정렬한다. lambda는 행 하나에서 정렬 기준값을 꺼내는 짧은 함수다.
# 입력 N행, 남긴 R행: 시간 O(N+R log R), 공간 O(R).
```

## 확인한 범위

2026-10-15 23:48:09의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
