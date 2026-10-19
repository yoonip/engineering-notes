# 9로 나눈 나머지

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181914) · Level 0 · Python3

## 풀이

전체 숫자를 정수로 바꾸지 않고 각 자리 합을 구해 긴 입력도 처리합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(number):
    return sum(int(char) for char in number) % 9

# 전체 코드 줄별 설명
# def solution(number):  # def는 함수 정의. 아주 긴 숫자 문자열 입력.
#     return sum(int(char) for char in number) % 9  # int는 한 자리 숫자 변환, sum은 합계, %는 나머지. 자릿수 합을 9로 나눈 나머지 반환.

# 풀이 요약
# 전체 숫자를 정수로 바꾸지 않고 각 자리 합을 구해 긴 입력도 처리합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
