# 1로 만들기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181880) · Level 0 · Python3

## 풀이

짝수와 홀수 모두 정수 나눗셈 //2로 처리할 수 있습니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(num_list):
    count = 0
    for value in num_list:
        while value > 1:
            value //= 2
            count += 1
    return count

# 전체 코드 줄별 설명
# def solution(num_list):  # def는 함수 정의. 1로 만들 정수 리스트 입력.
#     count = 0  # 전체 나누기 횟수 초기화.
#     for value in num_list:  # for로 각 정수 순회.
#         while value > 1:  # while은 조건 반복. 1이 될 때까지 계속.
#             value //= 2  # //=는 정수 나눗셈 후 저장. 홀수도 소수점을 버리면 1을 뺀 뒤 나눈 결과와 같음.
#             count += 1  # +=는 더해 저장. 한 번의 나누기 기록.
#     return count  # 전체 원소의 연산 횟수 합계 반환.

# 풀이 요약
# 짝수와 홀수 모두 정수 나눗셈 //2로 처리할 수 있습니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
