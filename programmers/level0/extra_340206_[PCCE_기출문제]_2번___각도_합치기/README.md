# [PCCE 기출문제] 2번 / 각도 합치기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/340206) · Level 0 · Python3

유형: 기초 문법 · 나머지

## 풀이 원리

두 각도를 더한 뒤 360으로 나눈 나머지를 구한다. 완전한 한 바퀴를 제거하면 같은 방향을 나타내는 0~359도의 각도가 남는다. 예를 들어 280+100은 380이고 결과는 20이다.

문제의 정수 범위에서 시간·보조 공간 O(1).

## 공식 예제

표준 입력:

```text
280
485
```

표준 출력:

```text
45
```

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있다.

## 코드와 줄별 설명

이 문제는 빈칸 채우기 또는 한 줄 수정 형식이다. 당시 정답 제출의 완성된 코드를 보관했고, 아래 문법 설명은 이번에 덧붙였다.

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
angle1 = int(input())
angle2 = int(input())
sum_angle = (angle1 + angle2) %360
print(sum_angle)

# 전체 코드 줄별 설명
# angle1 = int(input())  # int는 정수 변환. input은 한 줄의 문자열 입력. =는 값 저장. 첫 각도를 정수로 입력받음.
# angle2 = int(input())  # int는 정수 변환. input은 한 줄의 문자열 입력. =는 값 저장. 둘째 각도를 정수로 입력받음.
# sum_angle = (angle1 + angle2) %360  # %는 나머지. =는 값 저장. 각도의 합을 한 바퀴 360도로 나눈 나머지로 바꿈.
# print(sum_angle)  # print는 값을 표준 출력에 표시. 0도 이상 360도 미만인 결과 출력.

# 풀이 요약
# 두 각도를 더한 뒤 360으로 나눈 나머지를 구한다. 완전한 한 바퀴를 제거하면 같은 방향을 나타내는 0~359도의 각도가 남는다. 예를 들어 280+100은 380이고 결과는 20이다.
# 문제의 정수 범위에서 시간·보조 공간 O(1).
```

## 확인한 범위

2026-10-15 22:28:47의 Python3 제출 내역에서 정답 100/100을 확인했다. 원본은 그대로 보관했다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
