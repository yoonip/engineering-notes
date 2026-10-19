# 왼쪽 오른쪽

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181890) · Level 0 · Python3

## 풀이

앞에서부터 보다가 l 또는 r을 처음 만나는 즉시 해당 부분을 반환합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(str_list):
    for i, direction in enumerate(str_list):
        if direction == 'l':
            return str_list[:i]
        if direction == 'r':
            return str_list[i + 1:]
    return []

# 전체 코드 줄별 설명
# def solution(str_list):  # def는 함수 정의. 방향 문자 리스트 입력.
#     for i, direction in enumerate(str_list):  # enumerate는 인덱스와 방향 문자를 함께 제공.
#         if direction == 'l':  # if는 조건, ==는 같음 비교. 처음 만난 왼쪽 방향인지 확인.
#             return str_list[:i]  # 기준 문자를 제외한 왼쪽 부분 반환.
#         if direction == 'r':  # 처음 만난 오른쪽 방향인지 확인.
#             return str_list[i + 1:]  # 기준 문자를 제외한 오른쪽 부분 반환.
#     return []  # l·r이 하나도 없으면 빈 리스트 반환.

# 풀이 요약
# 앞에서부터 보다가 l 또는 r을 처음 만나는 즉시 해당 부분을 반환합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
