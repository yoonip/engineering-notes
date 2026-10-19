# 배열의 길이에 따라 다른 연산하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181854) · Level 0 · Python3

## 풀이

길이의 홀짝에 맞는 시작 인덱스를 정하고 두 칸씩 이동합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(arr, n):
    start = 0 if len(arr) % 2 else 1
    for i in range(start, len(arr), 2):
        arr[i] += n
    return arr

# 전체 코드 줄별 설명
# def solution(arr, n):  # def는 함수 정의. 정수 리스트와 더할 값 입력.
#     start = 0 if len(arr) % 2 else 1  # len은 길이, %는 나머지. 길이 홀수면 짝수 인덱스 0, 짝수면 홀수 인덱스 1부터 시작.
#     for i in range(start, len(arr), 2):  # range(시작,끝,간격)로 해당 홀짝 인덱스만 순회.
#         arr[i] += n  # []로 원소 접근, +=는 더해 저장. 선택한 위치에 n 추가.
#     return arr  # 수정된 리스트 반환.

# 풀이 요약
# 길이의 홀짝에 맞는 시작 인덱스를 정하고 두 칸씩 이동합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
