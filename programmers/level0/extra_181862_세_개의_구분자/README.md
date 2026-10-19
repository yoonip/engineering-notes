# 세 개의 구분자

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181862) · Level 0 · Python3

## 풀이

구분자를 공백 하나로 통일하면 split으로 빈 조각 없이 나눌 수 있습니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(myStr):
    separated = myStr.replace('a', ' ').replace('b', ' ').replace('c', ' ')
    return separated.split() or ['EMPTY']

# 전체 코드 줄별 설명
# def solution(myStr):  # def는 함수 정의. a·b·c로 나눌 문자열 입력.
#     separated = myStr.replace('a', ' ').replace('b', ' ').replace('c', ' ')  # replace는 문자열 치환. 세 구분자를 모두 공백으로 바꿔 통일.
#     return separated.split() or ['EMPTY']  # split()은 연속 공백과 빈 조각을 무시하고 분리. or는 결과가 비어 있으면 EMPTY 리스트 선택.

# 풀이 요약
# 구분자를 공백 하나로 통일하면 split으로 빈 조각 없이 나눌 수 있습니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
