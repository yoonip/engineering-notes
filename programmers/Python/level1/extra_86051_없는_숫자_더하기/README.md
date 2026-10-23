# 없는 숫자 더하기

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/86051) · Level 1 · Python3

유형: 수학 · 합계

## 풀이 원리

0~9의 합은 45입니다. 입력 숫자는 중복되지 않으므로 45에서 입력 합을 빼면 빠진 숫자들의 합만 남습니다.

입력 길이 N: 시간 O(N), 보조 공간 O(1).

## 공식 예제

입력 인수: `[[1, 2, 3, 4, 6, 7, 8, 0]]`

반환값: `14`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(numbers):
    answer = 45 - sum(numbers)
    return answer

# 전체 코드 줄별 설명
# def solution(numbers):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 0~9 중 일부 숫자가 담긴 리스트를 입력받음
#     answer = 45 - sum(numbers)  # sum은 원소 합. =는 값 저장. 0부터 9까지의 합 45에서 리스트에 존재하는 숫자의 합을 뺌
#     return answer  # return은 결과를 돌려주고 함수 종료. 리스트에 없는 숫자들의 합을 반환

# 풀이 요약
# 0~9의 합은 45다. 입력 숫자는 중복되지 않으므로 45에서 입력 합을 빼면 빠진 숫자들의 합만 남는다.
# 입력 길이 N: 시간 O(N), 보조 공간 O(1).
```

## 확인한 범위

2026-10-16 01:30:00의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
