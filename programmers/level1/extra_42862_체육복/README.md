# 체육복

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/42862) · Level 1 · Python3

유형: 그리디 · 집합

## 풀이 원리

분실자이면서 여벌도 가진 학생은 자기 것을 써야 하므로 두 집합의 공통 원소를 먼저 제외합니다. 여벌 학생을 번호순으로 보며 왼쪽 이웃에게 먼저, 없으면 오른쪽 이웃에게 빌려줍니다. 작은 번호부터 가장 왼쪽의 미해결 수요를 처리해 뒤의 선택을 막지 않습니다.

분실 L명, 여벌 R명: 평균 시간 O(L+R log R), 공간 O(L+R).

## 공식 예제

입력 인수: `[5, [2, 4], [1, 3, 5]]`

반환값: `5`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(n, lost, reserve):
    lost_set = set(lost)
    reserve_set = set(reserve)
    need = lost_set - reserve_set
    extra = reserve_set - lost_set
    for student in sorted(extra):
        if student - 1 in need:
            need.remove(student - 1)
        elif student + 1 in need:
            need.remove(student + 1)
    return n - len(need)

# 전체 코드 줄별 설명
# def solution(n, lost, reserve):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. n: 전체 학생 수, lost: 도난당한 학생, reserve: 여벌이 있는 학생
#     lost_set = set(lost)  # set은 중복 없는 집합. =는 값 저장. 도난당한 학생 번호 목록을 집합으로 변환
#     reserve_set = set(reserve)  # set은 중복 없는 집합. =는 값 저장. 여벌이 있는 학생 번호 목록을 집합으로 변환
#     need = lost_set - reserve_set  # =는 값 저장. 도난당한 학생 중 여벌도 없는 학생 → 빌려야 할 대상
#     extra = reserve_set - lost_set  # =는 값 저장. 여벌이 있는 학생 중 도난당하지 않은 학생 → 빌려줄 수 있는 대상
#     for student in sorted(extra):  # for·in은 원소를 차례로 꺼내는 반복문. sorted는 정렬한 새 리스트. 빌려줄 수 있는 학생을 번호가 작은 순서로 하나씩 확인
#         if student - 1 in need:  # if는 조건이 참일 때 실행. in은 포함 여부. 바로 앞 번호 학생에게 체육복이 없다면
#             need.remove(student - 1)  # remove는 지정한 값의 첫 항목 삭제. 앞 학생에게 빌려주고, 필요한 학생 집합에서 제거
#         elif student + 1 in need:  # elif는 앞 조건이 거짓일 때 검사할 다음 조건. in은 포함 여부. 앞 학생에게 빌려주지 않았고, 바로 뒤 학생에게 체육복이 없다면
#             need.remove(student + 1)  # remove는 지정한 값의 첫 항목 삭제. 뒤 학생에게 빌려주고, 필요한 학생 집합에서 제거
#     return n - len(need)  # return은 결과를 돌려주고 함수 종료. len은 길이. 전체 학생 수에서 끝까지 체육복이 없는 학생 수를 빼서 반환

# 풀이 요약
# 분실자이면서 여벌도 가진 학생은 자기 것을 써야 하므로 두 집합의 공통 원소를 먼저 제외한다. 여벌 학생을 번호순으로 보며 왼쪽 이웃에게 먼저, 없으면 오른쪽 이웃에게 빌려준다. 작은 번호부터 가장 왼쪽의 미해결 수요를 처리해 뒤의 선택을 막지 않는다.
# 분실 L명, 여벌 R명: 평균 시간 O(L+R log R), 공간 O(L+R).
```

## 확인한 범위

2026-10-16 02:11:03의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
