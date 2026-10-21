# 문자열 여러 번 뒤집기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181913) · Level 0 · Python3

## 풀이

끝 인덱스를 포함하도록 end+1까지 잘라 뒤집고 원래 위치에 넣습니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(my_string, queries):
    chars = list(my_string)
    for start, end in queries:
        chars[start:end + 1] = chars[start:end + 1][::-1]
    return ''.join(chars)

# 전체 코드 줄별 설명
# def solution(my_string, queries):  # def는 함수 정의. 문자열과 뒤집을 범위 쿼리 입력.
#     chars = list(my_string)  # list는 문자열을 문자 리스트로 변환. 문자열과 달리 일부 구간 수정 가능.
#     for start, end in queries:  # 각 쿼리의 양 끝 인덱스를 나누어 받음.
#         chars[start:end + 1] = chars[start:end + 1][::-1]  # 슬라이싱은 끝 제외. [::-1]은 역순 복사. 해당 구간만 역순으로 대입.
#     return ''.join(chars)  # join으로 수정된 문자 리스트를 문자열로 연결하여 반환.

# 풀이 요약
# 끝 인덱스를 포함하도록 end+1까지 잘라 뒤집고 원래 위치에 넣습니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
