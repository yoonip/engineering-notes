# 접미사 배열

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181909) · Level 0 · Python3

## 풀이

모든 시작 인덱스의 접미사를 만들어 사전순으로 정렬합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(my_string):
    return sorted(my_string[i:] for i in range(len(my_string)))

# 전체 코드 줄별 설명
# def solution(my_string):  # def는 함수 정의. 접미사를 구할 문자열 입력.
#     return sorted(my_string[i:] for i in range(len(my_string)))  # len은 길이, range는 인덱스 순회, [i:]는 i부터 끝까지. sorted는 접미사들을 사전순 정렬.

# 풀이 요약
# 모든 시작 인덱스의 접미사를 만들어 사전순으로 정렬합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
