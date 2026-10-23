# 정수 찾기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181840) · Level 0 · Python3

## 풀이

멤버십 연산 in으로 정수의 존재 여부를 확인합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(num_list, n):
    return int(n in num_list)

# 전체 코드 줄별 설명
# def solution(num_list, n):  # def는 함수 정의. 정수 리스트와 찾을 수 입력.
#     return int(n in num_list)  # in은 리스트에 값이 있는지 검사. int는 참을 1·거짓을 0으로 변환.

# 풀이 요약
# 멤버십 연산 in으로 정수의 존재 여부를 확인합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
