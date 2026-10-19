# 특별한 이차원 배열 2

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181831) · Level 0 · Python3

## 풀이

주대각선을 기준으로 서로 마주 보는 두 칸의 값이 모두 같은지 검사합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(arr):
    n = len(arr)
    return int(all(arr[i][j] == arr[j][i] for i in range(n) for j in range(n)))

# 전체 코드 줄별 설명
# def solution(arr):  # def는 함수 정의. 정사각형 이차원 리스트 입력.
#     n = len(arr)  # len은 길이. 행렬 한 변의 크기 저장.
#     return int(all(arr[i][j] == arr[j][i] for i in range(n) for j in range(n)))  # all은 모든 조건이 참인지 검사. 행·열을 바꾼 값과 비교하고 int로 1·0 반환.

# 풀이 요약
# 주대각선을 기준으로 서로 마주 보는 두 칸의 값이 모두 같은지 검사합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
