# 각도기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120829) · Level 0 · Python3

## 풀이

90도와 180도의 경계값을 별도로 구분합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(angle):
    if angle < 90:
        return 1
    if angle == 90:
        return 2
    if angle < 180:
        return 3
    return 4

# 전체 코드 줄별 설명
# def solution(angle):  # def는 함수 정의. 1~180도의 각도 입력.
#     if angle < 90:  # if는 조건, <는 미만 비교. 예각 검사.
#         return 1  # 예각 번호 반환.
#     if angle == 90:  # ==는 같음 비교. 직각 검사.
#         return 2  # 직각 번호 반환.
#     if angle < 180:  # 앞 경우를 제외했으므로 90 초과 180 미만의 둔각 검사.
#         return 3  # 둔각 번호 반환.
#     return 4  # 남은 180도는 평각.

# 풀이 요약
# 90도와 180도의 경계값을 별도로 구분합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
