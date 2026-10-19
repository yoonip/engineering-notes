# 인덱스 바꾸기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120895) · Level 0 · Python3

## 풀이

문자열을 리스트로 바꾸어 두 위치를 교환한 뒤 다시 문자열로 만듭니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(my_string, num1, num2):
    chars = list(my_string)
    chars[num1], chars[num2] = chars[num2], chars[num1]
    return ''.join(chars)

# 전체 코드 줄별 설명
# def solution(my_string, num1, num2):  # def는 함수 정의. 문자열과 교환할 두 인덱스 입력.
#     chars = list(my_string)  # list는 문자열을 수정 가능한 문자 리스트로 변환.
#     chars[num1], chars[num2] = chars[num2], chars[num1]  # 다중 대입으로 오른쪽 두 값을 먼저 읽어 위치를 맞바꿈.
#     return ''.join(chars)  # join은 문자 리스트를 문자열로 연결. return은 결과 반환.

# 풀이 요약
# 문자열을 리스트로 바꾸어 두 위치를 교환한 뒤 다시 문자열로 만듭니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
