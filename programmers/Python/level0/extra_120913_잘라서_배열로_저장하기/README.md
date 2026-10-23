# 잘라서 배열로 저장하기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120913) · Level 0 · Python3

## 풀이

시작 위치를 n칸씩 옮기며 길이 n의 부분 문자열을 자릅니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(my_str, n):
    return [my_str[i:i + n] for i in range(0, len(my_str), n)]

# 전체 코드 줄별 설명
# def solution(my_str, n):  # def는 함수 정의. 문자열과 조각 길이 입력.
#     return [my_str[i:i + n] for i in range(0, len(my_str), n)]  # range의 간격 n으로 시작 위치 순회. 슬라이싱으로 n글자씩 추출하는 리스트 내포. 마지막 짧은 조각도 유지.

# 풀이 요약
# 시작 위치를 n칸씩 옮기며 길이 n의 부분 문자열을 자릅니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
