# 핸드폰 번호 가리기

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12948) · Level 1 · Python3

유형: 문자열 · 슬라이싱

## 풀이 원리

마지막 네 글자는 [-4:]로 보존하고 나머지 길이만큼 별을 만듭니다. 두 문자열을 연결하면 번호 길이를 유지하면서 뒤 네 자리만 보입니다.

번호 길이 N: 시간·공간 O(N).

## 공식 예제

입력 인수: `["01033334444"]`

반환값: `"*******4444"`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(phone_number):
    return "*" * (len(phone_number) - 4) + phone_number[-4:]

# 전체 코드 줄별 설명
# def solution(phone_number):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def로 함수를 정의합니다. 전화번호 문자열을 매개변수로 받습니다.
#     return "*" * (len(phone_number) - 4) + phone_number[-4:]  # return은 결과를 돌려주고 함수 종료. len은 길이. [시작:끝]은 끝을 제외하는 슬라이스. 별표 문자열과 뒤 네 자리를 연결해 반환합니다.

# 풀이 요약
# 마지막 네 글자는 [-4:]로 보존하고 나머지 길이만큼 별을 만든다. 두 문자열을 연결하면 번호 길이를 유지하면서 뒤 네 자리만 보인다.
# 번호 길이 N: 시간·공간 O(N).
```

## 확인한 범위

2026-10-16 02:47:10의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
