# 특이한 정렬

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120880) · Level 0 · Python3

## 풀이

정렬 기준을 (거리,음수 값)으로 지정해 동률일 때 큰 수를 앞에 둡니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(numlist, n):
    return sorted(numlist, key=lambda x: (abs(x - n), -x))

# 전체 코드 줄별 설명
# def solution(numlist, n):  # def는 함수 정의. 후보 정수 리스트와 기준값 입력.
#     return sorted(numlist, key=lambda x: (abs(x - n), -x))  # sorted는 정렬, lambda는 익명 기준 함수, abs는 절댓값. 거리 우선, 동률이면 -x를 사용해 큰 수 우선.

# 풀이 요약
# 정렬 기준을 (거리,음수 값)으로 지정해 동률일 때 큰 수를 앞에 둡니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
