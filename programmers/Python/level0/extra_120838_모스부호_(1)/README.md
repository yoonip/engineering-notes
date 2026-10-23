# 모스부호 (1)

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120838) · Level 0 · Python3

## 풀이

문제에서 제공한 모스부호 표를 딕셔너리로 만들어 각 부호를 문자로 바꿉니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(letter):
    codes = '.- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. -- -. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --..'.split()
    morse = {code: chr(97 + i) for i, code in enumerate(codes)}
    return ''.join(morse[code] for code in letter.split())

# 전체 코드 줄별 설명
# def solution(letter):  # def는 함수 정의. 공백으로 나눈 모스부호 문자열 입력.
#     codes = '.- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. -- -. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --..'.split()  # split은 공백으로 분리. a부터 z까지의 모스부호 표 저장.
#     morse = {code: chr(97 + i) for i, code in enumerate(codes)}  # 딕셔너리 내포. enumerate는 번호와 부호 제공, chr은 문자 코드를 문자로 변환. 97은 a의 코드.
#     return ''.join(morse[code] for code in letter.split())  # 공백으로 부호를 나눈 뒤 []로 알파벳을 조회하고 join으로 연결.

# 풀이 요약
# 문제에서 제공한 모스부호 표를 딕셔너리로 만들어 각 부호를 문자로 바꿉니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
