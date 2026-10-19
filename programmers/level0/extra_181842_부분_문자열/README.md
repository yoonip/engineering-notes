# 부분 문자열

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181842) · Level 0 · Python3

## 풀이

포함 관계의 방향을 주의해 str1이 str2 안에 있는지 확인합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(str1, str2):
    return int(str1 in str2)

# 전체 코드 줄별 설명
# def solution(str1, str2):  # def는 함수 정의. 찾을 문자열과 원본 문자열 입력.
#     return int(str1 in str2)  # in은 왼쪽 문자열이 오른쪽에 포함되는지 검사. int는 결과를 1·0으로 변환.

# 풀이 요약
# 포함 관계의 방향을 주의해 str1이 str2 안에 있는지 확인합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
