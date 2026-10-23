# 폰켓몬

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/1845) · Level 1 · Python3

유형: 집합 · 선택 개수 제한

## 풀이 원리

고를 수 있는 마릿수는 전체의 절반이고, 서로 다른 종류 수보다 많은 종류를 고를 수는 없습니다. 종류가 충분하면 고를 수 있는 수만큼, 부족하면 종류 수만큼 고르므로 두 값의 최솟값이 답입니다.

입력 N개, 종류 U개: 평균 시간 O(N), 공간 O(U).

## 공식 예제

입력 인수: `[[3, 1, 2, 3]]`

반환값: `2`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(nums):
    answer = min(len(set(nums)), len(nums) // 2)
    return answer

# 전체 코드 줄별 설명
# def solution(nums):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. nums: 폰켓몬의 종류 번호가 들어 있는 리스트
#     answer = min(len(set(nums)), len(nums) // 2)  # len은 길이. min은 최솟값. set은 중복 없는 집합. //는 내림한 정수 몫. =는 값 저장. 서로 다른 종류 수와 선택 가능한 마릿수 중 작은 값을 저장
#     return answer  # return은 결과를 돌려주고 함수 종료. 선택할 수 있는 폰켓몬 종류의 최댓값 반환

# 풀이 요약
# 고를 수 있는 마릿수는 전체의 절반이고, 서로 다른 종류 수보다 많은 종류를 고를 수는 없다. 종류가 충분하면 고를 수 있는 수만큼, 부족하면 종류 수만큼 고르므로 두 값의 최솟값이 답이다.
# 입력 N개, 종류 U개: 평균 시간 O(N), 공간 O(U).
```

## 확인한 범위

2026-10-16 02:17:26의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
