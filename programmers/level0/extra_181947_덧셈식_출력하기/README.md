# 덧셈식 출력하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181947) · Level 0 · Python3

## 풀이

덧셈은 실제로 계산하고, 식의 기호와 공백은 문자열로 출력합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
a, b = map(int, input().split())
print(f"{a} + {b} = {a + b}")

# 전체 코드 줄별 설명
# a, b = map(int, input().split())  # input은 입력, split은 공백 분리, map(int, ...)는 각 항목 정수 변환. 두 변수에 나누어 저장.
# print(f"{a} + {b} = {a + b}")  # f 문자열의 {}에는 변수나 계산식 삽입. print로 숫자·연산 기호·합계 출력.

# 풀이 요약
# 덧셈은 실제로 계산하고, 식의 기호와 공백은 문자열로 출력합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
