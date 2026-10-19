# 팩토리얼

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120848) · Level 0 · Python3

## 풀이

다음 팩토리얼이 n을 넘지 않을 때만 정수 i를 증가시킵니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(n):
    i, product = 1, 1
    while product * (i + 1) <= n:
        i += 1
        product *= i
    return i

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의. 팩토리얼 값의 상한 입력.
#     i, product = 1, 1  # 현재 정수 i와 i! 값을 각각 1로 초기화.
#     while product * (i + 1) <= n:  # while은 조건 반복. 다음 팩토리얼 (i+1)!도 상한 이하인지 검사.
#         i += 1  # +=는 더해 저장. 다음 정수로 이동.
#         product *= i  # *=는 곱해 저장. 새 i! 값 계산.
#     return i  # 더 증가시킬 수 없을 때 현재 i가 가능한 최댓값.

# 풀이 요약
# 다음 팩토리얼이 n을 넘지 않을 때만 정수 i를 증가시킵니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
