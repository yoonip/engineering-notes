# 개미 군단

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120837) · Level 0 · Python3

## 풀이

공격력 5·3·1 순서로 큰 개미부터 배치합니다. 현재 화폐 체계에서는 이 방법으로 최소 병력을 얻습니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(hp):
    return hp // 5 + (hp % 5) // 3 + (hp % 5) % 3

# 전체 코드 줄별 설명
# def solution(hp):  # def는 함수 정의. 목표 공격력에 해당하는 체력 입력.
#     return hp // 5 + (hp % 5) // 3 + (hp % 5) % 3  # //는 몫, %는 나머지. 공격력 5를 최대한 사용하고 남은 값에 3, 마지막 나머지에 1 사용.

# 풀이 요약
# 공격력 5·3·1 순서로 큰 개미부터 배치합니다. 현재 화폐 체계에서는 이 방법으로 최소 병력을 얻습니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
