# 두 수의 연산값 비교하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181938) · Level 0 · Python3

## 풀이

연결한 수와 2ab를 각각 계산해 큰 수를 반환합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(a, b):
    return max(int(str(a) + str(b)), 2 * a * b)

# 전체 코드 줄별 설명
# def solution(a, b):  # def는 함수 정의. 두 정수 a와 b를 입력받음.
#     return max(int(str(a) + str(b)), 2 * a * b)  # str로 바꿔 +로 연결한 수와 *로 곱한 수를 max로 비교. int는 정수 변환.

# 풀이 요약
# 연결한 수와 2ab를 각각 계산해 큰 수를 반환합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
