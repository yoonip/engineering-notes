# [PCCE 기출문제] 2번 / 피타고라스의 정리

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/250132) · Level 0 · Python3

## 풀이

a²+b²=c²이므로 b²=c²-a²입니다. 제곱 계산 한 줄만 수정합니다.

## 코드와 줄별 설명

빈칸 채우기·한 줄 수정 형식이라 사이트에는 지정된 부분만 제출했습니다. 아래 전체 주석본은 학습용으로 보관합니다.

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
a = int(input())
c = int(input())
b_square = c ** 2 - a ** 2
print(b_square)

# 전체 코드 줄별 설명
# a = int(input())  # input은 한 줄 입력, int는 정수 변환. 직각변 길이 저장.
# c = int(input())  # 빗변 길이를 입력받아 정수로 저장.
# b_square = c ** 2 - a ** 2  # **는 거듭제곱. 피타고라스 정리에서 다른 변 제곱은 빗변 제곱 빼기 주어진 변 제곱.
# print(b_square)  # print는 결과를 화면에 출력.

# 풀이 요약
# a²+b²=c²이므로 b²=c²-a²입니다. 제곱 계산 한 줄만 수정합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
