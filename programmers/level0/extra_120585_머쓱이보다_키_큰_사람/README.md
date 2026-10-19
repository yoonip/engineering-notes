# 머쓱이보다 키 큰 사람

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120585) · Level 0 · Python3

## 풀이

같은 키는 제외하고 기준 키보다 큰 사람만 셉니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(array, height):
    return sum(value > height for value in array)

# 전체 코드 줄별 설명
# def solution(array, height):  # def는 함수 정의. 친구들 키 리스트와 기준 키 입력.
#     return sum(value > height for value in array)  # >는 초과 비교. 생성기 표현식으로 더 큰 키인지 검사하고 sum으로 참의 개수 합산.

# 풀이 요약
# 같은 키는 제외하고 기준 키보다 큰 사람만 셉니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
