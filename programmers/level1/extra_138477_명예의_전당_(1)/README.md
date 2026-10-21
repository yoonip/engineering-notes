# 명예의 전당 (1)

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/138477) · Level 1 · Python3

유형: 정렬 · 상위 K개 유지

## 풀이 원리

매일 새 점수를 넣고 오름차순으로 정렬합니다. k개를 초과하면 최솟값을 제거해 가장 큰 k개만 남깁니다. 이 리스트의 첫 값이 그날 명예의 전당 최저 점수입니다. 실제 제출본은 힙이 아니라 정렬 리스트를 사용합니다.

점수 N개: 시간 상한 O(NK log(K+1)), 결과 포함 공간 O(N+K).

## 공식 예제

입력 인수: `[3, [10, 100, 20, 150, 1, 100, 200]]`

반환값: `[10, 10, 10, 20, 20, 100, 100]`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(k, score):
    answer = []
    hall = []
    for point in score:
        hall.append(point)
        hall.sort()
        if len(hall) > k:
            hall.pop(0)
        answer.append(hall[0])
    return answer

# 전체 코드 줄별 설명
# def solution(k, score):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. k: 명예의 전당 정원, score: 날짜순으로 주어진 점수 목록
#     answer = []  # []는 리스트. =는 값 저장. 매일 발표하는 최하위 점수를 순서대로 저장할 리스트
#     hall = []  # []는 리스트. =는 값 저장. 현재 명예의 전당에 들어 있는 점수들을 저장할 리스트
#     for point in score:  # for·in은 원소를 차례로 꺼내는 반복문. 첫날부터 마지막 날까지 점수를 하나씩 꺼냄
#         hall.append(point)  # append는 리스트 끝에 추가. 오늘의 점수를 명예의 전당 목록에 일단 추가
#         hall.sort()  # sort는 원래 리스트 정렬. 점수를 작은 값부터 큰 값 순서로 정렬
#         if len(hall) > k:  # if는 조건이 참일 때 실행. len은 길이. >는 큼 비교. 저장된 점수 개수가 정원 k를 초과하면
#             hall.pop(0)  # pop은 지정 위치를 꺼내고 삭제, 생략하면 마지막. 0번 위치의 가장 작은 점수를 하나 제거
#         answer.append(hall[0])  # append는 리스트 끝에 추가. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. 남아 있는 점수 중 가장 작은 값을 오늘의 발표 점수로 저장
#     return answer  # return은 결과를 돌려주고 함수 종료. 첫날부터 마지막 날까지의 발표 점수 목록을 반환

# 풀이 요약
# 매일 새 점수를 넣고 오름차순으로 정렬한다. k개를 초과하면 최솟값을 제거해 가장 큰 k개만 남긴다. 이 리스트의 첫 값이 그날 명예의 전당 최저 점수다. 실제 제출본은 힙이 아니라 정렬 리스트를 사용한다.
# 점수 N개: 시간 상한 O(NK log(K+1)), 결과 포함 공간 O(N+K).
```

## 확인한 범위

2026-10-16 00:50:35의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
