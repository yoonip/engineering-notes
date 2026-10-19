# 문자열 계산하기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/120902) · Level 0 · Python3

## 풀이

연산 기호와 그 다음 숫자를 한 쌍씩 처리하여 앞에서부터 계산합니다.

## 코드와 줄별 설명

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(my_string):
    tokens = my_string.split()
    total = int(tokens[0])
    for i in range(1, len(tokens), 2):
        value = int(tokens[i + 1])
        total += value if tokens[i] == '+' else -value
    return total

# 전체 코드 줄별 설명
# def solution(my_string):  # def는 함수 정의. 덧셈·뺄셈 식 문자열 입력.
#     tokens = my_string.split()  # split은 공백으로 나누어 숫자·기호 문자열 리스트 생성.
#     total = int(tokens[0])  # []는 인덱스 접근. int로 첫 숫자를 정수로 바꿔 초기 합계 설정.
#     for i in range(1, len(tokens), 2):  # range의 간격 2로 연산 기호 위치만 순회. len은 리스트 길이.
#         value = int(tokens[i + 1])  # 기호 다음의 숫자를 정수로 변환.
#         total += value if tokens[i] == '+' else -value  # 조건 표현식으로 덧셈이면 양수, 뺄셈이면 음수를 선택해 +=로 누적.
#     return total  # 계산한 최종 정수 반환.

# 풀이 요약
# 연산 기호와 그 다음 숫자를 한 쌍씩 처리하여 앞에서부터 계산합니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점이다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼다. 이 기록을 정리하면서 새로 제출한 것은 아니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
