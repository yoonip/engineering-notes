# 문자열 바꿔서 찾기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181864) · Level 0 · Python3

## 풀이

한 번의 문자 순회에서 A와 B를 바꾸어 이미 바꾼 문자를 다시 치환하는 실수를 피합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(myString, pat):
    changed = ''.join('B' if char == 'A' else 'A' for char in myString)
    return int(pat in changed)

# 전체 코드 줄별 설명
# def solution(myString, pat):  # def는 함수 정의. A·B 문자열과 찾을 패턴 입력.
#     changed = ''.join('B' if char == 'A' else 'A' for char in myString)  # 조건 표현식으로 A·B를 교환. 생성기 표현식 결과를 join으로 연결.
#     return int(pat in changed)  # in은 부분 문자열 포함 검사. int는 참·거짓을 1·0으로 변환.

# 풀이 요약
# 한 번의 문자 순회에서 A와 B를 바꾸어 이미 바꾼 문자를 다시 치환하는 실수를 피합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
