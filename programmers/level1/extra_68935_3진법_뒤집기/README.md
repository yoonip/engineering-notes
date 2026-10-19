# 3진법 뒤집기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/68935) · Level 1 · Python3

유형: 수학 · 진법 변환

## 풀이 원리

3으로 나눈 나머지는 낮은 자리부터 나온다. 그 순서대로 문자열에 붙이면 이미 뒤집힌 3진수다. 이 문자열을 밑이 3인 숫자로 해석해 10진수 정수를 얻는다.

3진 자릿수 D: 반복 D회, 문자열 연결을 포함한 보수적 시간 상한 O(D²), 공간 O(D).

## 공식 예제

입력 인수: `[45]`

반환값: `7`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(n):
    ternary = ""
    while n > 0:
        ternary += str(n % 3)
        n //= 3
    answer = int(ternary, 3)
    return answer

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 자연수 n을 입력받는 함수
#     ternary = ""  # =는 값 저장. 뒤집힌 3진법 숫자를 저장할 빈 문자열
#     while n > 0:  # while은 조건이 참인 동안 반복. >는 큼 비교. n이 0보다 큰 동안 반복
#         ternary += str(n % 3)  # str은 문자열 변환. +=는 더하거나 연결한 값을 저장. %는 나머지. n을 3으로 나눈 나머지를 문자열로 변환하여 뒤에 추가
#         n //= 3  # //=는 정수 몫을 저장. n을 3으로 나눈 몫으로 갱신
#     answer = int(ternary, 3)  # int는 정수 변환. =는 값 저장. ternary를 3진법 숫자로 해석하여 10진수 정수로 변환
#     return answer  # return은 결과를 돌려주고 함수 종료. 최종 10진수 결과 반환

# 풀이 요약
# 3으로 나눈 나머지는 낮은 자리부터 나온다. 그 순서대로 문자열에 붙이면 이미 뒤집힌 3진수다. 이 문자열을 밑이 3인 숫자로 해석해 10진수 정수를 얻는다.
# 3진 자릿수 D: 반복 D회, 문자열 연결을 포함한 보수적 시간 상한 O(D²), 공간 O(D).
```

## 확인한 범위

2026-10-16 02:28:35의 Python3 제출 내역에서 정답 100/100을 확인했다. 원본은 그대로 보관했다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
