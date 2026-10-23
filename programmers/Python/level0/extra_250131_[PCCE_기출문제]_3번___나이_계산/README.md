# [PCCE 기출문제] 3번 / 나이 계산

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/250131) · Level 0 · Python3

## 풀이

한국식 나이는 연도 차이+1, 연 나이는 연도 차이입니다. 기준 연도는 문제에서 정한 2030입니다.

## 코드와 줄별 설명

빈칸 채우기·한 줄 수정 형식이라 사이트에는 지정된 부분만 제출했습니다. 아래 전체 주석본은 학습용으로 보관합니다.

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
year = int(input())
age_type = input()
if age_type == "Korea":
    answer = 2030 - year + 1
elif age_type == "Year":
    answer = 2030 - year
print(answer)

# 전체 코드 줄별 설명
# year = int(input())  # input은 입력, int는 정수 변환. 출생 연도 입력.
# age_type = input()  # 나이 종류를 문자열로 입력.
# if age_type == "Korea":  # if는 조건, ==는 같음 비교. 한국식 나이인지 확인.
#     answer = 2030 - year + 1  # 현재 연도에서 출생 연도를 빼고 1을 더함.
# elif age_type == "Year":  # elif는 다음 조건 검사. 연 나이인지 확인.
#     answer = 2030 - year  # 연 나이는 연도 차이만 계산.
# print(answer)  # print로 계산한 나이 출력.

# 풀이 요약
# 한국식 나이는 연도 차이+1, 연 나이는 연도 차이입니다. 기준 연도는 문제에서 정한 2030입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
