# 내적

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/70128) · Level 1 · Python3

유형: 배열 · 누적 합

## 풀이 원리

같은 위치의 원소끼리 곱한 값을 더하면 내적입니다. zip이 두 배열의 대응 원소를 한 쌍씩 꺼내므로 별도의 인덱스 관리가 필요 없습니다.

배열 길이 N: 시간 O(N), 보조 공간 O(1).

## 공식 예제

입력 인수: `[[1, 2, 3, 4], [-3, -1, 0, 2]]`

반환값: `3`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(a, b):
    answer = 0
    for x, y in zip(a, b):
        answer += x * y
    return answer

# 전체 코드 줄별 설명
# def solution(a, b):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 두 정수 배열 a와 b를 입력받는 함수
#     answer = 0  # =는 값 저장. 내적 결과를 저장할 변수를 0으로 초기화
#     for x, y in zip(a, b):  # for·in은 원소를 차례로 꺼내는 반복문. zip은 같은 위치의 값들을 짝지음. ()로 묶은 여러 값은 변경 불가 튜플. zip()으로 두 배열의 같은 위치에 있는 값을 묶어 순회
#         answer += x * y  # +=는 더하거나 연결한 값을 저장. 같은 위치의 두 숫자를 곱해서 answer에 누적
#     return answer  # return은 결과를 돌려주고 함수 종료. 계산한 내적 결과 반환

# 풀이 요약
# 같은 위치의 원소끼리 곱한 값을 더하면 내적이다. zip이 두 배열의 대응 원소를 한 쌍씩 꺼내므로 별도의 인덱스 관리가 필요 없다.
# 배열 길이 N: 시간 O(N), 보조 공간 O(1).
```

## 확인한 범위

2026-10-16 02:26:27의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
