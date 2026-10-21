# 문자열 묶기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181855) · Level 0 · Python3

## 풀이

문자열의 내용이 아닌 길이를 기준으로 개수를 세고 최댓값을 구합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(strArr):
    counts = [0] * 31
    for text in strArr:
        counts[len(text)] += 1
    return max(counts)

# 전체 코드 줄별 설명
# def solution(strArr):  # def는 함수 정의. 문자열 리스트 입력.
#     counts = [0] * 31  # []는 리스트, *는 반복. 길이 1~30의 출현 횟수 저장 공간 초기화.
#     for text in strArr:  # for로 각 문자열 순회.
#         counts[len(text)] += 1  # len은 길이, []는 인덱스 접근. 해당 길이 그룹의 문자열 수 증가.
#     return max(counts)  # max는 최댓값. 가장 큰 그룹의 크기 반환.

# 풀이 요약
# 문자열의 내용이 아닌 길이를 기준으로 개수를 세고 최댓값을 구합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
