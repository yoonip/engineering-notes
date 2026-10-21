# 성격 유형 검사하기

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/118666) · Level 1 · Python3

유형: 해시 · 점수 집계

## 풀이 원리

선택값 4를 중립으로 두고 작으면 앞 유형에, 크면 뒤 유형에 차이만큼 점수를 줍니다. 네 유형 쌍을 정해진 순서로 비교하고 동점이면 사전순으로 앞선 첫 글자를 고릅니다.

질문 N개: 시간 O(N), 보조 공간 O(1). 유형은 8개로 고정입니다.

## 공식 예제

입력 인수: `[["AN", "CF", "MJ", "RT", "NA"], [5, 3, 2, 7, 5]]`

반환값: `"TCMA"`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(survey, choices):
    points = {char: 0 for char in "RTCFJMAN"}
    for pair, choice in zip(survey, choices):
        if choice < 4:
            points[pair[0]] += 4 - choice
        elif choice > 4:
            points[pair[1]] += choice - 4
    answer = ""
    for first, second in ["RT", "CF", "JM", "AN"]:
        if points[first] >= points[second]:
            answer += first
        else:
            answer += second
    return answer

# 전체 코드 줄별 설명
# def solution(survey, choices):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def는 함수 정의입니다. 질문과 응답 리스트를 매개변수로 받습니다.
#     points = {char: 0 for char in "RTCFJMAN"}  # in은 포함 여부. {}는 키:값을 저장하는 딕셔너리. 내포문은 반복하면서 원소를 구성. =는 값 저장. 딕셔너리 컴프리헨션입니다. 각 글자를 키로, 0을 값으로 저장합니다.
#     for pair, choice in zip(survey, choices):  # for·in은 원소를 차례로 꺼내는 반복문. zip은 같은 위치의 값들을 짝지음. ()로 묶은 여러 값은 변경 불가 튜플. zip은 같은 위치의 질문과 응답을 묶습니다. 두 값을 각각 변수로 받습니다.
#         if choice < 4:  # if는 조건이 참일 때 실행. <는 작음 비교. <는 작다는 비교입니다. 응답이 1, 2, 3이면 실행합니다.
#             points[pair[0]] += 4 - choice  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. +=는 더하거나 연결한 값을 저장. pair[0]은 질문의 첫 글자입니다. 해당 유형에 각각 3, 2, 1점을 더합니다.
#         elif choice > 4:  # elif는 앞 조건이 거짓일 때 검사할 다음 조건. >는 큼 비교. elif는 앞 조건이 거짓일 때 검사합니다. 응답이 4면 어느 분기도 실행하지 않습니다.
#             points[pair[1]] += choice - 4  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. +=는 더하거나 연결한 값을 저장. pair[1]은 둘째 글자입니다. 응답 5, 6, 7에 각각 1, 2, 3점을 더합니다.
#     answer = ""  # =는 값 저장. 결과를 담을 빈 문자열입니다.
#     for first, second in ["RT", "CF", "JM", "AN"]:  # for·in은 원소를 차례로 꺼내는 반복문. []는 리스트. 두 글자 문자열을 각각 변수에 나눠 받습니다. 예: first="R", second="T".
#         if points[first] >= points[second]:  # if는 조건이 참일 때 실행. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. >=는 이상 비교. >=는 크거나 같다는 비교입니다. 첫 글자가 사전순으로 앞서므로 동점도 처리합니다.
#             answer += first  # +=는 더하거나 연결한 값을 저장. 문자열을 뒤에 붙여 저장합니다. answer = answer + first와 같습니다.
#         else:  # else는 앞 조건들에 해당하지 않는 경우. 둘째 유형의 점수가 더 높으면 실행합니다.
#             answer += second  # +=는 더하거나 연결한 값을 저장. 둘째 글자를 결과 뒤에 붙입니다.
#     return answer  # return은 결과를 돌려주고 함수 종료. 모든 비교가 끝나면 네 글자 문자열을 반환하고 함수를 종료합니다.

# 풀이 요약
# 선택값 4를 중립으로 두고 작으면 앞 유형에, 크면 뒤 유형에 차이만큼 점수를 준다. 네 유형 쌍을 정해진 순서로 비교하고 동점이면 사전순으로 앞선 첫 글자를 고른다.
# 질문 N개: 시간 O(N), 보조 공간 O(1). 유형은 8개로 고정이다.
```

## 확인한 범위

2026-10-16 01:04:54의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
