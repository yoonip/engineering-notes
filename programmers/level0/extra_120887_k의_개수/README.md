# k의 개수

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120887) · Level 0 · Python3

## 풀이

범위 안 각 정수의 문자열에서 k가 나온 횟수를 더합니다. 같은 수의 중복 자릿수도 셉니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(i, j, k):
    digit = str(k)
    return sum(str(value).count(digit) for value in range(i, j + 1))

# 전체 코드 줄별 설명
# def solution(i, j, k):  # def는 함수 정의. 범위 양 끝과 셀 숫자 입력.
#     digit = str(k)  # str은 정수를 숫자 문자열로 변환.
#     return sum(str(value).count(digit) for value in range(i, j + 1))  # range는 양 끝 포함 범위 순회, count는 문자 출현 횟수, sum은 모든 수의 횟수 합산.

# 풀이 요약
# 범위 안 각 정수의 문자열에서 k가 나온 횟수를 더합니다. 같은 수의 중복 자릿수도 셉니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
