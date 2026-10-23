# [1차] 비밀지도

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/17681) · Level 1 · Python3

유형: 비트 연산 · 문자열

## 풀이 원리

두 지도의 각 행은 비트로 벽 위치를 나타냅니다. OR 연산은 어느 지도에든 벽이 있으면 1을 남깁니다. 이진수의 0b 접두사를 제거하고 n자리로 채운 뒤 1은 벽, 0은 공백으로 바꿉니다.

한 변 N: 출력 문자 수 기준 시간·공간 O(N²).

## 공식 예제

입력 인수: `[5, [9, 20, 28, 18, 11], [30, 1, 21, 17, 28]]`

반환값: `["#####", "# # #", "### #", "#  ##", "#####"]`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(n, arr1, arr2):
    answer = []
    for a, b in zip(arr1, arr2):
        combined = a | b
        binary = bin(combined)[2:].zfill(n)
        row = binary.replace("1", "#").replace("0", " ")
        answer.append(row)
    return answer

# 전체 코드 줄별 설명
# def solution(n, arr1, arr2):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 지도 크기 n과 두 개의 지도 배열을 입력받음
#     answer = []  # []는 리스트. =는 값 저장. 완성된 지도의 각 행을 저장할 빈 리스트
#     for a, b in zip(arr1, arr2):  # for·in은 원소를 차례로 꺼내는 반복문. zip은 같은 위치의 값들을 짝지음. ()로 묶은 여러 값은 변경 불가 튜플. 두 지도에서 같은 위치의 숫자 a, b를 하나씩 가져옴
#         combined = a | b  # |는 비트 OR. =는 값 저장. 비트 OR 연산으로 두 지도를 합침 (하나라도 1이면 1)
#         binary = bin(combined)[2:].zfill(n)  # bin은 0b 접두사가 있는 이진수 문자열. zfill은 지정한 자릿수까지 앞을 0으로 채움. [시작:끝]은 끝을 제외하는 슬라이스. =는 값 저장. 2진수로 변환하고 0b 제거 후 앞에 0을 채워 길이를 n으로 맞춤
#         row = binary.replace("1", "#").replace("0", " ")  # replace는 문자열 치환. =는 값 저장. 숫자 1은 벽(#), 0은 공백으로 변환
#         answer.append(row)  # append는 리스트 끝에 추가. 변환한 한 행을 정답 리스트에 추가
#     return answer  # return은 결과를 돌려주고 함수 종료. 완성된 지도를 문자열 리스트로 반환

# 풀이 요약
# 두 지도의 각 행은 비트로 벽 위치를 나타낸다. OR 연산은 어느 지도에든 벽이 있으면 1을 남긴다. 이진수의 0b 접두사를 제거하고 n자리로 채운 뒤 1은 벽, 0은 공백으로 바꾼다.
# 한 변 N: 출력 문자 수 기준 시간·공간 O(N²).
```

## 확인한 범위

2026-10-16 02:34:16의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
