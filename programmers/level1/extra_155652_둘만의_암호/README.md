# 둘만의 암호

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/155652) · Level 1 · Python3

유형: 문자열 · 순환 인덱스

## 풀이 원리

skip에 없는 알파벳만 순서대로 이어 새 알파벳표를 만듭니다. 현재 문자의 표 안 위치에 index를 더하고 표 길이로 나눈 나머지를 쓰면 z 뒤에서 다시 처음으로 돌아갑니다. 건너뛸 문자를 표에서 미리 제거했으므로 이동할 때 다시 검사하지 않습니다.

문자 수 N: 알파벳 조회 O(N), 문자열 연결 복사를 포함한 보수적 시간 상한 O(N²), 공간 O(N).

## 공식 예제

입력 인수: `["aukks", "wbqd", 5]`

반환값: `"happy"`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(s, skip, index):
    alphabet = ""
    for char in "abcdefghijklmnopqrstuvwxyz":
        if char not in skip:
            alphabet += char
    answer = ""
    for char in s:
        position = alphabet.index(char)
        next_position = (position + index) % len(alphabet)
        answer += alphabet[next_position]
    return answer

# 전체 코드 줄별 설명
# def solution(s, skip, index):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def는 함수 정의입니다. 세 매개변수로 입력을 받습니다.
#     alphabet = ""  # =는 값 저장. ""는 빈 문자열입니다. =로 변수에 값을 저장합니다.
#     for char in "abcdefghijklmnopqrstuvwxyz":  # for·in은 원소를 차례로 꺼내는 반복문. 문자열에서 글자를 하나씩 꺼내 반복합니다.
#         if char not in skip:  # if는 조건이 참일 때 실행. not in은 포함되지 않음. not in은 해당 글자가 skip에 포함되지 않았는지 검사합니다.
#             alphabet += char  # +=는 더하거나 연결한 값을 저장. alphabet = alphabet + char와 같습니다. 글자를 뒤에 붙입니다.
#     answer = ""  # =는 값 저장. 변환 결과를 저장할 빈 문자열입니다.
#     for char in s:  # for·in은 원소를 차례로 꺼내는 반복문. 입력 문자열 s의 글자를 순서대로 하나씩 처리합니다.
#         position = alphabet.index(char)  # index는 값이 처음 나오는 위치. =는 값 저장. .index()는 글자의 위치를 구합니다. 위치는 0부터입니다.
#         next_position = (position + index) % len(alphabet)  # len은 길이. %는 나머지. =는 값 저장. len()은 길이, %는 나머지입니다. 길이가 22라면 위치 22는 0으로 돌아옵니다.
#         answer += alphabet[next_position]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. +=는 더하거나 연결한 값을 저장. 문자열[위치]로 변환할 글자를 읽어 결과 뒤에 붙입니다.
#     return answer  # return은 결과를 돌려주고 함수 종료. 완성한 문자열을 반환합니다. for문 바깥이므로 모든 글자를 처리한 뒤 실행됩니다.

# 풀이 요약
# skip에 없는 알파벳만 순서대로 이어 새 알파벳표를 만든다. 현재 문자의 표 안 위치에 index를 더하고 표 길이로 나눈 나머지를 쓰면 z 뒤에서 다시 처음으로 돌아간다. 건너뛸 문자를 표에서 미리 제거했으므로 이동할 때 다시 검사하지 않는다.
# 문자 수 N: 알파벳 조회 O(N), 문자열 연결 복사를 포함한 보수적 시간 상한 O(N²), 공간 O(N).
```

## 확인한 범위

2026-10-16 00:21:37의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
