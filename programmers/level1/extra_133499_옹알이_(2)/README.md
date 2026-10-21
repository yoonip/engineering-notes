# 옹알이 (2)

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/133499) · Level 1 · Python3

유형: 문자열 · 순차 파싱

## 풀이 원리

현재 위치에서 가능한 네 발음 중 하나가 시작하는지 확인합니다. 직전 발음과 같은 것은 허용하지 않습니다. 맞는 발음을 찾으면 길이만큼 이동하고, 찾지 못한 순간 그 단어는 실패합니다. 끝까지 읽힌 단어만 셉니다.

전체 글자 수 L: 시간 O(L), 보조 공간 O(1). 네 발음 길이는 고정입니다.

## 공식 예제

입력 인수: `[["aya", "yee", "u", "maa"]]`

반환값: `1`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(babbling):
    words = ["aya", "ye", "woo", "ma"]
    answer = 0
    for sound in babbling:
        i = 0
        prev = ""
        valid = True
        while i < len(sound):
            matched = False
            for word in words:
                if sound.startswith(word, i) and word != prev:
                    prev = word
                    i += len(word)
                    matched = True
                    break
            if not matched:
                valid = False
                break
        if valid:
            answer += 1
    return answer

# 전체 코드 줄별 설명
# def solution(babbling):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 옹알이 문자열들이 담긴 리스트를 입력받음
#     words = ["aya", "ye", "woo", "ma"]  # []는 리스트. =는 값 저장. 발음할 수 있는 네 가지 단어
#     answer = 0  # =는 값 저장. 발음 가능한 문자열의 개수
#     for sound in babbling:  # for·in은 원소를 차례로 꺼내는 반복문. 옹알이 문자열을 하나씩 확인
#         i = 0  # =는 값 저장. 현재 검사할 문자의 인덱스를 0으로 초기화
#         prev = ""  # =는 값 저장. 직전에 사용한 발음을 저장
#         valid = True  # =는 값 저장. True·False는 참·거짓. 현재 문자열이 발음 가능한지 표시
#         while i < len(sound):  # while은 조건이 참인 동안 반복. len은 길이. <는 작음 비교. 문자열 끝에 도달할 때까지 반복
#             matched = False  # =는 값 저장. True·False는 참·거짓. 현재 위치에서 발음을 찾았는지 표시
#             for word in words:  # for·in은 원소를 차례로 꺼내는 반복문. 가능한 네 가지 발음을 하나씩 확인
#                 if sound.startswith(word, i) and word != prev:  # if는 조건이 참일 때 실행. startswith는 지정 위치의 접두사 검사. and는 두 조건 모두 참. !=는 다름 비교. 현재 위치에서 단어가 시작하고 직전 발음과 다르면
#                     prev = word  # =는 값 저장. 현재 발음을 직전 발음으로 저장
#                     i += len(word)  # len은 길이. +=는 더하거나 연결한 값을 저장. 발음한 단어의 길이만큼 인덱스 이동
#                     matched = True  # =는 값 저장. True·False는 참·거짓. 발음 가능한 단어를 찾았다고 표시
#                     break  # break는 가장 가까운 반복문 종료. while 반복문 종료
#             if not matched:  # if는 조건이 참일 때 실행. not은 참·거짓 반전. 현재 위치에서 가능한 발음을 찾지 못했다면
#                 valid = False  # =는 값 저장. True·False는 참·거짓. 발음할 수 없는 문자열로 표시
#                 break  # break는 가장 가까운 반복문 종료. while 반복문 종료
#         if valid:  # if는 조건이 참일 때 실행. 문자열 전체를 올바르게 발음할 수 있다면
#             answer += 1  # +=는 더하거나 연결한 값을 저장. 발음 가능한 문자열 개수를 1 증가
#     return answer  # return은 결과를 돌려주고 함수 종료. 발음 가능한 문자열의 총개수 반환

# 풀이 요약
# 현재 위치에서 가능한 네 발음 중 하나가 시작하는지 확인한다. 직전 발음과 같은 것은 허용하지 않는다. 맞는 발음을 찾으면 길이만큼 이동하고, 찾지 못한 순간 그 단어는 실패한다. 끝까지 읽힌 단어만 센다.
# 전체 글자 수 L: 시간 O(L), 보조 공간 O(1). 네 발음 길이는 고정이다.
```

## 확인한 범위

2026-10-16 00:55:08의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
