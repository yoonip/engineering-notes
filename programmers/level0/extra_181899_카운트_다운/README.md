# 카운트 다운

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181899) · Level 0 · Python3

## 풀이

간격을 -1로 지정해 양 끝을 포함하는 감소 수열을 만듭니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(start_num, end_num):
    return list(range(start_num, end_num - 1, -1))

# 전체 코드 줄별 설명
# def solution(start_num, end_num):  # def는 함수 정의. 시작값과 끝값 입력.
#     return list(range(start_num, end_num - 1, -1))  # range의 간격 -1은 감소 수열. 끝은 제외하므로 end_num-1 사용, list로 변환.

# 풀이 요약
# 간격을 -1로 지정해 양 끝을 포함하는 감소 수열을 만듭니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
