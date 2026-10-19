# 음양 더하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/76501) · Level 1 · Python3

유형: 배열 · 부호 적용

## 풀이 원리

zip으로 절댓값과 부호를 같은 위치끼리 읽는다. 부호가 참이면 더하고 거짓이면 빼서 원래 정수들의 합을 복원한다.

원소 N개: 시간 O(N), 보조 공간 O(1).

## 공식 예제

입력 인수: `[[4, 7, 12], [true, false, true]]`

반환값: `9`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(absolutes, signs):
    answer = 0
    for number, positive in zip(absolutes, signs):
        if positive:
            answer += number
        else:
            answer -= number
    return answer

# 전체 코드 줄별 설명
# def solution(absolutes, signs):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def로 함수를 정의합니다. 절댓값 리스트와 부호 리스트를 받습니다.
#     answer = 0  # =는 값 저장. =는 대입입니다. 합계를 0으로 시작합니다.
#     for number, positive in zip(absolutes, signs):  # for·in은 원소를 차례로 꺼내는 반복문. zip은 같은 위치의 값들을 짝지음. ()로 묶은 여러 값은 변경 불가 튜플. zip은 같은 위치의 숫자와 부호를 묶습니다. 두 값을 각각 변수로 받습니다.
#         if positive:  # if는 조건이 참일 때 실행. positive는 True 또는 False입니다. True이면 아래 코드를 실행합니다.
#             answer += number  # +=는 더하거나 연결한 값을 저장. answer = answer + number와 같습니다.
#         else:  # else는 앞 조건들에 해당하지 않는 경우. positive가 False이면 실행합니다.
#             answer -= number  # -=는 빼서 저장. answer = answer - number와 같습니다.
#     return answer  # return은 결과를 돌려주고 함수 종료. 반복이 끝나면 합계를 반환하고 함수를 종료합니다.

# 풀이 요약
# zip으로 절댓값과 부호를 같은 위치끼리 읽는다. 부호가 참이면 더하고 거짓이면 빼서 원래 정수들의 합을 복원한다.
# 원소 N개: 시간 O(N), 보조 공간 O(1).
```

## 확인한 범위

2026-10-16 01:54:09의 Python3 제출 내역에서 정답 100/100을 확인했다. 원본은 그대로 보관했다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
