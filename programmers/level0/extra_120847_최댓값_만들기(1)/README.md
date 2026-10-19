# 최댓값 만들기(1)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120847) · Level 0 · Python3

## 풀이

모든 수가 0 이상이므로 가장 큰 두 원소의 곱이 최대입니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(numbers):
    values = sorted(numbers)
    return values[-1] * values[-2]

# 전체 코드 줄별 설명
# def solution(numbers):  # def는 함수 정의. 음이 아닌 정수 리스트 입력.
#     values = sorted(numbers)  # sorted는 오름차순 정렬한 새 리스트 반환.
#     return values[-1] * values[-2]  # -1은 마지막, -2는 끝에서 두 번째. 가장 큰 두 수를 곱함.

# 풀이 요약
# 모든 수가 0 이상이므로 가장 큰 두 원소의 곱이 최대입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
