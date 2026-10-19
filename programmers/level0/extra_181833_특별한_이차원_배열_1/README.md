# 특별한 이차원 배열 1

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181833) · Level 0 · Python3

## 풀이

행 번호와 열 번호가 같은 대각선만 1로 채웁니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 정사각형 행렬의 크기 입력.
#     return [[int(i == j) for j in range(n)] for i in range(n)]  # 중첩 리스트 내포로 행·열 생성. range는 0부터 n-1, ==는 같음 비교, int는 참을 1·거짓을 0으로 변환.

# 풀이 요약
# 행 번호와 열 번호가 같은 대각선만 1로 채웁니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
