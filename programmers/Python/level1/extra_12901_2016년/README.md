# 2016년

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12901) · Level 1 · Python3

유형: 날짜 · 누적 일수

## 풀이 원리

2016년은 윤년이므로 2월은 29일입니다. 앞선 달의 일수와 b-1을 더하면 1월 1일부터 지난 날 수가 됩니다. 1월 1일이 금요일인 요일 리스트에서 나머지 7로 위치를 찾습니다.

달 수가 12로 고정되어 시간·보조 공간 O(1).

## 공식 예제

입력 인수: `[5, 24]`

반환값: `"TUE"`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(a, b):
    month_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    weekdays = ["FRI", "SAT", "SUN", "MON", "TUE", "WED", "THU"]
    elapsed = sum(month_days[:a - 1]) + b - 1
    return weekdays[elapsed % 7]

# 전체 코드 줄별 설명
# def solution(a, b):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. def로 함수를 정의합니다. a는 월, b는 일을 받는 매개변수입니다.
#     month_days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # []는 리스트. =는 값 저장. 각 달의 일수를 담은 리스트입니다. 윤년이므로 2월은 29일입니다.
#     weekdays = ["FRI", "SAT", "SUN", "MON", "TUE", "WED", "THU"]  # []는 리스트. =는 값 저장. 요일 문자열 리스트입니다. 인덱스 0을 금요일로 둡니다.
#     elapsed = sum(month_days[:a - 1]) + b - 1  # sum은 원소 합. [시작:끝]은 끝을 제외하는 슬라이스. =는 값 저장. [:a-1]로 이전 달들을 꺼내 sum()으로 더합니다. b-1은 이번 달에서 이미 지난 일수입니다.
#     return weekdays[elapsed % 7]  # return은 결과를 돌려주고 함수 종료. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. %는 나머지. %는 나머지 연산입니다. 결과 0~6을 인덱스로 사용해 요일을 반환합니다.

# 풀이 요약
# 2016년은 윤년이므로 2월은 29일이다. 앞선 달의 일수와 b-1을 더하면 1월 1일부터 지난 날 수가 된다. 1월 1일이 금요일인 요일 리스트에서 나머지 7로 위치를 찾는다.
# 달 수가 12로 고정되어 시간·보조 공간 O(1).
```

## 확인한 범위

2026-10-16 02:15:20의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
