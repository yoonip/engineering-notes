# 다항식 더하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120863) · Level 0 · Python3

## 풀이

일차 항의 계수와 상수를 따로 합산합니다. 계수 1과 불필요한 0 항을 생략해 가장 짧게 표시합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(polynomial):
    coefficient, constant = 0, 0
    for term in polynomial.split(' + '):
        if term.endswith('x'):
            coefficient += int(term[:-1] or '1')
        else:
            constant += int(term)
    parts = []
    if coefficient:
        parts.append('x' if coefficient == 1 else str(coefficient) + 'x')
    if constant:
        parts.append(str(constant))
    return ' + '.join(parts)

# 전체 코드 줄별 설명
# def solution(polynomial):  # def는 함수 정의. 덧셈으로 된 일차 다항식 문자열 입력.
#     coefficient, constant = 0, 0  # x의 계수 합과 상수 합을 각각 초기화.
#     for term in polynomial.split(' + '):  # split은 지정 구분자로 나누기. + 기호 양쪽 공백까지 포함해 항별 분리.
#         if term.endswith('x'):  # if는 조건, endswith는 x로 끝나는지 검사. 일차 항인지 확인.
#             coefficient += int(term[:-1] or '1')  # [:-1]로 x 제외. or는 계수가 생략되면 1 선택, int는 정수 변환, +=는 누적.
#         else:  # 상수 항인 경우.
#             constant += int(term)  # 문자열을 정수로 바꾸어 상수 합에 더함.
#     parts = []  # []는 빈 리스트. 출력할 일차 항과 상수 항 저장.
#     if coefficient:  # 계수가 0이 아닌 경우만 일차 항 출력.
#         parts.append('x' if coefficient == 1 else str(coefficient) + 'x')  # 조건 표현식으로 계수 1은 생략. str은 문자열 변환, append는 항 추가.
#     if constant:  # 상수가 0이 아닌 경우만 출력.
#         parts.append(str(constant))  # 상수 문자열을 끝에 추가.
#     return ' + '.join(parts)  # join은 항들 사이에 +와 공백을 넣어 문자열 연결.

# 풀이 요약
# 일차 항의 계수와 상수를 따로 합산합니다. 계수 1과 불필요한 0 항을 생략해 가장 짧게 표시합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
