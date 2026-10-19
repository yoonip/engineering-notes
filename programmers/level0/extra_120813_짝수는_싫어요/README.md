# 짝수는 싫어요

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120813) · Level 0 · Python3

## 풀이

1부터 두 칸 간격으로 증가하면 홀수만 선택됩니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(n):
    return list(range(1, n + 1, 2))

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 홀수 리스트의 상한 입력.
#     return list(range(1, n + 1, 2))  # range는 1부터 n까지 간격 2의 정수 생성. list는 리스트 변환.

# 풀이 요약
# 1부터 두 칸 간격으로 증가하면 홀수만 선택됩니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
