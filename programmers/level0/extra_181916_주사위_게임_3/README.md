# 주사위 게임 3

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181916) · Level 0 · Python3

## 풀이

출현 횟수가 많은 눈부터 정렬하면 네 개 같음·세 개 같음·두 쌍·한 쌍·모두 다름을 구분할 수 있습니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
from collections import Counter

def solution(a, b, c, d):
    counts = Counter((a, b, c, d))
    values = sorted(counts, key=counts.get, reverse=True)
    p = values[0]
    if counts[p] == 4:
        return 1111 * p
    if counts[p] == 3:
        return (10 * p + values[1]) ** 2
    if counts[p] == 2:
        if len(values) == 2:
            q = values[1]
            return (p + q) * abs(p - q)
        return values[1] * values[2]
    return min(values)

# 전체 코드 줄별 설명
# from collections import Counter  # from 모듈 import 이름은 도구 가져오기. Counter는 원소별 출현 횟수를 세는 딕셔너리형 자료구조.
# 
# def solution(a, b, c, d):  # def는 함수 정의. 네 주사위 눈 입력.
#     counts = Counter((a, b, c, d))  # ()는 튜플. Counter에 네 눈을 넣어 같은 눈의 개수 집계.
#     values = sorted(counts, key=counts.get, reverse=True)  # sorted는 정렬. key는 기준 함수, get은 횟수 조회, reverse=True는 횟수 내림차순.
#     p = values[0]  # []는 인덱스 접근. 가장 자주 나온 눈 선택.
#     if counts[p] == 4:  # if는 조건, ==는 같음 비교. 네 눈이 모두 같은지 확인.
#         return 1111 * p  # 네 개가 같은 경우 점수 반환.
#     if counts[p] == 3:  # 세 개가 같은 경우 검사.
#         return (10 * p + values[1]) ** 2  # 나머지 눈을 q로 사용. **는 제곱.
#     if counts[p] == 2:  # 같은 눈이 두 개 있는 경우.
#         if len(values) == 2:  # len은 길이. 서로 다른 눈이 두 종류면 두 쌍.
#             q = values[1]  # 다른 쌍의 눈 조회.
#             return (p + q) * abs(p - q)  # abs는 절댓값. 두 쌍에 해당하는 점수 계산.
#         return values[1] * values[2]  # 한 쌍만 있으면 나머지 서로 다른 두 눈의 곱 반환.
#     return min(values)  # min은 최솟값. 네 눈이 다르면 가장 작은 눈 반환.

# 풀이 요약
# 출현 횟수가 많은 눈부터 정렬하면 네 개 같음·세 개 같음·두 쌍·한 쌍·모두 다름을 구분할 수 있습니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
