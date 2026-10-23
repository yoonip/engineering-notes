# [PCCE 기출문제] 8번 / 창고 정리

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/250126) · Level 0 · Python3

## 풀이

이름 리스트와 수량 리스트의 위치를 맞춰 관리합니다. 새 물건은 이름을 등록해야 같은 물건을 합칠 수 있습니다.

## 코드와 줄별 설명

빈칸 채우기·한 줄 수정 형식이라 사이트에는 지정된 부분만 제출했습니다. 아래 전체 주석본은 학습용으로 보관합니다.

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(storage, num):
    clean_storage = []
    clean_num = []
    for i in range(len(storage)):
        if storage[i] in clean_storage:
            pos = clean_storage.index(storage[i])
            clean_num[pos] += num[i]
        else:
            clean_storage.append(storage[i])
            clean_num.append(num[i])
    max_num = max(clean_num)
    answer = clean_storage[clean_num.index(max_num)]
    return answer

# 전체 코드 줄별 설명
# def solution(storage, num):  # def는 함수 정의. 물건 이름과 수량 리스트를 입력받음.
#     clean_storage = []  # []는 빈 리스트. 중복을 합친 물건 이름 저장.
#     clean_num = []  # 같은 위치에 해당 물건의 합계 수량 저장.
#     for i in range(len(storage)):  # len은 길이, range는 0부터 길이-1까지 순회.
#         if storage[i] in clean_storage:  # in은 포함 여부. []로 현재 물건 이름 조회 후 이미 등록되었는지 확인.
#             pos = clean_storage.index(storage[i])  # index는 값이 처음 나오는 위치 반환. 합산할 수량 위치를 찾음.
#             clean_num[pos] += num[i]  # +=는 더해 저장. 같은 이름의 기존 수량에 더함.
#         else:  # 처음 보는 물건 이름인 경우.
#             clean_storage.append(storage[i])  # append는 끝에 추가. 수량이 아니라 물건 이름을 저장하도록 수정.
#             clean_num.append(num[i])  # 새 물건의 수량을 같은 위치에 저장.
#     max_num = max(clean_num)  # max는 최댓값. 가장 많은 수량 계산.
#     answer = clean_storage[clean_num.index(max_num)]  # 최대 수량의 인덱스로 그 물건의 이름 조회.
#     return answer  # 가장 수량이 많은 물건 이름 반환.

# 풀이 요약
# 이름 리스트와 수량 리스트의 위치를 맞춰 관리합니다. 새 물건은 이름을 등록해야 같은 물건을 합칠 수 있습니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
