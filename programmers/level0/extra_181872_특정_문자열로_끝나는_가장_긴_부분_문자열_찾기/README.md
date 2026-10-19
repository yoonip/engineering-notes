# 특정 문자열로 끝나는 가장 긴 부분 문자열 찾기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181872) · Level 0 · Python3

## 풀이

가장 뒤에 등장한 pat까지 처음부터 가져오면 가능한 가장 긴 부분 문자열입니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(myString, pat):
    end = myString.rfind(pat) + len(pat)
    return myString[:end]

# 전체 코드 줄별 설명
# def solution(myString, pat):  # def는 함수 정의. 문자열과 끝부분 패턴 입력.
#     end = myString.rfind(pat) + len(pat)  # rfind는 패턴이 마지막으로 시작하는 인덱스, len은 길이. 패턴이 끝난 다음 위치 계산.
#     return myString[:end]  # [:끝]은 처음부터 끝 직전까지의 슬라이싱.

# 풀이 요약
# 가장 뒤에 등장한 pat까지 처음부터 가져오면 가능한 가장 긴 부분 문자열입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
