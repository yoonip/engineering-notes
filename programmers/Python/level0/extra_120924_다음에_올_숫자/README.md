# 다음에 올 숫자

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120924) · Level 0 · Python3

## 풀이

앞 세 항의 차이가 같으면 등차수열이고, 아니면 등비수열입니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(common):
    if common[1] - common[0] == common[2] - common[1]:
        return common[-1] + common[1] - common[0]
    return common[-1] * (common[1] // common[0])

# 전체 코드 줄별 설명
# def solution(common):  # def는 함수 정의. 등차수열 또는 등비수열 입력.
#     if common[1] - common[0] == common[2] - common[1]:  # []는 인덱스 접근, ==는 같음 비교. 첫 두 차이가 같은지 확인.
#         return common[-1] + common[1] - common[0]  # -1은 마지막 원소. 등차수열의 공차를 마지막 값에 더함.
#     return common[-1] * (common[1] // common[0])  # *는 곱셈, //는 정수 나눗셈. 등비수열의 정수 공비를 마지막 값에 곱함.

# 풀이 요약
# 앞 세 항의 차이가 같으면 등차수열이고, 아니면 등비수열입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
