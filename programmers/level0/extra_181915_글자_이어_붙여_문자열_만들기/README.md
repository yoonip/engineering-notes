# 글자 이어 붙여 문자열 만들기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181915) · Level 0 · Python3

## 풀이

인덱스가 가리키는 문자를 주어진 순서 그대로 연결합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(my_string, index_list):
    return ''.join(my_string[i] for i in index_list)

# 전체 코드 줄별 설명
# def solution(my_string, index_list):  # def는 함수 정의. 원본 문자열과 글자 위치 리스트 입력.
#     return ''.join(my_string[i] for i in index_list)  # []는 인덱스 접근. 생성기 표현식으로 지정 글자를 순서대로 꺼내 join으로 연결.

# 풀이 요약
# 인덱스가 가리키는 문자를 주어진 순서 그대로 연결합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
