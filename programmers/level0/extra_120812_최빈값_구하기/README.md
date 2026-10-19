# 최빈값 구하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120812) · Level 0 · Python3

## 풀이

등장 횟수를 센 뒤 가장 높은 빈도를 가진 값이 유일한지 확인합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
from collections import Counter

def solution(array):
    counts = Counter(array)
    highest = max(counts.values())
    modes = [value for value, count in counts.items() if count == highest]
    return modes[0] if len(modes) == 1 else -1

# 전체 코드 줄별 설명
# from collections import Counter  # from 모듈 import 이름은 도구 가져오기. Counter는 원소별 출현 횟수를 저장하는 딕셔너리형 자료구조.
# 
# def solution(array):  # def는 함수 정의. 최빈값을 구할 정수 리스트 입력.
#     counts = Counter(array)  # 각 정수의 등장 횟수 집계.
#     highest = max(counts.values())  # values는 저장된 횟수들을 제공. max로 가장 높은 빈도 계산.
#     modes = [value for value, count in counts.items() if count == highest]  # items는 값·횟수 쌍 제공. 리스트 내포로 최대 빈도를 가진 모든 값 선택.
#     return modes[0] if len(modes) == 1 else -1  # len은 후보 수. 조건 표현식으로 최빈값이 하나면 그 값, 여러 개면 -1 반환.

# 풀이 요약
# 등장 횟수를 센 뒤 가장 높은 빈도를 가진 값이 유일한지 확인합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
