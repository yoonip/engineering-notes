# 평행

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120875) · Level 0 · Python3

## 풀이

기울기의 분자·분모를 교차 곱해 비교하고 네 점을 두 쌍으로 나누는 모든 경우를 검사합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(dots):
    for i, j, k, l in ((0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 1, 2)):
        a, b, c, d = dots[i], dots[j], dots[k], dots[l]
        if (b[1] - a[1]) * (d[0] - c[0]) == (d[1] - c[1]) * (b[0] - a[0]):
            return 1
    return 0

# 전체 코드 줄별 설명
# def solution(dots):  # def는 함수 정의. 네 점의 좌표 리스트 입력.
#     for i, j, k, l in ((0, 1, 2, 3), (0, 2, 1, 3), (0, 3, 1, 2)):  # 네 점을 서로 다른 두 쌍으로 나누는 세 가지 경우를 튜플로 순회.
#         a, b, c, d = dots[i], dots[j], dots[k], dots[l]  # []는 인덱스 접근. 현재 두 선분의 네 끝점 조회.
#         if (b[1] - a[1]) * (d[0] - c[0]) == (d[1] - c[1]) * (b[0] - a[0]):  # if는 조건. 기울기 분수를 나누지 않고 교차 곱으로 비교해 실수 오차 방지.
#             return 1  # 평행한 두 직선이 하나라도 있으면 1 반환.
#     return 0  # 세 경우 모두 평행하지 않으면 0 반환.

# 풀이 요약
# 기울기의 분자·분모를 교차 곱해 비교하고 네 점을 두 쌍으로 나누는 모든 경우를 검사합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
