# [PCCE 기출문제] 3번 / 수 나누기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/340205) · Level 0 · Python3

유형: 기초 문법 · 반복 · 자릿수

## 풀이 원리

100으로 나눈 나머지는 끝 두 자리이고, 100으로 나눈 몫은 그 두 자리를 제거한 앞부분입니다. 문제에서 주어진 짝수 자릿수 정수를 오른쪽부터 두 자리씩 떼어 더합니다. 예를 들어 1234는 34+12=46입니다.

두 자리 묶음 수 D: 시간 O(D), 보조 공간 O(1).

## 공식 예제

표준 입력:

```text
4859
```

표준 출력:

```text
107
```

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

이 문제는 빈칸 채우기 또는 한 줄 수정 형식입니다. 당시 정답 제출의 완성된 코드를 보관했고, 아래 문법 설명은 이번에 덧붙였습니다.

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
number = int(input())
answer = 0
while number>1:
    answer += number % 100
    number //= 100
print(answer)

# 전체 코드 줄별 설명
# number = int(input())  # int는 정수 변환. input은 한 줄의 문자열 입력. =는 값 저장. 두 자리씩 나눌 정수를 입력받음.
# answer = 0  # =는 값 저장. 두 자리 묶음의 합 초기화.
# while number>1:  # while은 조건이 참인 동안 반복. >는 큼 비교. 남은 정수 부분을 처리하는 반복 조건.
#     answer += number % 100  # +=는 더하거나 연결한 값을 저장. %는 나머지. 끝 두 자릿수를 100으로 나눈 나머지로 얻어 합산.
#     number //= 100  # //=는 정수 몫을 저장. 끝 두 자릿수를 버리도록 100으로 나눈 몫 저장.
# print(answer)  # print는 값을 표준 출력에 표시. 모든 묶음을 더한 결과 출력.

# 풀이 요약
# 100으로 나눈 나머지는 끝 두 자리이고, 100으로 나눈 몫은 그 두 자리를 제거한 앞부분이다. 문제에서 주어진 짝수 자릿수 정수를 오른쪽부터 두 자리씩 떼어 더한다. 예를 들어 1234는 34+12=46이다.
# 두 자리 묶음 수 D: 시간 O(D), 보조 공간 O(1).
```

## 확인한 범위

2026-10-15 22:35:03의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
