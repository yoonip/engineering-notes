# 진료순서 정하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120835) · Level 0 · Python3

## 풀이

응급도를 내림차순으로 정렬해 순위를 붙인 뒤 원래 입력 순서로 되돌립니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(emergency):
    order = {value: i + 1 for i, value in enumerate(sorted(emergency, reverse=True))}
    return [order[value] for value in emergency]

# 전체 코드 줄별 설명
# def solution(emergency):  # def는 함수 정의. 서로 다른 응급도 리스트 입력.
#     order = {value: i + 1 for i, value in enumerate(sorted(emergency, reverse=True))}  # sorted의 reverse=True는 내림차순, enumerate는 0부터 번호 부여. 딕셔너리 내포로 응급도별 1부터의 순서 저장.
#     return [order[value] for value in emergency]  # []로 진료 순서 조회. 리스트 내포로 원래 환자 순서에 맞춰 반환.

# 풀이 요약
# 응급도를 내림차순으로 정렬해 순위를 붙인 뒤 원래 입력 순서로 되돌립니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
