# 문자 리스트를 문자열로 변환하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181941) · Level 0 · Python3

## 풀이

빈 문자열을 구분자로 사용하면 문자 리스트가 하나의 문자열이 됩니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(arr):
    return ''.join(arr)

# 전체 코드 줄별 설명
# def solution(arr):  # def는 함수 정의. arr은 한 글자 문자열들의 리스트.
#     return ''.join(arr)  # join은 문자열들을 구분자 없이 연결. return으로 연결 결과 반환.

# 풀이 요약
# 빈 문자열을 구분자로 사용하면 문자 리스트가 하나의 문자열이 됩니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
