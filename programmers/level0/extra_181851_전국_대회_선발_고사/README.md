# 전국 대회 선발 고사

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181851) · Level 0 · Python3

## 풀이

참석할 수 있는 학생만 고른 뒤 등수가 작은 세 명의 번호를 사용합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(rank, attendance):
    candidates = [i for i, available in enumerate(attendance) if available]
    a, b, c = sorted(candidates, key=lambda i: rank[i])[:3]
    return 10000 * a + 100 * b + c

# 전체 코드 줄별 설명
# def solution(rank, attendance):  # def는 함수 정의. 학생별 등수와 참석 여부 입력.
#     candidates = [i for i, available in enumerate(attendance) if available]  # enumerate는 학생 번호와 참석 여부 제공. 리스트 내포로 참석 가능한 학생 번호만 선택.
#     a, b, c = sorted(candidates, key=lambda i: rank[i])[:3]  # sorted는 정렬, lambda는 이름 없는 함수. 등수가 작은 순으로 정렬해 세 학생 번호를 분해 대입.
#     return 10000 * a + 100 * b + c  # *는 곱셈, +는 덧셈. 문제에서 지정한 식으로 학생 번호 결합.

# 풀이 요약
# 참석할 수 있는 학생만 고른 뒤 등수가 작은 세 명의 번호를 사용합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
