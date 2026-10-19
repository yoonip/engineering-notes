# 암호 해독

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120892) · Level 0 · Python3

## 풀이

문자 순번은 1부터지만 인덱스는 0부터이므로 첫 위치에 1을 뺍니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(cipher, code):
    return cipher[code - 1::code]

# 전체 코드 줄별 설명
# def solution(cipher, code):  # def는 함수 정의. 암호 문자열과 추출할 순번의 배수 입력.
#     return cipher[code - 1::code]  # [시작::간격]은 슬라이싱. code번째 문자의 인덱스 code-1부터 code칸 간격 추출.

# 풀이 요약
# 문자 순번은 1부터지만 인덱스는 0부터이므로 첫 위치에 1을 뺍니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
