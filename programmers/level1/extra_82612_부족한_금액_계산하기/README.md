# 부족한 금액 계산하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/82612) · Level 1 · Python3

유형: 수학 · 등차수열

## 풀이 원리

이용료는 price×1부터 price×count까지 늘어난다. 1~count의 합인 count×(count+1)/2에 price를 곱해 총액을 구한다. 가진 돈이 충분하면 부족액이 음수가 되므로 max로 0을 반환한다.

문제의 정수 범위에서 시간·보조 공간 O(1).

## 공식 예제

입력 인수: `[3, 20, 4]`

반환값: `10`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(price, money, count):
    total = price * count * (count + 1) // 2
    return max(0, total - money)

# 전체 코드 줄별 설명
# def solution(price, money, count):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. price: 기본 이용료, money: 가진 돈, count: 이용 횟수
#     total = price * count * (count + 1) // 2  # //는 내림한 정수 몫. =는 값 저장. 1회부터 count회까지의 이용료를 모두 더한 금액
#     return max(0, total - money)  # return은 결과를 돌려주고 함수 종료. max는 최댓값. 부족한 금액을 반환하되, 돈이 충분하면 0을 반환

# 풀이 요약
# 이용료는 price×1부터 price×count까지 늘어난다. 1~count의 합인 count×(count+1)/2에 price를 곱해 총액을 구한다. 가진 돈이 충분하면 부족액이 음수가 되므로 max로 0을 반환한다.
# 문제의 정수 범위에서 시간·보조 공간 O(1).
```

## 확인한 범위

2026-10-16 01:45:41의 Python3 제출 내역에서 정답 100/100을 확인했다. 원본은 그대로 보관했다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
