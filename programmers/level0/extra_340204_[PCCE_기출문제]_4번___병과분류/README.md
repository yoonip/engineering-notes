# [PCCE 기출문제] 4번 / 병과분류

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/340204) · Level 0 · Python3

유형: 기초 문법 · 조건 분기

## 풀이 원리

코드 전체가 아니라 마지막 네 글자로 병과를 구분합니다. 슬라이스 [-4:]로 접미사를 얻고 if·elif를 위에서부터 비교합니다. 어느 조건도 맞지 않으면 else의 안내를 출력합니다. 출력 철자는 문제에서 지정한 문자열을 유지합니다.

접미사 길이가 4로 고정되어 분류 시간·보조 공간 O(1). 입력 문자열 저장은 O(N).

## 공식 예제

표준 입력:

```text
dry_eye
```

표준 출력:

```text
Ophthalmologyc
```

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

이 문제는 빈칸 채우기 또는 한 줄 수정 형식입니다. 당시 정답 제출의 완성된 코드를 보관했고, 아래 문법 설명은 이번에 덧붙였습니다.

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
code = input()
last_four_words = code[-4:]
if last_four_words == "_eye":
    print("Ophthalmologyc")
elif last_four_words == "head":
    print("Neurosurgery")
elif last_four_words == "infl":
    print("Orthopedics")
elif last_four_words == "skin":
    print("Dermatology")
else:
    print("direct recommendation")

# 전체 코드 줄별 설명
# code = input()  # input은 한 줄의 문자열 입력. =는 값 저장. 분류할 코드 문자열을 입력받음.
# last_four_words = code[-4:]  # [시작:끝]은 끝을 제외하는 슬라이스. =는 값 저장. 마지막 네 글자를 잘라 분류 기준으로 저장.
# if last_four_words == "_eye":  # if는 조건이 참일 때 실행. ==는 같음 비교. 끝 네 글자가 안과 코드인지 비교.
#     print("Ophthalmologyc")  # print는 값을 표준 출력에 표시. 문제에서 정한 안과 문자열 출력.
# elif last_four_words == "head":  # elif는 앞 조건이 거짓일 때 검사할 다음 조건. ==는 같음 비교. 신경외과 코드인지 비교.
#     print("Neurosurgery")  # print는 값을 표준 출력에 표시. 신경외과 이름 출력.
# elif last_four_words == "infl":  # elif는 앞 조건이 거짓일 때 검사할 다음 조건. ==는 같음 비교. 정형외과 코드인지 비교.
#     print("Orthopedics")  # print는 값을 표준 출력에 표시. 정형외과 이름 출력.
# elif last_four_words == "skin":  # elif는 앞 조건이 거짓일 때 검사할 다음 조건. ==는 같음 비교. 피부과 코드인지 비교.
#     print("Dermatology")  # print는 값을 표준 출력에 표시. 피부과 이름 출력.
# else:  # else는 앞 조건들에 해당하지 않는 경우. 어느 코드에도 해당하지 않는 경우.
#     print("direct recommendation")  # print는 값을 표준 출력에 표시. 직접 추천 문구 출력.

# 풀이 요약
# 코드 전체가 아니라 마지막 네 글자로 병과를 구분한다. 슬라이스 [-4:]로 접미사를 얻고 if·elif를 위에서부터 비교한다. 어느 조건도 맞지 않으면 else의 안내를 출력한다. 출력 철자는 문제에서 지정한 문자열을 유지한다.
# 접미사 길이가 4로 고정되어 분류 시간·보조 공간 O(1). 입력 문자열 저장은 O(N).
```

## 확인한 범위

2026-10-15 22:42:50의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
