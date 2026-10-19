# 문자 반복 출력하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120825) · Level 0 · Python3

## 풀이

문자열 전체가 아닌 각 글자를 n번씩 반복합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(my_string, n):
    return ''.join(char * n for char in my_string)

# 전체 코드 줄별 설명
# def solution(my_string, n):  # def는 함수 정의. 문자열과 각 문자 반복 횟수 입력.
#     return ''.join(char * n for char in my_string)  # 문자 * 정수는 문자 반복. 생성기 표현식으로 각 글자를 반복하고 join으로 연결.

# 풀이 요약
# 문자열 전체가 아닌 각 글자를 n번씩 반복합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
