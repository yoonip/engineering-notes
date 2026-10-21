# 숫자 짝꿍

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/131128) · Level 1 · Python3

유형: 문자열 · 빈도 집계

## 풀이 원리

각 숫자를 양쪽에서 쓸 수 있는 횟수는 두 문자열의 등장 횟수 중 작은 값입니다. 9부터 0까지 그 개수만큼 이어 붙여 가장 큰 수를 만듭니다. 공통 숫자가 없으면 -1, 0만 있으면 0 하나를 반환합니다.

입력 길이 X,Y와 결과 길이 L: 시간 O(X+Y+L), 공간 O(L). 숫자 종류는 10개입니다.

## 공식 예제

입력 인수: `["100", "2345"]`

반환값: `"-1"`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(X, Y):
    parts = []
    for digit in "9876543210":
        count = min(X.count(digit), Y.count(digit))
        parts.append(digit * count)
    answer = "".join(parts)
    if answer == "":
        return "-1"
    if answer[0] == "0":
        return "0"
    return answer

# 전체 코드 줄별 설명
# def solution(X, Y):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 숫자로 이루어진 문자열 X와 Y를 받는 함수
#     parts = []  # []는 리스트. =는 값 저장. 공통으로 사용할 숫자들을 문자열 조각으로 저장할 리스트
#     for digit in "9876543210":  # for·in은 원소를 차례로 꺼내는 반복문. 문자 "9"부터 "0"까지 큰 숫자 순서로 하나씩 확인
#         count = min(X.count(digit), Y.count(digit))  # min은 최솟값. count는 등장 횟수. =는 값 저장. 두 문자열에서 해당 숫자가 나온 횟수 중 작은 값
#         parts.append(digit * count)  # append는 리스트 끝에 추가. 해당 숫자를 count번 반복한 문자열을 리스트에 추가
#     answer = "".join(parts)  # join은 문자열들을 구분자로 연결. =는 값 저장. 저장한 문자열 조각들을 구분자 없이 하나로 이어 붙임
#     if answer == "":  # if는 조건이 참일 때 실행. ==는 같음 비교. 만들어진 문자열이 비어 있다면 공통 숫자가 하나도 없는 경우
#         return "-1"  # return은 결과를 돌려주고 함수 종료. 짝꿍이 없다는 뜻의 문자열 "-1"을 반환하고 함수 종료
#     if answer[0] == "0":  # if는 조건이 참일 때 실행. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. ==는 같음 비교. 큰 순서로 붙였는데 첫 글자가 "0"이면 모든 글자가 "0"임
#         return "0"  # return은 결과를 돌려주고 함수 종료. "00", "000"처럼 여러 개여도 문자열 "0" 하나만 반환
#     return answer  # return은 결과를 돌려주고 함수 종료. 공통 숫자들로 만든 가장 큰 수를 문자열 그대로 반환

# 풀이 요약
# 각 숫자를 양쪽에서 쓸 수 있는 횟수는 두 문자열의 등장 횟수 중 작은 값이다. 9부터 0까지 그 개수만큼 이어 붙여 가장 큰 수를 만든다. 공통 숫자가 없으면 -1, 0만 있으면 0 하나를 반환한다.
# 입력 길이 X,Y와 결과 길이 L: 시간 O(X+Y+L), 공간 O(L). 숫자 종류는 10개다.
```

## 확인한 범위

2026-10-16 01:08:23의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
