# [PCCE 기출문제] 5번 / 심폐소생술

[Level 0 목록 / Level 0 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/340203) · Level 0 · Python3

## 풀이

정답 순서 리스트에서 동작의 인덱스를 찾아 1을 더합니다. 예제 첫 결과는 [2, 4, 5, 1, 3]입니다.

## 코드와 줄별 설명

빈칸 채우기·한 줄 수정 형식이라 사이트에는 지정된 부분만 제출했습니다. 아래 전체 주석본은 학습용으로 보관합니다.

[코드 파일 / Source](solution.py) · [채점 기록 / Grade](grading.json)

```python
def solution(cpr):
    answer = []
    basic_order = ["check", "call", "pressure", "respiration", "repeat"]
    for action in cpr:
        for i in range(len(basic_order)):
            if action == basic_order[i]:
                answer.append(i + 1)
    return answer

# 전체 코드 줄별 설명
# def solution(cpr):  # def는 함수 정의. cpr은 무작위 순서의 동작 이름 리스트.
#     answer = []  # []는 빈 리스트. 단계 번호를 차례로 저장.
#     basic_order = ["check", "call", "pressure", "respiration", "repeat"]  # 올바른 동작 순서를 문자열 리스트로 저장.
#     for action in cpr:  # for는 반복문. 입력 동작을 하나씩 action에 넣어 처리.
#         for i in range(len(basic_order)):  # len은 길이, range는 0부터 길이-1까지의 정수 순서 생성.
#             if action == basic_order[i]:  # if는 조건, ==는 같은 값 비교, []는 인덱스 접근.
#                 answer.append(i + 1)  # append는 끝에 추가. 0부터 시작하는 인덱스에 1을 더해 단계 번호 저장.
#     return answer  # return은 계산한 단계 번호 리스트 반환.

# 풀이 요약
# 정답 순서 리스트에서 동작의 인덱스를 찾아 1을 더합니다. 예제 첫 결과는 [2, 4, 5, 1, 3]입니다.
#
```

## 채점 기록 / Grading record

저장된 사이트 채점 결과는 100점입니다. 코드 파일의 SHA-256과 채점 기록의 SHA-256을 `grading.json`에 남겼습니다. 이 기록을 정리하면서 새로 제출한 것은 아닙니다.

The saved website result is 100/100. The file contains executable code followed by an exact commented copy with Korean notes on syntax and purpose. Source and saved-result hashes are in `grading.json`. This archive update did not resubmit the solution.
