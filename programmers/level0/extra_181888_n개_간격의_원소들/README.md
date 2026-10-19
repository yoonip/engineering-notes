# n개 간격의 원소들

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181888) · Level 0 · Python3

## 풀이

인덱스 0, n, 2n 위치의 원소를 가져옵니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(num_list, n):
    return num_list[::n]

# 전체 코드 줄별 설명
# def solution(num_list, n):  # def는 함수 정의. 리스트와 추출 간격 입력.
#     return num_list[::n]  # [시작:끝:간격] 슬라이싱. 시작·끝을 생략해 처음부터 끝까지 n칸 간격 추출.

# 풀이 요약
# 인덱스 0, n, 2n 위치의 원소를 가져옵니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
