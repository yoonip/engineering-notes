# 문자열 겹쳐쓰기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181943) · Level 0 · Python3

## 풀이

교체 범위 바깥의 앞뒤 부분은 슬라이싱으로 보존하고 가운데를 새 문자열로 바꿉니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(my_string, overwrite_string, s):
    return my_string[:s] + overwrite_string + my_string[s + len(overwrite_string):]

# 전체 코드 줄별 설명
# def solution(my_string, overwrite_string, s):  # def는 함수 정의. 원본·덮을 문자열·시작 인덱스를 입력받음.
#     return my_string[:s] + overwrite_string + my_string[s + len(overwrite_string):]  # [:s]는 시작 전 부분, len은 길이, [끝:]는 덮는 구간 뒤의 부분. +로 앞·대체·뒤를 연결.

# 풀이 요약
# 교체 범위 바깥의 앞뒤 부분은 슬라이싱으로 보존하고 가운데를 새 문자열로 바꿉니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
