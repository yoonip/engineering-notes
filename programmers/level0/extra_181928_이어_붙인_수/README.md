# 이어 붙인 수

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181928) · Level 0 · Python3

## 풀이

홀수와 짝수를 각자 원래 순서대로 연결한 뒤 두 정수의 합을 구합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(num_list):
    odd = ''.join(str(x) for x in num_list if x % 2 == 1)
    even = ''.join(str(x) for x in num_list if x % 2 == 0)
    return int(odd) + int(even)

# 전체 코드 줄별 설명
# def solution(num_list):  # def는 함수 정의. 한 자리 정수 리스트 입력.
#     odd = ''.join(str(x) for x in num_list if x % 2 == 1)  # %는 나머지, if는 홀수 필터, str은 문자열 변환, join은 순서대로 연결.
#     even = ''.join(str(x) for x in num_list if x % 2 == 0)  # 짝수만 골라 문자열로 변환하고 연결.
#     return int(odd) + int(even)  # int로 각각 정수로 바꾼 후 숫자 덧셈.

# 풀이 요약
# 홀수와 짝수를 각자 원래 순서대로 연결한 뒤 두 정수의 합을 구합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
