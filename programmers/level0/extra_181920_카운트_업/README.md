# 카운트 업

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181920) · Level 0 · Python3

## 풀이

시작부터 끝까지 1씩 증가하는 정수 리스트를 만듭니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(start_num, end_num):
    return list(range(start_num, end_num + 1))

# 전체 코드 줄별 설명
# def solution(start_num, end_num):  # def는 함수 정의. 시작 정수와 마지막 정수 입력.
#     return list(range(start_num, end_num + 1))  # range는 끝 제외 정수 수열, list는 리스트 변환. 마지막 수를 포함하도록 1을 더함.

# 풀이 요약
# 시작부터 끝까지 1씩 증가하는 정수 리스트를 만듭니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
