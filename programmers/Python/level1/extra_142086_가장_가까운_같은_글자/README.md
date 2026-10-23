# 가장 가까운 같은 글자

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/142086) · Level 1 · Python3

유형: 해시 · 최근 위치

## 풀이 원리

문자마다 가장 최근에 등장한 인덱스를 저장합니다. 다시 등장하면 현재 위치-최근 위치가 가장 가까운 거리입니다. 처음 나온 문자는 -1을 넣고, 어느 경우든 최근 위치를 현재 인덱스로 갱신합니다.

문자 수 N: 평균 시간 O(N), 결과 포함 공간 O(N).

## 공식 예제

입력 인수: `["banana"]`

반환값: `[-1, -1, -1, 2, 2, 2]`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(s):
    answer = []
    last_position = {}
    for i, char in enumerate(s):
        if char in last_position:
            answer.append(i - last_position[char])
        else:
            answer.append(-1)
        last_position[char] = i
    return answer

# 전체 코드 줄별 설명
# def solution(s):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 검사할 문자열 s를 받는 함수
#     answer = []  # []는 리스트. =는 값 저장. 각 글자의 결과를 순서대로 저장할 빈 리스트
#     last_position = {}  # {}는 키:값을 저장하는 딕셔너리. =는 값 저장. 글자별로 가장 최근에 나온 위치를 저장할 딕셔너리
#     for i, char in enumerate(s):  # for·in은 원소를 차례로 꺼내는 반복문. enumerate는 인덱스·값을 함께 제공. ()로 묶은 여러 값은 변경 불가 튜플. 위치 i와 글자 char를 함께 꺼냄. 위치는 0부터 시작
#         if char in last_position:  # if는 조건이 참일 때 실행. in은 포함 여부. 현재 글자가 딕셔너리에 있으면 이전에 나온 글자
#             answer.append(i - last_position[char])  # append는 리스트 끝에 추가. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. 현재 위치에서 이전 위치를 빼서 결과에 추가
#         else:  # else는 앞 조건들에 해당하지 않는 경우. 딕셔너리에 없으면 처음 나온 글자
#             answer.append(-1)  # append는 리스트 끝에 추가. 앞에 같은 글자가 없다는 의미로 -1을 결과에 추가
#         last_position[char] = i  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 현재 글자의 마지막 위치를 i로 저장하거나 갱신
#     return answer  # return은 결과를 돌려주고 함수 종료. 모든 글자의 결과가 담긴 리스트를 반환

# 풀이 요약
# 문자마다 가장 최근에 등장한 인덱스를 저장한다. 다시 등장하면 현재 위치-최근 위치가 가장 가까운 거리다. 처음 나온 문자는 -1을 넣고, 어느 경우든 최근 위치를 현재 인덱스로 갱신한다.
# 문자 수 N: 평균 시간 O(N), 결과 포함 공간 O(N).
```

## 확인한 범위

2026-10-16 00:29:12의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
