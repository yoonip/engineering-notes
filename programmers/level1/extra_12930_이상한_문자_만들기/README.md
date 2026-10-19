# 이상한 문자 만들기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12930) · Level 1 · Python3

유형: 문자열 · 상태 관리

## 풀이 원리

문자열 전체가 아니라 단어 안의 인덱스로 짝수·홀수를 판단한다. 공백은 그대로 결과에 넣고 단어 인덱스를 0으로 초기화한다. 따라서 연속 공백도 유지되며 각 단어의 첫 글자부터 다시 대문자로 시작한다.

문자 수 N: 순회 O(N), 문자열 연결 복사를 포함한 보수적 시간 상한 O(N²), 공간 O(N).

## 공식 예제

입력 인수: `["try hello world"]`

반환값: `"TrY HeLlO WoRlD"`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(s):
    answer = ""
    index = 0
    for char in s:
        if char == " ":
            answer += " "
            index = 0
        else:
            if index % 2 == 0:
                answer += char.upper()
            else:
                answer += char.lower()
            index += 1
    return answer

# 전체 코드 줄별 설명
# def solution(s):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. s: 변환할 문자열을 입력받는 함수
#     answer = ""  # =는 값 저장. 변환된 글자를 저장할 빈 문자열
#     index = 0  # =는 값 저장. 공백 다음에는 새로운 단어가 시작되므로 위치를 0으로 초기화
#     for char in s:  # for·in은 원소를 차례로 꺼내는 반복문. 문자열 s에서 문자를 하나씩 꺼내 char에 저장
#         if char == " ":  # if는 조건이 참일 때 실행. ==는 같음 비교. 현재 문자가 공백인지 확인
#             answer += " "  # +=는 더하거나 연결한 값을 저장. 공백이라면 변환하지 않고 그대로 추가
#             index = 0  # =는 값 저장. 공백 다음에는 새로운 단어가 시작되므로 위치를 0으로 초기화
#         else:  # else는 앞 조건들에 해당하지 않는 경우. 글자 인덱스가 홀수라면
#             if index % 2 == 0:  # if는 조건이 참일 때 실행. ==는 같음 비교. %는 나머지. 현재 단어의 글자 인덱스가 짝수인지 확인
#                 answer += char.upper()  # upper는 대문자 변환. +=는 더하거나 연결한 값을 저장. 짝수 인덱스라면 대문자로 변환 후 추가
#             else:  # else는 앞 조건들에 해당하지 않는 경우. 글자 인덱스가 홀수라면
#                 answer += char.lower()  # lower는 소문자 변환. +=는 더하거나 연결한 값을 저장. 소문자로 변환 후 추가
#             index += 1  # +=는 더하거나 연결한 값을 저장. 글자 하나를 처리했으므로 다음 글자 위치로 이동
#     return answer  # return은 결과를 돌려주고 함수 종료. 모든 문자를 변환한 최종 문자열 반환

# 풀이 요약
# 문자열 전체가 아니라 단어 안의 인덱스로 짝수·홀수를 판단한다. 공백은 그대로 결과에 넣고 단어 인덱스를 0으로 초기화한다. 따라서 연속 공백도 유지되며 각 단어의 첫 글자부터 다시 대문자로 시작한다.
# 문자 수 N: 순회 O(N), 문자열 연결 복사를 포함한 보수적 시간 상한 O(N²), 공간 O(N).
```

## 확인한 범위

2026-10-16 02:55:23의 Python3 제출 내역에서 정답 100/100을 확인했다. 원본은 그대로 보관했다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
