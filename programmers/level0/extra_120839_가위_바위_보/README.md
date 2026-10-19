# 가위 바위 보

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120839) · Level 0 · Python3

## 풀이

가위에는 바위, 바위에는 보, 보에는 가위를 대응시킵니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(rsp):
    wins = {'2': '0', '0': '5', '5': '2'}
    return ''.join(wins[char] for char in rsp)

# 전체 코드 줄별 설명
# def solution(rsp):  # def는 함수 정의. 가위·바위·보를 표시한 문자열 입력.
#     wins = {'2': '0', '0': '5', '5': '2'}  # {}는 딕셔너리. 각 상대 값에 이기는 값을 대응.
#     return ''.join(wins[char] for char in rsp)  # []로 이기는 값 조회. 생성기 표현식 결과를 join으로 입력 순서대로 연결.

# 풀이 요약
# 가위에는 바위, 바위에는 보, 보에는 가위를 대응시킵니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
