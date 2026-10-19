# 배열 두 배 만들기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120809) · Level 0 · Python3

## 풀이

원소 순서를 유지하며 각 값을 두 배로 바꿉니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(numbers):
    return [value * 2 for value in numbers]

# 전체 코드 줄별 설명
# def solution(numbers):  # def는 함수 정의. 정수 리스트 입력.
#     return [value * 2 for value in numbers]  # [] 안의 for는 리스트 내포. 각 원소에 2를 곱해 새 리스트 생성.

# 풀이 요약
# 원소 순서를 유지하며 각 값을 두 배로 바꿉니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
