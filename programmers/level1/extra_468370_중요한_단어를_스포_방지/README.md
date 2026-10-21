# 중요한 단어를 스포 방지

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/468370) · Level 1 · Python3

유형: 문자열 · 집합

## 풀이 원리

각 문자에 가림 여부를 표시하고 공백을 기준으로 단어의 시작·끝을 찾습니다. 한 글자라도 가려진 단어는 가린 단어 집합에, 완전히 보이는 단어는 보이는 단어 집합에 넣습니다. 가린 집합에서 보이는 집합을 빼면 가려진 곳에만 등장하는 단어가 중복 없이 남습니다.

메시지 길이 N, 가린 구간 길이의 합 H: 평균 시간 O(N+H), 공간 O(N).

## 공식 예제

입력 인수: `["here is muzi here is a secret message", [[0, 3], [23, 28]]]`

반환값: `1`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(message, spoiler_ranges):
    n = len(message)
    hidden = [False] * n
    for start, end in spoiler_ranges:
        for i in range(start, end + 1):
            hidden[i] = True
    visible_words = set()
    spoiler_words = set()
    i = 0
    while i < n:
        if message[i] == " ":
            i += 1
            continue
        start = i
        while i < n and message[i] != " ":
            i += 1
        word = message[start:i]
        if any(hidden[start:i]):
            spoiler_words.add(word)
        else:
            visible_words.add(word)
    return len(spoiler_words - visible_words)

# 전체 코드 줄별 설명
# def solution(message, spoiler_ranges):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 메시지와 가려진 문자 구간을 입력받음.
#     n = len(message)  # len은 길이. =는 값 저장. 메시지의 전체 문자 수.
#     hidden = [False] * n  # []는 리스트. =는 값 저장. True·False는 참·거짓. 문자별 가림 여부를 저장하는 불리언 리스트.
#     for start, end in spoiler_ranges:  # for·in은 원소를 차례로 꺼내는 반복문. 가릴 구간의 시작·끝 번호를 꺼냄.
#         for i in range(start, end + 1):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. 끝 문자를 포함하도록 end+1까지 반복.
#             hidden[i] = True  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. True·False는 참·거짓. 현재 문자 위치를 가려졌다고 표시.
#     visible_words = set()  # set은 중복 없는 집합. =는 값 저장. 안 가려진 단어를 중복 없이 모을 집합.
#     spoiler_words = set()  # set은 중복 없는 집합. =는 값 저장. 가려진 부분과 겹친 단어를 모을 집합.
#     i = 0  # =는 값 저장. 현재 읽을 문자 위치를 0으로 시작.
#     while i < n:  # while은 조건이 참인 동안 반복. <는 작음 비교. 모든 문자를 읽을 때까지 반복.
#         if message[i] == " ":  # if는 조건이 참일 때 실행. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. ==는 같음 비교. 현재 문자가 단어 사이의 공백인지 검사.
#             i += 1  # +=는 더하거나 연결한 값을 저장. 공백 다음 문자로 이동.
#             continue  # continue는 다음 반복으로 이동. 이번 반복의 나머지를 건너뜀.
#         start = i  # =는 값 저장. 단어가 시작한 위치 보관.
#         while i < n and message[i] != " ":  # while은 조건이 참인 동안 반복. and는 두 조건 모두 참. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. !=는 다름 비교. <는 작음 비교. 메시지 끝이나 공백을 만날 때까지 진행.
#             i += 1  # +=는 더하거나 연결한 값을 저장. 다음 문자로 이동.
#         word = message[start:i]  # [시작:끝]은 끝을 제외하는 슬라이스. =는 값 저장. 시작부터 현재 위치 직전까지 단어를 추출.
#         if any(hidden[start:i]):  # if는 조건이 참일 때 실행. any는 원소 중 하나라도 참이면 참. [시작:끝]은 끝을 제외하는 슬라이스. 단어 안에 가려진 문자가 하나라도 있는지 확인.
#             spoiler_words.add(word)  # add는 집합에 원소 추가. 가려진 단어 집합에 등록.
#         else:  # else는 앞 조건들에 해당하지 않는 경우. 가려진 문자가 없는 경우.
#             visible_words.add(word)  # add는 집합에 원소 추가. 보이는 단어 집합에 등록.
#     return len(spoiler_words - visible_words)  # return은 결과를 돌려주고 함수 종료. len은 길이. 가려진 곳에만 나타난 서로 다른 단어 수 반환.

# 풀이 요약
# 각 문자에 가림 여부를 표시하고 공백을 기준으로 단어의 시작·끝을 찾는다. 한 글자라도 가려진 단어는 가린 단어 집합에, 완전히 보이는 단어는 보이는 단어 집합에 넣는다. 가린 집합에서 보이는 집합을 빼면 가려진 곳에만 등장하는 단어가 중복 없이 남는다.
# 메시지 길이 N, 가린 구간 길이의 합 H: 평균 시간 O(N+H), 공간 O(N).
```

## 확인한 범위

2026-10-15 23:33:59의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
