# 주사위의 개수

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120845) · Level 0 · Python3

## 풀이

각 방향에 몇 개씩 들어가는지 따로 구해 곱합니다. 전체 부피만 나누면 남는 틈을 잘못 계산할 수 있습니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(box, n):
    return (box[0] // n) * (box[1] // n) * (box[2] // n)

# 전체 코드 줄별 설명
# def solution(box, n):  # def는 함수 정의. 상자의 가로·세로·높이와 주사위 한 변 입력.
#     return (box[0] // n) * (box[1] // n) * (box[2] // n)  # []는 인덱스 접근, //는 정수 나눗셈. 각 축에 들어가는 개수를 곱함.

# 풀이 요약
# 각 방향에 몇 개씩 들어가는지 따로 구해 곱합니다. 전체 부피만 나누면 남는 틈을 잘못 계산할 수 있습니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
