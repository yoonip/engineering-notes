# K번째수

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/42748) · Level 1 · Python3

유형: 배열 · 구간 복사 · 정렬

## 풀이 원리

질의의 시작·끝 위치로 구간을 복사하고 정렬한 뒤 k번째를 읽습니다. 문제의 위치는 1부터 시작하므로 배열 접근은 1을 뺍니다. 끝 위치를 포함하려면 range의 끝값은 문제의 end 그대로 둡니다.

질의 구간 길이 L_i: 시간 O(Σ L_i log(L_i+1)), 보조 공간 O(max L_i). 결과 리스트는 질의 수만큼 필요합니다.

## 공식 예제

입력 인수: `[[1, 5, 2, 6, 3, 7, 4], [[2, 5, 3], [4, 4, 1], [1, 7, 3]]]`

반환값: `[5, 6, 3]`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(array, commands):
    answer = []
    for command in commands:
        start = command[0]
        end = command[1]
        k = command[2]
        numbers = []
        for index in range(start - 1, end):
            numbers.append(array[index])
        numbers.sort()
        number = numbers[k - 1]
        answer.append(number)
    return answer

# 전체 코드 줄별 설명
# def solution(array, commands):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. array: 원본 숫자 배열, commands: [i, j, k] 명령들의 목록
#     answer = []  # []는 리스트. =는 값 저장. 각 명령에서 구한 K번째 숫자를 저장할 빈 리스트
#     for command in commands:  # for·in은 원소를 차례로 꺼내는 반복문. 각 구간 질의의 시작·끝·선택 순위를 처리.
#         start = command[0]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 질의의 시작 위치를 읽음.
#         end = command[1]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 질의의 마지막 위치를 읽음.
#         k = command[2]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 정렬한 구간에서 고를 순위.
#         numbers = []  # []는 리스트. =는 값 저장. 이번 구간의 값을 모을 리스트.
#         for index in range(start - 1, end):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. 문제의 1부터 시작하는 구간을 배열 인덱스로 변환.
#             numbers.append(array[index])  # append는 리스트 끝에 추가. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. 해당 구간 원소를 복사.
#         numbers.sort()  # sort는 원래 리스트 정렬. 잘라낸 숫자들을 오름차순(작은 숫자부터 큰 숫자 순서)으로 정렬
#         number = numbers[k - 1]  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. 정렬한 배열에서 k번째 값을 선택.
#         answer.append(number)  # append는 리스트 끝에 추가. 이 질의의 결과를 추가.
#     return answer  # return은 결과를 돌려주고 함수 종료. 모든 명령의 결과를 순서대로 반환

# 풀이 요약
# 질의의 시작·끝 위치로 구간을 복사하고 정렬한 뒤 k번째를 읽는다. 문제의 위치는 1부터 시작하므로 배열 접근은 1을 뺀다. 끝 위치를 포함하려면 range의 끝값은 문제의 end 그대로 둔다.
# 질의 구간 길이 L_i: 시간 O(Σ L_i log(L_i+1)), 보조 공간 O(max L_i). 결과 리스트는 질의 수만큼 필요하다.
```

## 확인한 범위

2026-10-16 15:05:50의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
