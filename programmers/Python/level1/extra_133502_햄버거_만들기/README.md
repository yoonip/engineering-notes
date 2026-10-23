# 햄버거 만들기

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/133502) · Level 1 · Python3

유형: 스택 · 패턴 제거

## 풀이 원리

재료를 스택에 순서대로 넣습니다. 끝 네 개가 1,2,3,1이면 햄버거를 만들고 그 네 개를 지웁니다. 제거 뒤에 새로 이어진 재료도 다음 추가에서 검사되므로 전체 배열을 처음부터 다시 탐색하지 않습니다.

재료 N개: 시간 O(N), 공간 O(N). 끝 네 원소의 비교·삭제는 고정 크기입니다.

## 공식 예제

입력 인수: `[[2, 1, 1, 2, 3, 1, 2, 3, 1]]`

반환값: `2`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(ingredient):
    stack = []
    answer = 0
    for item in ingredient:
        stack.append(item)
        if stack[-4:] == [1, 2, 3, 1]:
            del stack[-4:]
            answer += 1
    return answer

# 전체 코드 줄별 설명
# def solution(ingredient):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def로 함수를 정의합니다. ingredient는 재료 리스트를 받는 매개변수입니다.
#     stack = []  # []는 리스트. =는 값 저장. []는 빈 리스트입니다. 맨 뒤에 넣고 빼는 스택으로 사용합니다.
#     answer = 0  # =는 값 저장. =는 대입입니다. 만든 햄버거 개수를 0으로 시작합니다.
#     for item in ingredient:  # for·in은 원소를 차례로 꺼내는 반복문. 재료를 하나씩 꺼내 item에 넣으며 반복합니다.
#         stack.append(item)  # append는 리스트 끝에 추가. append()는 리스트 맨 뒤에 원소 하나를 추가합니다.
#         if stack[-4:] == [1, 2, 3, 1]:  # if는 조건이 참일 때 실행. []는 리스트. [시작:끝]은 끝을 제외하는 슬라이스. ==는 같음 비교. [-4:]는 마지막 네 원소를 읽는 슬라이싱입니다. ==로 값과 순서를 비교합니다.
#             del stack[-4:]  # del은 지정한 원소나 구간 삭제. [시작:끝]은 끝을 제외하는 슬라이스. del은 삭제 문법입니다. 원래 리스트에서 마지막 네 원소를 지웁니다.
#             answer += 1  # +=는 더하거나 연결한 값을 저장. answer = answer + 1과 같습니다.
#     return answer  # return은 결과를 돌려주고 함수 종료. 반복이 모두 끝나면 햄버거 개수를 반환하고 함수를 종료합니다.

# 풀이 요약
# 재료를 스택에 순서대로 넣는다. 끝 네 개가 1,2,3,1이면 햄버거를 만들고 그 네 개를 지운다. 제거 뒤에 새로 이어진 재료도 다음 추가에서 검사되므로 전체 배열을 처음부터 다시 탐색하지 않는다.
# 재료 N개: 시간 O(N), 공간 O(N). 끝 네 원소의 비교·삭제는 고정 크기다.
```

## 확인한 범위

2026-10-16 00:55:59의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
