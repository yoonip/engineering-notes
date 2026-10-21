# 무작위로 K개의 수 뽑기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181858) · Level 0 · Python3

## 풀이

처음 등장한 서로 다른 수를 k개까지 남기고 부족한 자리는 -1로 채웁니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(arr, k):
    unique = list(dict.fromkeys(arr))[:k]
    return unique + [-1] * (k - len(unique))

# 전체 코드 줄별 설명
# def solution(arr, k):  # def는 함수 정의. 숫자 리스트와 목표 길이 입력.
#     unique = list(dict.fromkeys(arr))[:k]  # dict.fromkeys는 각 값을 키로 하는 딕셔너리 생성. 중복을 제거하며 처음 등장 순서 유지. list로 변환 후 앞 k개 선택.
#     return unique + [-1] * (k - len(unique))  # len은 길이, 리스트 * 횟수는 반복, +는 연결. 부족한 개수만큼 -1 추가.

# 풀이 요약
# 처음 등장한 서로 다른 수를 k개까지 남기고 부족한 자리는 -1로 채웁니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
