# ad 제거하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181870) · Level 0 · Python3

## 풀이

ad가 포함되지 않은 문자열만 순서를 유지해 남깁니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(strArr):
    return [text for text in strArr if 'ad' not in text]

# 전체 코드 줄별 설명
# def solution(strArr):  # def는 함수 정의. 문자열 리스트 입력.
#     return [text for text in strArr if 'ad' not in text]  # 리스트 내포의 for는 순회, if는 필터, not in은 부분 문자열이 없음 검사.

# 풀이 요약
# ad가 포함되지 않은 문자열만 순서를 유지해 남깁니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
