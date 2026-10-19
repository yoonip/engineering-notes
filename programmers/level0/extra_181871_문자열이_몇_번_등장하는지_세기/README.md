# 문자열이 몇 번 등장하는지 세기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181871) · Level 0 · Python3

## 풀이

모든 시작 위치를 검사하므로 패턴이 서로 겹쳐 등장하는 경우도 모두 셉니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(myString, pat):
    return sum(myString.startswith(pat, i) for i in range(len(myString)))

# 전체 코드 줄별 설명
# def solution(myString, pat):  # def는 함수 정의. 원본 문자열과 찾을 패턴 입력.
#     return sum(myString.startswith(pat, i) for i in range(len(myString)))  # range·len으로 모든 시작 위치 순회. startswith(패턴,위치)는 해당 위치의 패턴 검사. sum은 참을 1로 합산.

# 풀이 요약
# 모든 시작 위치를 검사하므로 패턴이 서로 겹쳐 등장하는 경우도 모두 셉니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
