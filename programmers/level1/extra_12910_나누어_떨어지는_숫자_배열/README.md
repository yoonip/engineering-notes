# 나누어 떨어지는 숫자 배열

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12910) · Level 1 · Python3

유형: 배열 · 필터 · 정렬

## 풀이 원리

각 수를 divisor로 나눈 나머지가 0일 때만 남긴다. 남은 값이 없으면 [-1]을 반환하고, 있으면 오름차순 정렬한다. 입력 순서를 그대로 반환하면 정렬 조건을 놓친다.

원소 N개, 남긴 K개: 시간 O(N+K log K), 공간 O(K).

## 공식 예제

입력 인수: `[[5, 9, 7, 10], 5]`

반환값: `[5, 10]`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있다.

## 코드와 줄별 설명

원본에는 `solution`이 2번 정의돼 있다. Python은 나중에 나온 같은 이름의 정의를 사용하므로 마지막 함수가 실제로 호출된다. 위 실행 부분도 원본의 정의 순서를 유지했다.

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(arr, divisor):
    answer = []
    for number in arr:
        if number % divisor == 0:
            answer.append(number)
    if len(answer) == 0:
        return [-1]
    answer.sort()
    return answer

def solution(arr, divisor):
    answer = []
    for number in arr:
        if number % divisor ==0:
            answer.append(number)
    if len(answer) ==0:
        return [-1]
    answer.sort()
    return answer

# 전체 코드 줄별 설명
# def solution(arr, divisor):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 숫자 배열 arr와 나눌 수 divisor를 입력받습니다.
#     answer = []  # []는 리스트. =는 값 저장. 조건에 맞는 숫자를 담을 빈 리스트를 만듭니다.
#     for number in arr:  # for·in은 원소를 차례로 꺼내는 반복문. 배열의 각 수를 확인.
#         if number % divisor == 0:  # if는 조건이 참일 때 실행. ==는 같음 비교. %는 나머지. 지정한 수로 나누어떨어지는지 확인.
#             answer.append(number)  # append는 리스트 끝에 추가. 나누어떨어지는 수를 결과에 저장.
#     if len(answer) == 0:  # if는 조건이 참일 때 실행. len은 길이. ==는 같음 비교. 조건을 만족한 수가 없는지 확인.
#         return [-1]  # return은 결과를 돌려주고 함수 종료. []는 리스트. 정수가 아닌, -1을 담은 리스트를 반환합니다.
#     answer.sort()  # sort는 원래 리스트 정렬. 남긴 수들을 오름차순 정렬.
#     return answer  # return은 결과를 돌려주고 함수 종료. 정렬한 결과 리스트 반환.
# 
# def solution(arr, divisor):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 숫자 배열 arr와 나눌 수 divisor를 입력받습니다.
#     answer = []  # []는 리스트. =는 값 저장. 조건에 맞는 숫자를 담을 빈 리스트를 만듭니다.
#     for number in arr:  # for·in은 원소를 차례로 꺼내는 반복문. 배열 원소를 하나씩 확인.
#         if number % divisor ==0:  # if는 조건이 참일 때 실행. ==는 같음 비교. %는 나머지. 나눗셈의 나머지가 0인지 확인.
#             answer.append(number)  # append는 리스트 끝에 추가. 조건을 만족한 수를 추가.
#     if len(answer) ==0:  # if는 조건이 참일 때 실행. len은 길이. ==는 같음 비교. 남은 수가 없는지 확인.
#         return [-1]  # return은 결과를 돌려주고 함수 종료. []는 리스트. 정수가 아닌, -1을 담은 리스트를 반환합니다.
#     answer.sort()  # sort는 원래 리스트 정렬. 결과를 작은 수부터 정렬.
#     return answer  # return은 결과를 돌려주고 함수 종료. 최종 결과 반환.

# 풀이 요약
# 각 수를 divisor로 나눈 나머지가 0일 때만 남긴다. 남은 값이 없으면 [-1]을 반환하고, 있으면 오름차순 정렬한다. 입력 순서를 그대로 반환하면 정렬 조건을 놓친다.
# 원소 N개, 남긴 K개: 시간 O(N+K log K), 공간 O(K).
```

## 확인한 범위

2026-10-17 10:42:58의 Python3 제출 내역에서 정답 100/100을 확인했다. 원본은 그대로 보관했다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
