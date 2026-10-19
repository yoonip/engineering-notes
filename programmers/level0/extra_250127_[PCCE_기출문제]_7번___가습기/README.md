# [PCCE 기출문제] 7번 / 가습기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/250127) · Level 0 · Python3

## 풀이

각 보조 함수가 담당하는 모드를 구별해 호출합니다. 자동 모드는 습도가 높을수록 단계를 줄입니다.

## 코드와 줄별 설명

빈칸 채우기·한 줄 수정 형식이라 사이트에는 지정된 부분만 제출했습니다. 아래 전체 주석본은 학습용으로 보관합니다.

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def func1(humidity, val_set):
    if humidity < val_set:
        return 3
    return 1

def func2(humidity):
    if humidity >= 50:
        return 0
    elif humidity >= 40:
        return 1
    elif humidity >= 30:
        return 2
    elif humidity >= 20:
        return 3
    elif humidity >= 10:
        return 4
    else:
        return 5

def func3(humidity, val_set):
    if humidity < val_set:
        return 1
    return 0

def solution(mode_type, humidity, val_set):
    answer = 0
    if mode_type == "auto":
        answer = func2(humidity)
    elif mode_type == "target":
        answer = func1(humidity, val_set)
    elif mode_type == "minimum":
        answer = func3(humidity, val_set)
    return answer

# 전체 코드 줄별 설명
# def func1(humidity, val_set):  # def는 함수 정의. 목표 습도 모드의 가습 단계를 구함.
#     if humidity < val_set:  # if는 조건문. 현재 습도가 설정값 미만인지 비교.
#         return 3  # 설정값 미만이면 3단계 반환.
#     return 1  # 설정값 이상이면 1단계 반환.
# 
# def func2(humidity):  # 자동 모드의 가습 단계를 구하는 함수.
#     if humidity >= 50:  # >=는 이상 비교. 습도 50 이상 검사.
#         return 0  # 가습하지 않음.
#     elif humidity >= 40:  # elif는 앞 조건이 거짓일 때 다음 조건 검사.
#         return 1  # 습도 40 이상 50 미만이면 1단계.
#     elif humidity >= 30:  # 습도 30 이상 40 미만인지 확인.
#         return 2  # 2단계 반환.
#     elif humidity >= 20:  # 습도 20 이상 30 미만인지 확인.
#         return 3  # 3단계 반환.
#     elif humidity >= 10:  # 습도 10 이상 20 미만인지 확인.
#         return 4  # 4단계 반환.
#     else:  # 위 조건이 모두 거짓이면 습도 10 미만.
#         return 5  # 가장 강한 5단계 반환.
# 
# def func3(humidity, val_set):  # 최소 가습 모드의 단계를 구하는 함수.
#     if humidity < val_set:  # 현재 습도가 설정값보다 낮은지 비교.
#         return 1  # 부족할 때만 1단계 가습.
#     return 0  # 충분하면 가습하지 않음.
# 
# def solution(mode_type, humidity, val_set):  # 모드 이름·현재 습도·설정값을 받는 정답 함수.
#     answer = 0  # 반환할 가습 단계 초기화.
#     if mode_type == "auto":  # ==는 같음 비교. 자동 모드인지 확인.
#         answer = func2(humidity)  # 괄호 ()로 자동 모드 함수 호출.
#     elif mode_type == "target":  # 목표 습도 모드인지 확인.
#         answer = func1(humidity, val_set)  # 두 인자를 쉼표로 구분해 목표 모드 함수 호출.
#     elif mode_type == "minimum":  # 최소 가습 모드인지 확인.
#         answer = func3(humidity, val_set)  # 최소 가습 모드의 단계 계산.
#     return answer  # 계산한 가습 단계 반환.

# 풀이 요약
# 각 보조 함수가 담당하는 모드를 구별해 호출합니다. 자동 모드는 습도가 높을수록 단계를 줄입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
