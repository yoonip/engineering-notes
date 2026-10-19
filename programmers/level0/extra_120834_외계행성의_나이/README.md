# 외계행성의 나이

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120834) · Level 0 · Python3

## 풀이

숫자 0~9를 a~j로 대응시켜 각 자릿수를 바꿉니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(age):
    return ''.join(chr(ord('a') + int(char)) for char in str(age))

# 전체 코드 줄별 설명
# def solution(age):  # def는 함수 정의. 숫자로 표현된 나이 입력.
#     return ''.join(chr(ord('a') + int(char)) for char in str(age))  # str은 숫자 문자열 변환, int는 각 자릿수 변환, ord는 문자 코드, chr은 코드에서 문자 변환, join은 연결.

# 풀이 요약
# 숫자 0~9를 a~j로 대응시켜 각 자릿수를 바꿉니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
