# 서울에서 김서방 찾기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12919) · Level 1 · Python3

유형: 배열 · 검색 · 문자열 서식

## 풀이 원리

index로 Kim이 있는 0부터 시작하는 위치를 구합니다. f-string의 중괄호에 그 위치를 넣어 문제에서 지정한 문장을 만듭니다.

이름 수 N: 검색 시간 O(N), 보조 공간 O(1). 결과 문자열은 별도입니다.

## 공식 예제

입력 인수: `[["Jane", "Kim"]]`

반환값: `"김서방은 1에 있다"`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(seoul):
    index = seoul.index("Kim")
    answer = f"김서방은 {index}에 있다"
    return answer

# 전체 코드 줄별 설명
# def solution(seoul):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 서울 사람들의 이름 리스트를 입력받음.
#     index = seoul.index("Kim")  # index는 값이 처음 나오는 위치. =는 값 저장. Kim이 있는 위치를 찾음.
#     answer = f"김서방은 {index}에 있다"  # f-string의 {} 안에 계산한 값 삽입. =는 값 저장. 찾은 위치를 문장 안에 넣음.
#     return answer  # return은 결과를 돌려주고 함수 종료. 완성된 안내 문장 반환.

# 풀이 요약
# index로 Kim이 있는 0부터 시작하는 위치를 구한다. f-string의 중괄호에 그 위치를 넣어 문제에서 지정한 문장을 만든다.
# 이름 수 N: 검색 시간 O(N), 보조 공간 O(1). 결과 문자열은 별도다.
```

## 확인한 범위

2026-10-16 10:18:32의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
