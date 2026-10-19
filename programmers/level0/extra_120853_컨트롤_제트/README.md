# 컨트롤 제트

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120853) · Level 0 · Python3

## 풀이

Z를 만나면 스택의 마지막 숫자를 제거하고 남은 값만 합산합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(s):
    stack = []
    for token in s.split():
        if token == 'Z':
            stack.pop()
        else:
            stack.append(int(token))
    return sum(stack)

# 전체 코드 줄별 설명
# def solution(s):  # def는 함수 정의. 숫자와 취소 명령 Z의 문자열 입력.
#     stack = []  # []는 빈 리스트. 아직 취소되지 않은 숫자들을 스택으로 저장.
#     for token in s.split():  # split은 공백으로 나누기, for는 각 항목 순회.
#         if token == 'Z':  # if는 조건, ==는 같음 비교. 취소 명령인지 확인.
#             stack.pop()  # pop은 마지막 숫자 제거. 가장 최근 더한 수를 취소.
#         else:  # 숫자 문자열인 경우.
#             stack.append(int(token))  # int는 정수 변환, append는 끝에 추가.
#     return sum(stack)  # sum으로 취소되지 않은 숫자 합계 반환.

# 풀이 요약
# Z를 만나면 스택의 마지막 숫자를 제거하고 남은 값만 합산합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
