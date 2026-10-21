# 기사단원의 무기

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/136798) · Level 1 · Python3

유형: 정수론 · 배수 집계

## 풀이 원리

정수 i를 약수로 가지는 수는 i의 배수들입니다. 모든 i에 대해 배수의 약수 개수를 하나씩 늘리면 각 수의 약수 개수가 완성됩니다. 제한을 초과한 수만 정해진 공격력으로 바꿔 합합니다.

최대 번호 N: 시간 O(N log N), 공간 O(N).

## 공식 예제

입력 인수: `[5, 3, 2]`

반환값: `10`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(number, limit, power):
    counts = [0] * (number + 1)
    for i in range(1, number + 1):
        for j in range(i, number + 1, i):
            counts[j] += 1
    answer = 0
    for i in range(1, number + 1):
        if counts[i] > limit:
            answer += power
        else:
            answer += counts[i]
    return answer

# 전체 코드 줄별 설명
# def solution(number, limit, power):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 기사단원 수, 공격력 제한, 대체 공격력을 입력받음
#     counts = [0] * (number + 1)  # []는 리스트. =는 값 저장. 각 숫자의 약수 개수를 저장할 리스트 생성 (0으로 초기화)
#     for i in range(1, number + 1):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. 각 기사단원의 번호를 1부터 순회
#         for j in range(i, number + 1, i):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. i의 배수들을 i 간격으로 순회 (range의 세 번째 값은 증가 간격)
#             counts[j] += 1  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. +=는 더하거나 연결한 값을 저장. i는 j의 약수이므로 j의 약수 개수를 1 증가
#     answer = 0  # =는 값 저장. 필요한 철의 총무게를 0으로 초기화
#     for i in range(1, number + 1):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. 각 기사단원의 번호를 1부터 순회
#         if counts[i] > limit:  # if는 조건이 참일 때 실행. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. >는 큼 비교. 약수 개수가 공격력 제한을 초과하면
#             answer += power  # +=는 더하거나 연결한 값을 저장. 지정된 대체 공격력을 더함
#         else:  # else는 앞 조건들에 해당하지 않는 경우. 공격력 제한 이하라면
#             answer += counts[i]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. +=는 더하거나 연결한 값을 저장. 실제 약수 개수를 더함
#     return answer  # return은 결과를 돌려주고 함수 종료. 필요한 철의 총무게 반환

# 풀이 요약
# 정수 i를 약수로 가지는 수는 i의 배수들이다. 모든 i에 대해 배수의 약수 개수를 하나씩 늘리면 각 수의 약수 개수가 완성된다. 제한을 초과한 수만 정해진 공격력으로 바꿔 합한다.
# 최대 번호 N: 시간 O(N log N), 공간 O(N).
```

## 확인한 범위

2026-10-16 00:30:46의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
