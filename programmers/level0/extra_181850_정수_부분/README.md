# 정수 부분

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181850) · Level 0 · Python3

## 풀이

입력이 음수가 아니므로 int 변환으로 정수 부분을 구합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(flo):
    return int(flo)

# 전체 코드 줄별 설명
# def solution(flo):  # def는 함수 정의. 음이 아닌 실수 입력.
#     return int(flo)  # int는 정수 변환. 실수의 소수 부분을 버리고 정수 부분 반환.

# 풀이 요약
# 입력이 음수가 아니므로 int 변환으로 정수 부분을 구합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
