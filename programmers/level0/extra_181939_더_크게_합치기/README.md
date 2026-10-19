# 더 크게 합치기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181939) · Level 0 · Python3

## 풀이

문자열로 바꿔 두 순서로 연결한 뒤 정수로 비교합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(a, b):
    return max(int(str(a) + str(b)), int(str(b) + str(a)))

# 전체 코드 줄별 설명
# def solution(a, b):  # def는 함수 정의. 두 양의 정수 입력.
#     return max(int(str(a) + str(b)), int(str(b) + str(a)))  # str은 문자열 변환, +는 문자열 연결, int는 정수 변환, max는 큰 값 선택.

# 풀이 요약
# 문자열로 바꿔 두 순서로 연결한 뒤 정수로 비교합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
