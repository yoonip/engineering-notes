# 평균 구하기

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12944) · Level 1 · Python3

유형: 수학 · 평균

## 풀이 원리

모든 원소의 합을 원소 수로 나눕니다. 평균은 소수일 수 있으므로 정수 몫 //가 아니라 일반 나눗셈 /를 사용합니다.

원소 N개: 시간 O(N), 보조 공간 O(1).

## 공식 예제

입력 인수: `[[1, 2, 3, 4]]`

반환값: `2.5`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(arr):
    return sum(arr) / len(arr)

# 전체 코드 줄별 설명
# def solution(arr):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def로 함수를 정의합니다. arr는 정수 리스트를 받는 매개변수입니다.
#     return sum(arr) / len(arr)  # return은 결과를 돌려주고 함수 종료. len은 길이. sum은 원소 합. sum()으로 합을 구하고 len()으로 개수를 구해 나눈 뒤 반환합니다.

# 풀이 요약
# 모든 원소의 합을 원소 수로 나눈다. 평균은 소수일 수 있으므로 정수 몫 //가 아니라 일반 나눗셈 /를 사용한다.
# 원소 N개: 시간 O(N), 보조 공간 O(1).
```

## 확인한 범위

2026-10-16 02:46:53의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
