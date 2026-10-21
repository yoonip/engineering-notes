# x만큼 간격이 있는 n개의 숫자

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12954) · Level 1 · Python3

유형: 수학 · 반복 · 리스트

## 풀이 원리

x부터 시작해 x의 1배, 2배, …, n배를 차례로 저장합니다. x가 음수여도 곱셈으로 같은 간격의 수열을 만들 수 있습니다.

반환 원소 N개: 시간·공간 O(N).

## 공식 예제

입력 인수: `[2, 5]`

반환값: `[2, 4, 6, 8, 10]`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(x, n):
    answer = []
    for i in range(1, n + 1):
        answer.append(x * i)
    return answer

# 전체 코드 줄별 설명
# def solution(x, n):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. x: 시작 숫자이자 증가 간격, n: 만들어야 할 숫자의 개수
#     answer = []  # []는 리스트. =는 값 저장. 결과 숫자들을 저장할 빈 리스트 생성
#     for i in range(1, n + 1):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. i를 1부터 n까지 1씩 증가시키면서 반복
#         answer.append(x * i)  # append는 리스트 끝에 추가. x에 i를 곱한 값을 리스트 맨 뒤에 추가
#     return answer  # return은 결과를 돌려주고 함수 종료. 완성된 숫자 리스트를 반환

# 풀이 요약
# x부터 시작해 x의 1배, 2배, …, n배를 차례로 저장한다. x가 음수여도 곱셈으로 같은 간격의 수열을 만들 수 있다.
# 반환 원소 N개: 시간·공간 O(N).
```

## 확인한 범위

2026-10-16 02:34:28의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
