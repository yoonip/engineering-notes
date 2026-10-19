# [PCCE 기출문제] 4번 / 저축

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/250130) · Level 0 · Python3

## 풀이

70 전에는 before, 이후에는 after를 더합니다. 첫 달도 한 달로 세며 예제는 12개월과 2개월입니다.

## 코드와 줄별 설명

빈칸 채우기·한 줄 수정 형식이라 사이트에는 지정된 부분만 제출했습니다. 아래 전체 주석본은 학습용으로 보관합니다.

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
start = int(input())
before = int(input())
after = int(input())
money = start
month = 1
while money < 70:
    money += before
    month += 1
while money < 100:
    money += after
    month += 1
print(month)

# 전체 코드 줄별 설명
# start = int(input())  # input은 한 줄 입력, int는 정수 변환. 첫 달 저축액 입력.
# before = int(input())  # 70만 원 미만일 때의 월 저축액 입력.
# after = int(input())  # 70만 원 이상일 때의 월 저축액 입력.
# money = start  # 첫 달 저축 후 누적 금액 초기화.
# month = 1  # 첫 달을 이미 포함하므로 개월 수는 1부터 시작.
# while money < 70:  # while은 조건이 참인 동안 반복. <는 미만 비교.
#     money += before  # +=는 더해 저장. 70만 원까지 이전 저축액 사용.
#     month += 1  # 저축할 때마다 한 달 증가.
# while money < 100:  # 목표 100만 원에 도달할 때까지 반복.
#     money += after  # 증액된 월 저축액을 더함.
#     month += 1  # 소요 개월 수 증가.
# print(month)  # print로 목표 달성까지의 개월 수 출력.

# 풀이 요약
# 70 전에는 before, 이후에는 after를 더합니다. 첫 달도 한 달로 세며 예제는 12개월과 2개월입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
