# 직각삼각형 출력하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120823) · Level 0 · Python3

## 풀이

첫 행부터 별을 1개,2개 순서로 늘려 n개까지 출력합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
n = int(input())
for width in range(1, n + 1):
    print('*' * width)

# 전체 코드 줄별 설명
# n = int(input())  # input은 한 줄 입력, int는 정수 변환. 삼각형 높이 저장.
# for width in range(1, n + 1):  # for는 반복, range는 1부터 n까지 순회. 각 행의 별 개수를 증가시킴.
#     print('*' * width)  # 문자열 * 정수는 반복. print는 별을 출력하고 줄바꿈.

# 풀이 요약
# 첫 행부터 별을 1개,2개 순서로 늘려 n개까지 출력합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
