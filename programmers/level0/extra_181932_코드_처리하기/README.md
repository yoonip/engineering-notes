# 코드 처리하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/181932) · Level 0 · Python3

## 풀이

문자 1은 모드를 뒤집고, 나머지는 현재 모드와 인덱스 홀짝이 같을 때만 채택합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(code):
    mode = 0
    result = []
    for index, char in enumerate(code):
        if char == '1':
            mode = 1 - mode
        elif index % 2 == mode:
            result.append(char)
    return ''.join(result) or 'EMPTY'

# 전체 코드 줄별 설명
# def solution(code):  # def는 함수 정의. 처리할 문자열 입력.
#     mode = 0  # 현재 모드 초기화.
#     result = []  # []는 빈 리스트. 선택한 문자 저장.
#     for index, char in enumerate(code):  # enumerate는 인덱스와 문자를 함께 제공.
#         if char == '1':  # if는 조건. 모드 변경 문자 검사.
#             mode = 1 - mode  # 0은 1로, 1은 0으로 바꿈.
#         elif index % 2 == mode:  # elif는 다음 조건, %는 나머지. 인덱스 홀짝이 현재 모드와 같은지 검사.
#             result.append(char)  # append는 리스트 끝에 문자 추가.
#     return ''.join(result) or 'EMPTY'  # join은 문자 연결. or는 앞 값이 빈 문자열이면 뒤의 EMPTY 선택.

# 풀이 요약
# 문자 1은 모드를 뒤집고, 나머지는 현재 모드와 인덱스 홀짝이 같을 때만 채택합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
