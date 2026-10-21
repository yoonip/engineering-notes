# 추억 점수

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/176963) · Level 1 · Python3

유형: 해시 · 합계

## 풀이 원리

이름과 그리움 점수를 딕셔너리로 연결합니다. 사진 속 이름마다 점수를 조회해 합합니다. 등록되지 않은 이름은 get의 기본값 0으로 처리하므로 사진에 낯선 사람이 있어도 따로 예외 처리가 필요 없습니다.

등록 이름 N개, 사진 속 전체 인원 P명: 평균 시간 O(N+P), 결과 포함 공간 O(N+사진 수).

## 공식 예제

입력 인수: `[["may", "kein", "kain", "radi"], [5, 10, 1, 3], [["may", "kein", "kain", "radi"], ["may", "kein", "brin", "deny"], ["kon", "kain", "may", "coni"]]]`

반환값: `[19, 15, 6]`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(name, yearning, photo):
    scores = dict(zip(name, yearning))
    answer = []
    for people in photo:
        total = 0
        for person in people:
            total += scores.get(person, 0)
        answer.append(total)
    return answer

# 전체 코드 줄별 설명
# def solution(name, yearning, photo):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 이름·그리움 점수·사진들을 입력받음.
#     scores = dict(zip(name, yearning))  # zip은 같은 위치의 값들을 짝지음. dict는 키와 값의 연결을 저장. =는 값 저장. 이름과 점수를 같은 순서로 짝지어 딕셔너리 생성.
#     answer = []  # []는 리스트. =는 값 저장. 사진별 점수 결과 리스트.
#     for people in photo:  # for·in은 원소를 차례로 꺼내는 반복문. 사진 한 장의 사람 목록을 읽음.
#         total = 0  # =는 값 저장. 이 사진의 점수 합 초기화.
#         for person in people:  # for·in은 원소를 차례로 꺼내는 반복문. 사진 속 사람을 한 명씩 확인.
#             total += scores.get(person, 0)  # get은 키 조회와 기본값 지정. +=는 더하거나 연결한 값을 저장. 등록된 점수를 더하고, 없는 사람은 0점으로 처리.
#         answer.append(total)  # append는 리스트 끝에 추가. 사진의 총점을 결과에 저장.
#     return answer  # return은 결과를 돌려주고 함수 종료. 모든 사진의 점수 리스트 반환.

# 풀이 요약
# 이름과 그리움 점수를 딕셔너리로 연결한다. 사진 속 이름마다 점수를 조회해 합한다. 등록되지 않은 이름은 get의 기본값 0으로 처리하므로 사진에 낯선 사람이 있어도 따로 예외 처리가 필요 없다.
# 등록 이름 N개, 사진 속 전체 인원 P명: 평균 시간 O(N+P), 결과 포함 공간 O(N+사진 수).
```

## 확인한 범위

2026-10-15 23:55:19의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
