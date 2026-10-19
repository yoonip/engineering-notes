# 같은 숫자는 싫어

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12906) · Level 1 · Python3

유형: 배열 · 연속 중복 제거

## 풀이 원리

현재 수와 직전 수가 다를 때만 결과에 넣습니다. 값이 예전에 나왔더라도 바로 앞과 다르면 다시 넣어야 하므로 집합으로 전체 중복을 지우면 안 됩니다. 초기 이전 값 -1은 입력 범위 0~9에 없어서 첫 원소가 항상 들어갑니다.

원소 N개: 시간 O(N), 결과 공간 O(N).

## 공식 예제

입력 인수: `[[1, 1, 3, 3, 0, 1, 1]]`

반환값: `[1, 3, 0, 1]`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(arr):
    answer = []
    previous = -1
    for number in arr:
        if number != previous:
            answer.append(number)
        previous = number
    return answer

# 전체 코드 줄별 설명
# def solution(arr):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 연속 중복을 줄일 배열을 입력받음.
#     answer = []  # []는 리스트. =는 값 저장. 결과 리스트 초기화.
#     previous = -1  # =는 값 저장. 입력 범위 0~9와 다른 값으로 이전 수 초기화.
#     for number in arr:  # for·in은 원소를 차례로 꺼내는 반복문. 원래 순서대로 숫자를 확인.
#         if number != previous:  # if는 조건이 참일 때 실행. !=는 다름 비교. 직전 숫자와 달라 새 구간이 시작되는지 검사.
#             answer.append(number)  # append는 리스트 끝에 추가. 처음 나온 연속 구간의 숫자만 추가.
#         previous = number  # =는 값 저장. 다음 비교에 사용할 직전 숫자 갱신.
#     return answer  # return은 결과를 돌려주고 함수 종료. 연속 중복을 제거한 배열 반환.

# 풀이 요약
# 현재 수와 직전 수가 다를 때만 결과에 넣는다. 값이 예전에 나왔더라도 바로 앞과 다르면 다시 넣어야 하므로 집합으로 전체 중복을 지우면 안 된다. 초기 이전 값 -1은 입력 범위 0~9에 없어서 첫 원소가 항상 들어간다.
# 원소 N개: 시간 O(N), 결과 공간 O(N).
```

## 확인한 범위

2026-10-17 10:03:04의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
