# 날짜 비교하기

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181838) · Level 0 · Python3

## 풀이

연·월·일 순서의 리스트 비교는 날짜의 선후 비교와 같습니다. 같은 날짜는 0입니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(date1, date2):
    return int(date1 < date2)

# 전체 코드 줄별 설명
# def solution(date1, date2):  # def는 함수 정의. [연,월,일] 형식의 두 리스트 입력.
#     return int(date1 < date2)  # 리스트의 < 비교는 앞 항목부터 차례대로 비교. int로 참·거짓을 1·0으로 변환.

# 풀이 요약
# 연·월·일 순서의 리스트 비교는 날짜의 선후 비교와 같습니다. 같은 날짜는 0입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
