# 짝수 홀수 개수

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120824) · Level 0 · Python3

## 풀이

짝수 개수를 먼저 세고 나머지를 홀수 개수로 계산합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(num_list):
    even = sum(value % 2 == 0 for value in num_list)
    return [even, len(num_list) - even]

# 전체 코드 줄별 설명
# def solution(num_list):  # def는 함수 정의. 정수 리스트 입력.
#     even = sum(value % 2 == 0 for value in num_list)  # %는 나머지, ==는 같음 비교. sum은 짝수 조건의 참을 1로 합산.
#     return [even, len(num_list) - even]  # []는 리스트. len은 전체 개수. 전체에서 짝수 개수를 빼 홀수 개수 계산.

# 풀이 요약
# 짝수 개수를 먼저 세고 나머지를 홀수 개수로 계산합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
