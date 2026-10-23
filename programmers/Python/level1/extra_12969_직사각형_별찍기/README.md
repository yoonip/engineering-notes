# 직사각형 별찍기

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12969) · Level 1 · Python3

유형: 기초 문법 · 반복 출력

## 풀이 원리

가로 길이 n만큼 별을 반복한 문자열이 한 행입니다. 이 행을 세로 길이 m번 출력하면 직사각형이 됩니다. print가 행 끝에 줄바꿈을 붙입니다.

출력 크기 n×m: 시간 O(nm), 한 행 생성 공간 O(n).

## 공식 예제

표준 입력:

```text
5 3
```

표준 출력:

```text
*****
*****
*****
```

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
n, m = map(int, input().split())
for i in range(m):
    print("*" * n)

# 전체 코드 줄별 설명
# n, m = map(int, input().split())  # map은 각 원소에 함수 적용. input은 한 줄의 문자열 입력. split은 구분자로 문자열 분리. ()로 묶은 여러 값은 변경 불가 튜플. =는 값 저장. 두 숫자를 공백으로 구분해 입력받고, 정수 n과 m에 저장
# for i in range(m):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. 세로 길이 m만큼 반복
#     print("*" * n)  # print는 값을 표준 출력에 표시. "*"을 가로 길이 n만큼 반복하여 한 줄 출력

# 풀이 요약
# 가로 길이 n만큼 별을 반복한 문자열이 한 행이다. 이 행을 세로 길이 m번 출력하면 직사각형이 된다. print가 행 끝에 줄바꿈을 붙인다.
# 출력 크기 n×m: 시간 O(nm), 한 행 생성 공간 O(n).
```

## 확인한 범위

2026-10-16 02:31:57의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
