# 배열 만들기 1

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181901) · Level 0 · Python3

## 풀이

양의 k의 배수는 k, 2k, 3k 순서입니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(n, k):
    return list(range(k, n + 1, k))

# 전체 코드 줄별 설명
# def solution(n, k):  # def는 함수 정의. 상한과 배수 기준 입력.
#     return list(range(k, n + 1, k))  # range(시작,끝,간격)는 끝 제외 정수 수열. k부터 k씩 증가한 수를 list로 변환.

# 풀이 요약
# 양의 k의 배수는 k, 2k, 3k 순서입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
