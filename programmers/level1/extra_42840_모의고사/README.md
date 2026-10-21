# 모의고사

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/42840) · Level 1 · Python3

유형: 구현 · 반복 패턴

## 풀이 원리

각 수포자의 답안 패턴을 리스트로 저장합니다. 문제 번호를 패턴 길이로 나눈 나머지가 이번 답안 위치입니다. 세 사람의 맞힌 수를 구한 뒤 최고 점수인 번호를 모두 오름차순으로 반환합니다.

답안 N개: 시간 O(N), 보조 공간 O(1). 패턴과 수포자 수는 고정입니다.

## 공식 예제

입력 인수: `[[1, 2, 3, 4, 5]]`

반환값: `[1]`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(answers):
    patterns = [
        [1, 2, 3, 4, 5],
        [2, 1, 2, 3, 2, 4, 2, 5],
        [3, 3, 1, 1, 2, 2, 4, 4, 5, 5]
    ]
    scores = [0, 0, 0]
    for i, answer in enumerate(answers):
        for j in range(3):
            if answer == patterns[j][i % len(patterns[j])]:
                scores[j] += 1
    max_score = max(scores)
    result = [i + 1 for i in range(3) if scores[i] == max_score]
    return result

# 전체 코드 줄별 설명
# def solution(answers):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 실제 문제의 정답 리스트를 입력받는 함수
#     patterns = [  # []는 리스트. =는 값 저장. 3명의 수포자가 반복해서 찍는 답안 패턴
#         [1, 2, 3, 4, 5],  # []는 리스트. 1번 수포자의 반복 패턴
#         [2, 1, 2, 3, 2, 4, 2, 5],  # []는 리스트. 2번 수포자의 반복 패턴
#         [3, 3, 1, 1, 2, 2, 4, 4, 5, 5]  # []는 리스트. 3번 수포자의 반복 패턴
#     ]  # 리스트 정의의 닫는 대괄호. 세 수포자의 반복 답안 리스트 정의를 마침.
#     scores = [0, 0, 0]  # []는 리스트. =는 값 저장. 각 수포자의 정답 개수를 0으로 초기화
#     for i, answer in enumerate(answers):  # for·in은 원소를 차례로 꺼내는 반복문. enumerate는 인덱스·값을 함께 제공. ()로 묶은 여러 값은 변경 불가 튜플. 실제 정답의 인덱스 i와 정답 answer를 순서대로 가져옴
#         for j in range(3):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. 0, 1, 2번 인덱스로 세 수포자를 순회
#             if answer == patterns[j][i % len(patterns[j])]:  # if는 조건이 참일 때 실행. len은 길이. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. ==는 같음 비교. %는 나머지. 실제 정답과 해당 수포자가 찍은 답이 같으면
#                 scores[j] += 1  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. +=는 더하거나 연결한 값을 저장. 해당 수포자의 정답 개수를 1 증가
#     max_score = max(scores)  # max는 최댓값. =는 값 저장. 세 수포자 중 가장 높은 정답 개수를 구함
#     result = [i + 1 for i in range(3) if scores[i] == max_score]  # range는 끝값 직전까지 정수 순서 생성. in은 포함 여부. []는 리스트. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. 내포문은 반복하면서 원소를 구성. ==는 같음 비교. =는 값 저장. 최고 점수와 같은 수포자의 번호를 리스트로 저장
#     return result  # return은 결과를 돌려주고 함수 종료. 가장 많이 맞힌 수포자 번호들을 오름차순으로 반환

# 풀이 요약
# 각 수포자의 답안 패턴을 리스트로 저장한다. 문제 번호를 패턴 길이로 나눈 나머지가 이번 답안 위치다. 세 사람의 맞힌 수를 구한 뒤 최고 점수인 번호를 모두 오름차순으로 반환한다.
# 답안 N개: 시간 O(N), 보조 공간 O(1). 패턴과 수포자 수는 고정이다.
```

## 확인한 범위

2026-10-16 02:21:50의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
