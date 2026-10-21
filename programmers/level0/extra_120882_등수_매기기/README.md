# 등수 매기기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120882) · Level 0 · Python3

## 풀이

자신보다 점수가 높은 학생 수+1이 등수입니다. 평균 대신 합계를 비교해도 같습니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(score):
    totals = [sum(pair) for pair in score]
    return [1 + sum(other > value for other in totals) for value in totals]

# 전체 코드 줄별 설명
# def solution(score):  # def는 함수 정의. 영어·수학 점수 쌍 리스트 입력.
#     totals = [sum(pair) for pair in score]  # 리스트 내포로 두 과목 합계 계산. 평균을 비교하는 것과 순서가 같음.
#     return [1 + sum(other > value for other in totals) for value in totals]  # 현재 합계보다 큰 학생 수를 sum으로 세고 1을 더함. 동점자는 같은 등수.

# 풀이 요약
# 자신보다 점수가 높은 학생 수+1이 등수입니다. 평균 대신 합계를 비교해도 같습니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
