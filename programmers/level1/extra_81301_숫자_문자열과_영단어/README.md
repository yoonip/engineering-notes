# 숫자 문자열과 영단어

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/81301) · Level 1 · Python3

유형: 문자열 · 치환

## 풀이 원리

숫자 영어 이름을 0부터 9 순서의 리스트에 둔다. enumerate로 이름과 숫자를 함께 얻어 해당 영어 단어를 숫자 한 글자로 바꾼다. 모든 단어를 처리한 뒤 전체 문자열을 정수로 바꾼다.

문자열 길이 N: 시간 O(N), 공간 O(N). 단어 종류와 길이는 고정이다.

## 공식 예제

입력 인수: `["one4seveneight"]`

반환값: `1478`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(s):
    words = [
        "zero", "one", "two", "three", "four",
        "five", "six", "seven", "eight", "nine"
    ]
    for number, word in enumerate(words):
        s = s.replace(word, str(number))
    return int(s)

# 전체 코드 줄별 설명
# def solution(s):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def로 함수를 정의합니다. s는 입력 문자열을 받습니다.
#     words = [  # []는 리스트. =는 값 저장. 대괄호로 리스트를 만듭니다. 숫자 순서대로 영단어를 저장합니다.
#         "zero", "one", "two", "three", "four",  # 인덱스는 0부터입니다. words[0]은 "zero"입니다.
#         "five", "six", "seven", "eight", "nine"  # 쉼표로 원소를 구분합니다. 따옴표 안의 값은 문자열입니다.
#     ]  # 리스트 정의의 닫는 대괄호. 리스트의 끝입니다.
#     for number, word in enumerate(words):  # for·in은 원소를 차례로 꺼내는 반복문. enumerate는 인덱스·값을 함께 제공. ()로 묶은 여러 값은 변경 불가 튜플. enumerate는 인덱스와 원소를 함께 제공합니다. 예: number=1, word="one".
#         s = s.replace(word, str(number))  # str은 문자열 변환. replace는 문자열 치환. =는 값 저장. str()로 숫자를 문자열로 바꿉니다. replace(기존, 새값)는 일치하는 부분을 모두 교체합니다.
#     return int(s)  # return은 결과를 돌려주고 함수 종료. int는 정수 변환. int()로 숫자 문자열을 정수로 바꾸어 반환하고 함수를 종료합니다.

# 풀이 요약
# 숫자 영어 이름을 0부터 9 순서의 리스트에 둔다. enumerate로 이름과 숫자를 함께 얻어 해당 영어 단어를 숫자 한 글자로 바꾼다. 모든 단어를 처리한 뒤 전체 문자열을 정수로 바꾼다.
# 문자열 길이 N: 시간 O(N), 공간 O(N). 단어 종류와 길이는 고정이다.
```

## 확인한 범위

2026-10-16 01:49:02의 Python3 제출 내역에서 정답 100/100을 확인했다. 원본은 그대로 보관했다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
