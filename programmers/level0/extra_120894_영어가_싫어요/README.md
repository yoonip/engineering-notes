# 영어가 싫어요

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120894) · Level 0 · Python3

## 풀이

영어 이름을 대응하는 숫자 문자로 치환한 뒤 정수로 변환합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(numbers):
    words = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')
    for value, word in enumerate(words):
        numbers = numbers.replace(word, str(value))
    return int(numbers)

# 전체 코드 줄별 설명
# def solution(numbers):  # def는 함수 정의. 숫자 영어 이름을 연결한 문자열 입력.
#     words = ('zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')  # ()는 튜플. 숫자 0~9의 영어 이름을 순서대로 저장.
#     for value, word in enumerate(words):  # enumerate는 0부터의 번호와 단어를 함께 제공.
#         numbers = numbers.replace(word, str(value))  # str은 숫자 문자열 변환, replace는 영어 이름을 해당 숫자로 모두 치환.
#     return int(numbers)  # int로 완성된 숫자 문자열을 정수로 변환.

# 풀이 요약
# 영어 이름을 대응하는 숫자 문자로 치환한 뒤 정수로 변환합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
