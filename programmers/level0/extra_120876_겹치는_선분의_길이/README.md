# 겹치는 선분의 길이

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120876) · Level 0 · Python3

## 풀이

점이 아니라 길이 1인 구간의 덮인 횟수를 세면 끝점만 만나는 경우를 길이에 포함하지 않습니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(lines):
    counts = [0] * 200
    for start, end in lines:
        for x in range(start, end):
            counts[x + 100] += 1
    return sum(count >= 2 for count in counts)

# 전체 코드 줄별 설명
# def solution(lines):  # def는 함수 정의. 세 선분의 시작·끝 좌표 입력.
#     counts = [0] * 200  # []는 리스트, *는 반복. 좌표 -100부터 100까지의 단위 구간 200개 초기화.
#     for start, end in lines:  # 각 선분의 양 끝 좌표를 나누어 받음.
#         for x in range(start, end):  # range는 끝 제외. 길이 1인 구간 [x,x+1)을 순회하므로 끝점을 제외.
#             counts[x + 100] += 1  # 음수 좌표에 100을 더해 인덱스로 변환. 해당 구간을 덮는 선분 수 증가.
#     return sum(count >= 2 for count in counts)  # >=는 이상 비교. 선분 두 개 이상이 덮는 단위 구간 수를 sum으로 계산.

# 풀이 요약
# 점이 아니라 길이 1인 구간의 덮인 횟수를 세면 끝점만 만나는 경우를 길이에 포함하지 않습니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
