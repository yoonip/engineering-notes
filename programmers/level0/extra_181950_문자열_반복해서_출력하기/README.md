# 문자열 반복해서 출력하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181950) · Level 0 · Python3

## 풀이

문자열 곱셈을 이용해 입력 문자열을 n번 이어 붙입니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
text, n = input().split()
print(text * int(n))

# 전체 코드 줄별 설명
# text, n = input().split()  # input은 문자열 입력, split은 공백 분리. 두 문자열을 text와 n에 나누어 저장.
# print(text * int(n))  # int는 정수 변환. 문자열 * 정수는 해당 횟수 반복, print는 결과 출력.

# 풀이 요약
# 문자열 곱셈을 이용해 입력 문자열을 n번 이어 붙입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
