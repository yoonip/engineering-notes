# 문자열 붙여서 출력하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181946) · Level 0 · Python3

## 풀이

입력 구분용 공백은 split으로 제거하고 두 문자열만 연결합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
first, second = input().split()
print(first + second)

# 전체 코드 줄별 설명
# first, second = input().split()  # input은 한 줄 입력, split은 공백 기준으로 분리. 두 문자열에 나누어 저장.
# print(first + second)  # 문자열끼리 +는 연결. 두 문자열 사이에 공백 없이 붙여 출력.

# 풀이 요약
# 입력 구분용 공백은 split으로 제거하고 두 문자열만 연결합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
