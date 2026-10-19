# 두 정수 사이의 합

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12912) · Level 1 · Python3

유형: 수학 · 등차수열

## 풀이 원리

a와 b 중 작은 수를 시작, 큰 수를 끝으로 둡니다. 정수 개수는 끝-시작+1이며, 연속 정수의 합은 (시작+끝)×개수/2입니다. 음수 구간에서도 같은 식이 성립합니다.

문제의 정수 범위에서 시간·보조 공간 O(1).

## 공식 예제

입력 인수: `[3, 5]`

반환값: `12`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(a, b):
    start = min(a, b)
    end = max(a, b)
    count = end - start + 1
    return (start + end) * count // 2

# 전체 코드 줄별 설명
# def solution(a, b):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def: 함수 정의, a와 b를 입력받음
#     start = min(a, b)  # min은 최솟값. =는 값 저장. min(): a와 b 중 작은 값을 start에 저장
#     end = max(a, b)  # max는 최댓값. =는 값 저장. max(): a와 b 중 큰 값을 end에 저장
#     count = end - start + 1  # =는 값 저장. 정수의 개수 계산, 양 끝값을 포함하므로 1을 더함
#     return (start + end) * count // 2  # return은 결과를 돌려주고 함수 종료. //는 내림한 정수 몫. 등차수열의 합 공식으로 계산한 결과 반환

# 풀이 요약
# a와 b 중 작은 수를 시작, 큰 수를 끝으로 둔다. 정수 개수는 끝-시작+1이며, 연속 정수의 합은 (시작+끝)×개수/2다. 음수 구간에서도 같은 식이 성립한다.
# 문제의 정수 범위에서 시간·보조 공간 O(1).
```

## 확인한 범위

2026-10-16 09:39:56의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
