# 5명씩

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181886) · Level 0 · Python3

## 풀이

각 그룹의 첫 위치는 0, 5, 10 순서입니다. 마지막 소규모 그룹도 자동 포함됩니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(names):
    return names[::5]

# 전체 코드 줄별 설명
# def solution(names):  # def는 함수 정의. 줄 선 사람의 이름 리스트 입력.
#     return names[::5]  # [::5]는 인덱스 0부터 5칸 간격 슬라이싱. 각 5명 묶음의 첫 사람 선택.

# 풀이 요약
# 각 그룹의 첫 위치는 0, 5, 10 순서입니다. 마지막 소규모 그룹도 자동 포함됩니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
