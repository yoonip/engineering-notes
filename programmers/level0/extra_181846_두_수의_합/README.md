# 두 수의 합

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181846) · Level 0 · Python3

## 풀이

일의 자리부터 두 숫자와 올림을 더합니다. 각 자릿수를 한 번씩 처리하므로 시간 O(두 문자열의 최대 길이)입니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(a, b):
    i, j = len(a) - 1, len(b) - 1
    carry = 0
    digits = []
    while i >= 0 or j >= 0 or carry:
        total = carry
        if i >= 0:
            total += ord(a[i]) - ord('0')
            i -= 1
        if j >= 0:
            total += ord(b[j]) - ord('0')
            j -= 1
        carry, digit = divmod(total, 10)
        digits.append(str(digit))
    return ''.join(reversed(digits))

# 전체 코드 줄별 설명
# def solution(a, b):  # def는 함수 정의. 최대 10만 자리의 두 숫자 문자열 입력.
#     i, j = len(a) - 1, len(b) - 1  # len은 길이. 오른쪽 끝 자릿수의 인덱스 초기화.
#     carry = 0  # 다음 자릿수로 올릴 수 초기화.
#     digits = []  # []는 빈 리스트. 낮은 자릿수부터 계산한 숫자 문자 저장.
#     while i >= 0 or j >= 0 or carry:  # while은 반복, or는 하나라도 참. 남은 자릿수 또는 올림이 있으면 계속.
#         total = carry  # 이번 자릿수 합을 이전 올림으로 시작.
#         if i >= 0:  # if는 조건. 첫 번째 수에 남은 자릿수가 있는지 확인.
#             total += ord(a[i]) - ord('0')  # ord는 문자 코드. 숫자 문자를 0~9 정수로 바꾸어 더함.
#             i -= 1  # -=는 빼서 저장. 다음 높은 자릿수로 이동.
#         if j >= 0:  # 두 번째 수의 남은 자릿수 검사.
#             total += ord(b[j]) - ord('0')  # 두 번째 숫자의 현재 자릿수도 합산.
#             j -= 1  # 다음 높은 자릿수로 이동.
#         carry, digit = divmod(total, 10)  # divmod는 몫과 나머지를 튜플로 반환. 몫은 올림, 나머지는 현재 자릿수.
#         digits.append(str(digit))  # str은 문자열 변환, append는 끝에 추가. 현재 자릿수 기록.
#     return ''.join(reversed(digits))  # reversed는 역순 순회, join은 문자열 연결. 낮은 자리부터 저장한 결과를 뒤집어 반환.

# 풀이 요약
# 일의 자리부터 두 숫자와 올림을 더합니다. 각 자릿수를 한 번씩 처리하므로 시간 O(두 문자열의 최대 길이)입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
