# 배열 만들기 2

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181921) · Level 0 · Python3

## 풀이

5에서 시작해 뒤에 0과 5만 붙입니다. 범위를 넘는 후보는 확장하지 않아 불필요한 정수 검사를 줄입니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(l, r):
    candidates = [5]
    answer = []
    for value in candidates:
        if value > r:
            continue
        if value >= l:
            answer.append(value)
        candidates.extend([value * 10, value * 10 + 5])
    return answer or [-1]

# 전체 코드 줄별 설명
# def solution(l, r):  # def는 함수 정의. 숫자 범위의 양 끝 입력.
#     candidates = [5]  # []는 리스트. 0·5로만 이루어진 양의 정수의 시작은 5.
#     answer = []  # 조건을 만족한 정수 저장.
#     for value in candidates:  # 리스트를 앞에서부터 순회. 뒤에 추가한 후보도 차례로 처리.
#         if value > r:  # if는 조건, >는 초과 비교. 상한보다 큰 수 검사.
#             continue  # continue는 현재 반복을 건너뜀. 더 큰 자식 후보도 만들지 않음.
#         if value >= l:  # >=는 이상 비교. 하한까지 만족하는지 검사.
#             answer.append(value)  # append는 끝에 추가. 범위 안의 후보 저장.
#         candidates.extend([value * 10, value * 10 + 5])  # extend는 여러 원소를 끝에 추가. 오른쪽에 0 또는 5를 붙인 후보 생성.
#     return answer or [-1]  # or는 앞 리스트가 비어 있으면 뒤의 [-1] 선택. 후보 생성 순서는 오름차순.

# 풀이 요약
# 5에서 시작해 뒤에 0과 5만 붙입니다. 범위를 넘는 후보는 확장하지 않아 불필요한 정수 검사를 줄입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
