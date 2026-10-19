# 뒤에서 5등 위로

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181852) · Level 0 · Python3

## 풀이

가장 작은 다섯 개를 제외하려면 정렬 후 인덱스 5부터 가져옵니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(num_list):
    return sorted(num_list)[5:]

# 전체 코드 줄별 설명
# def solution(num_list):  # def는 함수 정의. 정수 리스트 입력.
#     return sorted(num_list)[5:]  # sorted는 오름차순 정렬, [5:]는 앞 5개를 제외한 나머지 슬라이싱.

# 풀이 요약
# 가장 작은 다섯 개를 제외하려면 정렬 후 인덱스 5부터 가져옵니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
