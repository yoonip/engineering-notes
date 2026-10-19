# 원소들의 곱과 합

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181929) · Level 0 · Python3

## 풀이

곱과 합의 제곱을 각각 계산한 뒤 비교합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(num_list):
    product = 1
    for value in num_list:
        product *= value
    return int(product < sum(num_list) ** 2)

# 전체 코드 줄별 설명
# def solution(num_list):  # def는 함수 정의. 정수 리스트 입력.
#     product = 1  # 곱셈의 시작값은 1.
#     for value in num_list:  # for로 각 정수 순회.
#         product *= value  # *=는 곱해 저장. 전체 원소의 곱 누적.
#     return int(product < sum(num_list) ** 2)  # sum은 합계, **는 제곱, <는 미만 비교, int는 참·거짓을 1·0으로 변환.

# 풀이 요약
# 곱과 합의 제곱을 각각 계산한 뒤 비교합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
