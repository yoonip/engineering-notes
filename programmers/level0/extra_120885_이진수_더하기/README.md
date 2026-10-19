# 이진수 더하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120885) · Level 0 · Python3

## 풀이

두 이진수를 정수로 바꿔 더한 뒤 이진 문자열로 다시 바꿉니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(bin1, bin2):
    return bin(int(bin1, 2) + int(bin2, 2))[2:]

# 전체 코드 줄별 설명
# def solution(bin1, bin2):  # def는 함수 정의. 두 이진수 문자열 입력.
#     return bin(int(bin1, 2) + int(bin2, 2))[2:]  # int(문자열,2)는 이진수 해석. bin은 합계를 0b 접두사가 있는 이진 문자열로 변환, [2:]로 접두사 제거.

# 풀이 요약
# 두 이진수를 정수로 바꿔 더한 뒤 이진 문자열로 다시 바꿉니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
