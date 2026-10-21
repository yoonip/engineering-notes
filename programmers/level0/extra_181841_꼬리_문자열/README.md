# 꼬리 문자열

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181841) · Level 0 · Python3

## 풀이

제외 문구가 없는 문자열만 원래 순서대로 이어 붙입니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(str_list, ex):
    return ''.join(text for text in str_list if ex not in text)

# 전체 코드 줄별 설명
# def solution(str_list, ex):  # def는 함수 정의. 문자열 리스트와 제외할 부분 문자열 입력.
#     return ''.join(text for text in str_list if ex not in text)  # not in은 부분 문자열 없음 검사. 생성기 표현식에서 조건에 맞는 문자열만 골라 join으로 연결.

# 풀이 요약
# 제외 문구가 없는 문자열만 원래 순서대로 이어 붙입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
