# qr code

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181903) · Level 0 · Python3

## 풀이

조건을 만족하는 인덱스 r, r+q, r+2q 위치를 슬라이싱으로 한 번에 가져옵니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(q, r, code):
    return code[r::q]

# 전체 코드 줄별 설명
# def solution(q, r, code):  # def는 함수 정의. 나눌 수·나머지·문자열 입력.
#     return code[r::q]  # [시작::간격] 슬라이싱. r부터 q칸 간격인 인덱스는 q로 나눈 나머지가 모두 r.

# 풀이 요약
# 조건을 만족하는 인덱스 r, r+q, r+2q 위치를 슬라이싱으로 한 번에 가져옵니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
