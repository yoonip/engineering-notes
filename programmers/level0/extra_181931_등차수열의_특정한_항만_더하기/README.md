# 등차수열의 특정한 항만 더하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181931) · Level 0 · Python3

## 풀이

0부터 시작하는 인덱스 i의 항은 a+i*d입니다. 포함 여부가 참인 항만 더합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(a, d, included):
    return sum(a + i * d for i, keep in enumerate(included) if keep)

# 전체 코드 줄별 설명
# def solution(a, d, included):  # def는 함수 정의. 첫 항·공차·포함 여부 리스트 입력.
#     return sum(a + i * d for i, keep in enumerate(included) if keep)  # enumerate는 인덱스와 값 제공. if로 참인 항만 골라 a+i*d를 sum으로 합산.

# 풀이 요약
# 0부터 시작하는 인덱스 i의 항은 a+i*d입니다. 포함 여부가 참인 항만 더합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
