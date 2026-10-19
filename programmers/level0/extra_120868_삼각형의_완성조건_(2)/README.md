# 삼각형의 완성조건 (2)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120868) · Level 0 · Python3

## 풀이

삼각형 부등식을 합치면 세 번째 변은 두 변의 차보다 크고 합보다 작아야 합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(sides):
    return 2 * min(sides) - 1

# 전체 코드 줄별 설명
# def solution(sides):  # def는 함수 정의. 삼각형의 두 변 길이 입력.
#     return 2 * min(sides) - 1  # min은 작은 변 길이. |a-b|<세 번째 변<a+b 사이 정수 개수는 2*작은 변-1.

# 풀이 요약
# 삼각형 부등식을 합치면 세 번째 변은 두 변의 차보다 크고 합보다 작아야 합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
