# 문자열 내 p와 y의 개수

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12916) · Level 1 · Python3

유형: 문자열 · 빈도 비교

## 풀이 원리

소문자로 통일한 뒤 p와 y의 등장 횟수를 비교합니다. 대문자 P와 소문자 p를 같은 문자로 세게 됩니다. 두 문자가 모두 없으면 0=0이므로 True입니다.

문자 수 N: 시간 O(N), 소문자 문자열 공간 O(N).

## 공식 예제

입력 인수: `["pPoooyY"]`

반환값: `true`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

원본에는 `solution`이 2번 정의돼 있습니다. Python은 나중에 나온 같은 이름의 정의를 사용하므로 마지막 함수가 실제로 호출됩니다. 위 실행 부분도 원본의 정의 순서를 유지했습니다.

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(s):
    s = s.lower()
    return s.count("p") == s.count("y")

def solution(s):
    s = s.lower()
    p_count = s.count("p")
    y_count = s.count("y")
    if p_count == y_count:
        return True
    else:
        return False

# 전체 코드 줄별 설명
# def solution(s):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 문자열 s를 입력받는 함수를 정의합니다.
#     s = s.lower()  # lower는 소문자 변환. =는 값 저장. lower()로 모두 소문자로 바꿔 대소문자 구분을 없앱니다.
#     return s.count("p") == s.count("y")  # return은 결과를 돌려주고 함수 종료. count는 등장 횟수. ==는 같음 비교. count()로 개수를 세고, 같으면 True, 다르면 False를 반환합니다.
# 
# def solution(s):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 문자열 s를 입력받는 함수를 정의합니다.
#     s = s.lower()  # lower는 소문자 변환. =는 값 저장. lower()로 모두 소문자로 바꿔 대소문자 구분을 없앱니다.
#     p_count = s.count("p")  # count는 등장 횟수. =는 값 저장. 소문자 p의 등장 횟수.
#     y_count = s.count("y")  # count는 등장 횟수. =는 값 저장. 소문자 y의 등장 횟수.
#     if p_count == y_count:  # if는 조건이 참일 때 실행. ==는 같음 비교. 두 등장 횟수가 같은지 비교.
#         return True  # return은 결과를 돌려주고 함수 종료. True·False는 참·거짓. 같으면 참을 반환.
#     else:  # else는 앞 조건들에 해당하지 않는 경우. 두 횟수가 다른 경우.
#         return False  # return은 결과를 돌려주고 함수 종료. True·False는 참·거짓. 거짓 반환.

# 풀이 요약
# 소문자로 통일한 뒤 p와 y의 등장 횟수를 비교한다. 대문자 P와 소문자 p를 같은 문자로 세게 된다. 두 문자가 모두 없으면 0=0이므로 True다.
# 문자 수 N: 시간 O(N), 소문자 문자열 공간 O(N).
```

## 확인한 범위

2026-10-16 17:28:57의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
