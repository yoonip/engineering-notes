# 약수의 합

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12928) · Level 1 · Python3

유형: 정수론 · 약수

## 풀이 원리

1부터 n까지의 정수 중 n을 나눈 나머지가 0인 수만 더합니다. n=0이면 range가 비어 합계의 초기값 0을 반환합니다.

입력 N: 시간 O(N), 보조 공간 O(1).

## 공식 예제

입력 인수: `[12]`

반환값: `28`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(n):
    answer = 0
    for i in range(1, n + 1):
        if n % i == 0:
            answer += i
    return answer

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def는 함수를 정의하는 명령어, n은 입력받는 정수
#     answer = 0  # =는 값 저장. 약수의 합을 저장할 변수, 처음에는 0으로 초기화
#     for i in range(1, n + 1):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. for는 반복문, i는 1부터 n까지 차례대로 증가
#         if n % i == 0:  # if는 조건이 참일 때 실행. ==는 같음 비교. %는 나머지. if는 조건문, %는 나머지 연산, 나머지가 0이면 i는 n의 약수
#             answer += i  # +=는 더하거나 연결한 값을 저장. answer = answer + i 와 같음, 약수 i를 합계에 더함
#     return answer  # return은 결과를 돌려주고 함수 종료. return은 함수의 결과를 반환하고 함수를 종료

# 풀이 요약
# 1부터 n까지의 정수 중 n을 나눈 나머지가 0인 수만 더한다. n=0이면 range가 비어 합계의 초기값 0을 반환한다.
# 입력 N: 시간 O(N), 보조 공간 O(1).
```

## 확인한 범위

2026-10-16 09:54:45의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
