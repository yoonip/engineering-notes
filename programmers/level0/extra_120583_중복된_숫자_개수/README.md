# 중복된 숫자 개수

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120583) · Level 0 · Python3

## 풀이

리스트 메서드 count로 중복을 포함한 출현 횟수를 셉니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(array, n):
    return array.count(n)

# 전체 코드 줄별 설명
# def solution(array, n):  # def는 함수 정의. 정수 리스트와 셀 정수 입력.
#     return array.count(n)  # count(값)는 리스트에서 해당 값이 나온 횟수 반환.

# 풀이 요약
# 리스트 메서드 count로 중복을 포함한 출현 횟수를 셉니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
