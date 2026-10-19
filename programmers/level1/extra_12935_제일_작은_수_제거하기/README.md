# 제일 작은 수 제거하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12935) · Level 1 · Python3

유형: 배열 · 최솟값 제거

## 풀이 원리

min으로 가장 작은 값을 구하고 remove로 그 값을 배열에서 지운다. 원소가 하나뿐이었다면 빈 배열이 되므로 [-1]을 반환한다. remove는 위치가 아니라 값을 받으며 입력 리스트를 직접 바꾼다.

원소 N개: 시간 O(N), 보조 공간 O(1).

## 공식 예제

입력 인수: `[[4, 3, 2, 1]]`

반환값: `[4, 3, 2]`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(arr):
    arr.remove(min(arr))
    if len(arr) == 0:
        return [-1]
    return arr

# 전체 코드 줄별 설명
# def solution(arr):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. arr: 정수들이 저장된 리스트를 입력받는 함수
#     arr.remove(min(arr))  # min은 최솟값. remove는 지정한 값의 첫 항목 삭제. min()으로 가장 작은 값을 찾고 remove()로 제거
#     if len(arr) == 0:  # if는 조건이 참일 때 실행. len은 길이. ==는 같음 비교. 숫자를 제거한 후 리스트의 원소가 0개인지 확인
#         return [-1]  # return은 결과를 돌려주고 함수 종료. []는 리스트. 리스트가 비었으면 [-1]을 반환하고 함수 종료
#     return arr  # return은 결과를 돌려주고 함수 종료. 남은 숫자들이 들어 있는 리스트를 반환

# 풀이 요약
# min으로 가장 작은 값을 구하고 remove로 그 값을 배열에서 지운다. 원소가 하나뿐이었다면 빈 배열이 되므로 [-1]을 반환한다. remove는 위치가 아니라 값을 받으며 입력 리스트를 직접 바꾼다.
# 원소 N개: 시간 O(N), 보조 공간 O(1).
```

## 확인한 범위

2026-10-16 02:52:21의 Python3 제출 내역에서 정답 100/100을 확인했다. 원본은 그대로 보관했다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
