# 커피 심부름

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181837) · Level 0 · Python3

## 풀이

온도에 따라 가격이 바뀌지 않으며 아무거나 주문은 아메리카노 가격입니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(order):
    return sum(5000 if 'cafelatte' in item else 4500 for item in order)

# 전체 코드 줄별 설명
# def solution(order):  # def는 함수 정의. 주문 문자열 리스트 입력.
#     return sum(5000 if 'cafelatte' in item else 4500 for item in order)  # in은 문자열 포함 검사. 조건 표현식으로 라테는 5000, 나머지는 4500을 골라 sum으로 합산.

# 풀이 요약
# 온도에 따라 가격이 바뀌지 않으며 아무거나 주문은 아메리카노 가격입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
