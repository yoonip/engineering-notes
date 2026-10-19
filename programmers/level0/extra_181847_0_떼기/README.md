# 0 떼기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181847) · Level 0 · Python3

## 풀이

문자열 왼쪽의 연속된 0만 제거합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(n_str):
    return n_str.lstrip('0')

# 전체 코드 줄별 설명
# def solution(n_str):  # def는 함수 정의. 앞쪽에 0이 있을 수 있는 문자열 입력.
#     return n_str.lstrip('0')  # lstrip(문자)는 왼쪽 끝에서 해당 문자가 반복되는 동안 제거. 중간·뒤의 0은 유지.

# 풀이 요약
# 문자열 왼쪽의 연속된 0만 제거합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
