# [PCCE 기출문제] 1번 / 문자 출력

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/340207) · Level 0 · Python3

유형: 기초 문법 · 문자열 출력

## 풀이 원리

문자열의 작은따옴표를 포함할 수 있도록 큰따옴표로 문장을 저장한다. 문자열 안의 역슬래시 n은 줄바꿈 문자이므로 3, 2, 1을 각각 다른 줄에 출력한 뒤 문장을 출력한다.

출력 길이가 고정되어 시간·보조 공간 O(1).

## 공식 예제

표준 입력:

```text

```

표준 출력:

```text
3
2
1
Let's go!
```

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있다.

## 코드와 줄별 설명

이 문제는 빈칸 채우기 또는 한 줄 수정 형식이다. 당시 정답 제출의 완성된 코드를 보관했고, 아래 문법 설명은 이번에 덧붙였다.

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
message = "Let's go!"
print("3\n2\n1")
print(message)

# 전체 코드 줄별 설명
# message = "Let's go!"  # =는 값 저장. 출력할 문장을 문자열 변수에 저장.
# print("3\n2\n1")  # print는 값을 표준 출력에 표시. 줄바꿈을 넣어 3·2·1을 서로 다른 줄에 출력.
# print(message)  # print는 값을 표준 출력에 표시. 변수에 저장한 문장을 출력.

# 풀이 요약
# 문자열의 작은따옴표를 포함할 수 있도록 큰따옴표로 문장을 저장한다. 문자열 안의 역슬래시 n은 줄바꿈 문자이므로 3, 2, 1을 각각 다른 줄에 출력한 뒤 문장을 출력한다.
# 출력 길이가 고정되어 시간·보조 공간 O(1).
```

## 확인한 범위

2026-10-14 23:13:56의 Python3 제출 내역에서 정답 100/100을 확인했다. 원본은 그대로 보관했다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
