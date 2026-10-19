# 안전지대

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120866) · Level 0 · Python3

## 풀이

각 지뢰의 주변 3×3 칸을 위험 집합에 기록합니다. 지도 범위를 벗어난 좌표는 제외합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(board):
    n = len(board)
    dangerous = set()
    for row in range(n):
        for col in range(n):
            if board[row][col] == 1:
                for nr in range(max(0, row - 1), min(n, row + 2)):
                    for nc in range(max(0, col - 1), min(n, col + 2)):
                        dangerous.add((nr, nc))
    return n * n - len(dangerous)

# 전체 코드 줄별 설명
# def solution(board):  # def는 함수 정의. 0은 빈칸, 1은 지뢰인 정사각형 지도 입력.
#     n = len(board)  # len은 길이. 지도 한 변의 크기.
#     dangerous = set()  # set()은 빈 집합. 위험 좌표를 중복 없이 저장.
#     for row in range(n):  # range는 0부터 n-1까지. 모든 행 순회.
#         for col in range(n):  # 각 행의 모든 열 순회.
#             if board[row][col] == 1:  # [][]는 이차원 원소 접근, ==는 값 비교. 지뢰인지 확인.
#                 for nr in range(max(0, row - 1), min(n, row + 2)):  # max·min으로 지도 안에 있는 이웃 행 범위만 선택. range는 끝 제외.
#                     for nc in range(max(0, col - 1), min(n, col + 2)):  # 지도 안에 있는 이웃 열 범위 순회. 자기 칸도 포함.
#                         dangerous.add((nr, nc))  # ()는 좌표 튜플. add는 집합에 추가하여 겹친 위험 칸 중복 제거.
#     return n * n - len(dangerous)  # 전체 칸 수에서 서로 다른 위험 칸 수를 빼 안전 칸 수 반환.

# 풀이 요약
# 각 지뢰의 주변 3×3 칸을 위험 집합에 기록합니다. 지도 범위를 벗어난 좌표는 제외합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
