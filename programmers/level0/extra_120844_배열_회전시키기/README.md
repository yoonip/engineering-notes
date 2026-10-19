# 배열 회전시키기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120844) · Level 0 · Python3

## 풀이

회전 방향에 따라 끝 원소를 앞으로 또는 첫 원소를 뒤로 옮깁니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(numbers, direction):
    if direction == 'right':
        return numbers[-1:] + numbers[:-1]
    return numbers[1:] + numbers[:1]

# 전체 코드 줄별 설명
# def solution(numbers, direction):  # def는 함수 정의. 정수 리스트와 회전 방향 입력.
#     if direction == 'right':  # if는 조건, ==는 문자열 같음 비교. 오른쪽 회전인지 검사.
#         return numbers[-1:] + numbers[:-1]  # [-1:]은 마지막 원소 리스트, [:-1]은 그 앞부분. +로 마지막을 맨 앞에 연결.
#     return numbers[1:] + numbers[:1]  # [1:]은 첫 원소 이후, [:1]은 첫 원소 리스트. 첫 원소를 맨 뒤에 연결.

# 풀이 요약
# 회전 방향에 따라 끝 원소를 앞으로 또는 첫 원소를 뒤로 옮깁니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
