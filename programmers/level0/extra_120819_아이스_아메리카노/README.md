# 아이스 아메리카노

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120819) · Level 0 · Python3

## 풀이

가격 5500원으로 나눈 몫과 나머지를 사용합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(money):
    return [money // 5500, money % 5500]

# 전체 코드 줄별 설명
# def solution(money):  # def는 함수 정의. 가진 돈 입력.
#     return [money // 5500, money % 5500]  # //는 정수 나눗셈의 몫, %는 나머지. 살 수 있는 잔 수와 남은 돈을 리스트로 반환.

# 풀이 요약
# 가격 5500원으로 나눈 몫과 나머지를 사용합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
