# 배열 자르기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120833) · Level 0 · Python3

## 풀이

인덱스 num1부터 num2까지 양 끝을 포함해 잘라냅니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(numbers, num1, num2):
    return numbers[num1:num2 + 1]

# 전체 코드 줄별 설명
# def solution(numbers, num1, num2):  # def는 함수 정의. 정수 리스트와 자를 양 끝 인덱스 입력.
#     return numbers[num1:num2 + 1]  # [시작:끝] 슬라이싱의 끝은 제외. num2를 포함하도록 1을 더함.

# 풀이 요약
# 인덱스 num1부터 num2까지 양 끝을 포함해 잘라냅니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
