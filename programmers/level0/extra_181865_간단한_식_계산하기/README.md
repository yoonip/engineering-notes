# 간단한 식 계산하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181865) · Level 0 · Python3

## 풀이

문자열을 세 항목으로 나눈 뒤 연산 기호에 맞는 계산을 적용합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(binomial):
    left, operator, right = binomial.split()
    a, b = int(left), int(right)
    if operator == '+':
        return a + b
    if operator == '-':
        return a - b
    return a * b

# 전체 코드 줄별 설명
# def solution(binomial):  # def는 함수 정의. 두 정수와 연산 기호로 된 문자열 입력.
#     left, operator, right = binomial.split()  # split은 공백 분리. 세 항목을 왼쪽 수·기호·오른쪽 수로 나누어 대입.
#     a, b = int(left), int(right)  # int는 문자열을 정수로 변환. 두 숫자를 각각 저장.
#     if operator == '+':  # if는 조건, ==는 같음 비교. 덧셈 기호 검사.
#         return a + b  # 두 정수의 합 반환.
#     if operator == '-':  # 뺄셈 기호 검사.
#         return a - b  # 두 정수의 차 반환.
#     return a * b  # 남은 연산 기호 *는 곱셈이므로 곱 반환.

# 풀이 요약
# 문자열을 세 항목으로 나눈 뒤 연산 기호에 맞는 계산을 적용합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
