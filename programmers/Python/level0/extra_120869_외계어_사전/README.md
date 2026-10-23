# 외계어 사전

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120869) · Level 0 · Python3

## 풀이

정렬한 문자 목록이 같으면 각 글자를 정확히 한 번씩 모두 사용한 단어입니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(spell, dic):
    target = sorted(spell)
    return 1 if any(sorted(word) == target for word in dic) else 2

# 전체 코드 줄별 설명
# def solution(spell, dic):  # def는 함수 정의. 사용할 문자 리스트와 단어 사전 입력.
#     target = sorted(spell)  # sorted는 정렬. 모든 문자를 한 번씩 쓴 기준 목록 생성.
#     return 1 if any(sorted(word) == target for word in dic) else 2  # any는 하나라도 참인지 검사. 각 단어의 문자와 개수가 기준과 같은지 비교.

# 풀이 요약
# 정렬한 문자 목록이 같으면 각 글자를 정확히 한 번씩 모두 사용한 단어입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
