# 배열의 평균값

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120817) · Level 0 · Python3

## 풀이

평균은 전체 합을 원소 개수로 나눈 값입니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(numbers):
    return sum(numbers) / len(numbers)

# 전체 코드 줄별 설명
# def solution(numbers):  # def는 함수 정의. 평균을 구할 정수 리스트 입력.
#     return sum(numbers) / len(numbers)  # sum은 합계, len은 개수, /는 실수 나눗셈. 합계를 개수로 나눔.

# 풀이 요약
# 평균은 전체 합을 원소 개수로 나눈 값입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
