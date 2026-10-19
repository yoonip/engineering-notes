# 점의 위치 구하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120841) · Level 0 · Python3

## 풀이

y의 부호로 위·아래를 나눈 뒤 x의 부호로 좌·우를 구분합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(dot):
    x, y = dot
    if y > 0:
        return 1 if x > 0 else 2
    return 4 if x > 0 else 3

# 전체 코드 줄별 설명
# def solution(dot):  # def는 함수 정의. 점의 x·y 좌표 리스트 입력.
#     x, y = dot  # 두 좌표를 각각 변수에 나누어 대입.
#     if y > 0:  # if는 조건, >는 초과 비교. 위쪽 반평면인지 확인.
#         return 1 if x > 0 else 2  # 조건 표현식. 위쪽에서 x 양수는 1사분면, 음수는 2사분면.
#     return 4 if x > 0 else 3  # 아래쪽에서 x 양수는 4사분면, 음수는 3사분면.

# 풀이 요약
# y의 부호로 위·아래를 나눈 뒤 x의 부호로 좌·우를 구분합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
