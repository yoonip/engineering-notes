# 세로 읽기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181904) · Level 0 · Python3

## 풀이

같은 열의 글자는 문자열에서 m칸 간격으로 나타납니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(my_string, m, c):
    return my_string[c - 1::m]

# 전체 코드 줄별 설명
# def solution(my_string, m, c):  # def는 함수 정의. 문자열·한 줄 글자 수·열 번호 입력.
#     return my_string[c - 1::m]  # [시작:끝:간격]은 슬라이싱. 1부터 시작하는 열 c를 인덱스 c-1로 바꾸고 m칸 간격으로 추출.

# 풀이 요약
# 같은 열의 글자는 문자열에서 m칸 간격으로 나타납니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
