# 행렬의 덧셈

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12950) · Level 1 · Python3

유형: 배열 · 2차원 반복

## 풀이 원리

두 행렬의 같은 행·열 위치끼리 더합니다. 행 하나를 만든 뒤 바깥 결과 리스트에 넣어 원래와 같은 행렬 모양을 유지합니다.

R행 C열: 시간·결과 공간 O(RC).

## 공식 예제

입력 인수: `[[[1, 2], [2, 3]], [[3, 4], [5, 6]]]`

반환값: `[[4, 6], [7, 9]]`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(arr1, arr2):
    rows = len(arr1)
    cols = len(arr1[0])
    answer = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(arr1[r][c] + arr2[r][c])
        answer.append(row)
    return answer

# 전체 코드 줄별 설명
# def solution(arr1, arr2):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def로 함수를 정의합니다. 두 행렬을 2차원 리스트로 받습니다.
#     rows = len(arr1)  # len은 길이. =는 값 저장. len()으로 행 수를 구합니다.
#     cols = len(arr1[0])  # len은 길이. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. arr1[0]은 첫 행입니다. 그 행의 원소 수가 열 수입니다.
#     answer = []  # []는 리스트. =는 값 저장. 완성된 행들을 담을 빈 리스트입니다.
#     for r in range(rows):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. r에 0부터 rows-1까지 넣습니다. r은 행 번호입니다.
#         row = []  # []는 리스트. =는 값 저장. 현재 행의 결과를 담을 새 리스트입니다. 행마다 새로 만듭니다.
#         for c in range(cols):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. c는 열 번호입니다. 현재 행의 모든 열을 확인합니다.
#             row.append(arr1[r][c] + arr2[r][c])  # append는 리스트 끝에 추가. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. [행][열]로 같은 위치의 값을 읽고 더해 현재 행에 추가합니다.
#         answer.append(row)  # append는 리스트 끝에 추가. 안쪽 반복이 끝나면 완성한 행 전체를 결과에 추가합니다.
#     return answer  # return은 결과를 돌려주고 함수 종료. 모든 행이 완성되면 결과 행렬을 반환합니다.

# 풀이 요약
# 두 행렬의 같은 행·열 위치끼리 더한다. 행 하나를 만든 뒤 바깥 결과 리스트에 넣어 원래와 같은 행렬 모양을 유지한다.
# R행 C열: 시간·결과 공간 O(RC).
```

## 확인한 범위

2026-10-16 02:50:16의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
