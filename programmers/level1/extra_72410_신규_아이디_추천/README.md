# 신규 아이디 추천

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/72410) · Level 1 · Python3

유형: 문자열 · 규칙 적용

## 풀이 원리

소문자 변환, 허용 문자 필터, 연속 마침표 축약, 양끝 마침표 제거를 순서대로 수행합니다. 비면 a를 넣고 15자로 자른 뒤 끝 마침표를 다시 제거합니다. 3자보다 짧으면 마지막 문자를 반복해 길이를 채웁니다. 앞 단계의 결과가 다음 단계의 입력이 됩니다.

길이 N: 문자열 연결·반복 치환을 포함한 보수적 시간 상한 O(N²), 공간 O(N).

## 공식 예제

입력 인수: `["...!@BaT#*..y.abcdefghijklm"]`

반환값: `"bat.y.abcdefghi"`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(new_id):
    new_id = new_id.lower()
    answer = ""
    for char in new_id:
        if char.isalnum() or char in "-_.":
            answer += char
    while ".." in answer:
        answer = answer.replace("..", ".")
    answer = answer.strip(".")
    if not answer:
        answer = "a"
    answer = answer[:15].rstrip(".")
    while len(answer) < 3:
        answer += answer[-1]
    return answer

# 전체 코드 줄별 설명
# def solution(new_id):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def로 함수를 정의합니다. new_id는 입력 문자열을 받습니다.
#     new_id = new_id.lower()  # lower는 소문자 변환. =는 값 저장. [1단계] lower()로 소문자로 바꾼 문자열을 만들어 다시 저장합니다.
#     answer = ""  # =는 값 저장. 허용된 글자들을 모을 빈 문자열입니다.
#     for char in new_id:  # for·in은 원소를 차례로 꺼내는 반복문. 입력 문자열에서 글자를 하나씩 꺼냅니다.
#         if char.isalnum() or char in "-_.":  # if는 조건이 참일 때 실행. isalnum은 글자·숫자 여부 검사. in은 포함 여부. or는 한 조건 이상 참. [2단계] 문자·숫자인지, 또는 허용 특수문자인지 검사합니다. or는 둘 중 하나가 참이면 참입니다.
#             answer += char  # +=는 더하거나 연결한 값을 저장. 허용된 글자를 뒤에 붙입니다. answer = answer + char와 같습니다.
#     while ".." in answer:  # while은 조건이 참인 동안 반복. in은 포함 여부. [3단계] ".."가 포함되어 있는 동안 반복합니다.
#         answer = answer.replace("..", ".")  # replace는 문자열 치환. =는 값 저장. 두 마침표를 하나로 교체한 새 문자열을 다시 저장합니다.
#     answer = answer.strip(".")  # strip은 양끝에서 지정 문자 제거. =는 값 저장. [4단계] strip(".")은 양끝의 마침표를 제거합니다. 중간은 그대로 둡니다.
#     if not answer:  # if는 조건이 참일 때 실행. not은 참·거짓 반전. [5단계] 빈 문자열은 거짓으로 취급됩니다. not으로 뒤집어 비었을 때 실행합니다.
#         answer = "a"  # =는 값 저장. 빈 문자열 대신 "a"를 저장합니다.
#     answer = answer[:15].rstrip(".")  # rstrip은 오른쪽 끝에서 지정 문자 제거. [시작:끝]은 끝을 제외하는 슬라이스. =는 값 저장. [6단계] [:15]로 앞의 15글자를 남기고, rstrip(".")으로 오른쪽 끝 마침표를 제거합니다.
#     while len(answer) < 3:  # while은 조건이 참인 동안 반복. len은 길이. <는 작음 비교. [7단계] len()은 길이입니다. 3글자 미만인 동안 반복합니다.
#         answer += answer[-1]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. +=는 더하거나 연결한 값을 저장. [-1]은 마지막 글자입니다. 그 글자를 끝에 하나 더 붙입니다.
#     return answer  # return은 결과를 돌려주고 함수 종료. 완성된 추천 아이디를 반환하고 함수를 종료합니다.

# 풀이 요약
# 소문자 변환, 허용 문자 필터, 연속 마침표 축약, 양끝 마침표 제거를 순서대로 수행한다. 비면 a를 넣고 15자로 자른 뒤 끝 마침표를 다시 제거한다. 3자보다 짧으면 마지막 문자를 반복해 길이를 채운다. 앞 단계의 결과가 다음 단계의 입력이 된다.
# 길이 N: 문자열 연결·반복 치환을 포함한 보수적 시간 상한 O(N²), 공간 O(N).
```

## 확인한 범위

2026-10-16 01:59:14의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
