# 콜라츠 추측

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12943) · Level 1 · Python3

유형: 구현 · 반복 · 종료 조건

## 풀이 원리

짝수는 절반, 홀수는 3배+1로 바꾸며 횟수를 셉니다. 1이 되면 멈추고, 이미 500번 했는데도 1이 아니면 -1을 반환합니다. 정확히 500번째에 1이 되면 다음 while 조건에서 종료돼 500이 반환됩니다.

실제 반복 T≤500: 시간 O(T), 보조 공간 O(1).

## 공식 예제

입력 인수: `[6]`

반환값: `8`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(num):
    answer = 0
    while num != 1:
        if answer >= 500:
            return -1
        if num % 2 == 0:
            num //= 2
        else:
            num = num * 3 + 1
        answer += 1
    return answer

# 전체 코드 줄별 설명
# def solution(num):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. num: 처음 입력받은 정수
#     answer = 0  # =는 값 저장. 작업을 반복한 횟수를 저장하는 변수. 처음에는 0
#     while num != 1:  # while은 조건이 참인 동안 반복. !=는 다름 비교. num이 1이 아닌 동안 계속 반복. !=는 같지 않다는 뜻
#         if answer >= 500:  # if는 조건이 참일 때 실행. >=는 이상 비교. 이미 500번 반복했다면
#             return -1  # return은 결과를 돌려주고 함수 종료. 500번 안에 1을 만들지 못했으므로 -1 반환 후 함수 종료
#         if num % 2 == 0:  # if는 조건이 참일 때 실행. ==는 같음 비교. %는 나머지. num을 2로 나눈 나머지가 0이면 짝수라는 뜻
#             num //= 2  # //=는 정수 몫을 저장. num을 2로 나눈 정수 몫을 다시 num에 저장
#         else:  # else는 앞 조건들에 해당하지 않는 경우. 짝수가 아니라면 홀수이므로
#             num = num * 3 + 1  # =는 값 저장. 현재 숫자에 3을 곱하고 1을 더한 값을 저장
#         answer += 1  # +=는 더하거나 연결한 값을 저장. 작업을 한 번 수행했으므로 반복 횟수를 1 증가
#     return answer  # return은 결과를 돌려주고 함수 종료. num이 1이 되었다면 총 반복 횟수를 반환

# 풀이 요약
# 짝수는 절반, 홀수는 3배+1로 바꾸며 횟수를 센다. 1이 되면 멈추고, 이미 500번 했는데도 1이 아니면 -1을 반환한다. 정확히 500번째에 1이 되면 다음 while 조건에서 종료돼 500이 반환된다.
# 실제 반복 T≤500: 시간 O(T), 보조 공간 O(1).
```

## 확인한 범위

2026-10-16 02:37:18의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
