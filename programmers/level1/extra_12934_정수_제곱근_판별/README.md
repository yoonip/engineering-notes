# 정수 제곱근 판별

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12934) · Level 1 · Python3

유형: 정수론 · 정수 제곱근

## 풀이 원리

isqrt는 n의 제곱근을 내림한 정수를 돌려준다. 그 수의 제곱이 n과 같을 때만 완전제곱수이므로 다음 정수의 제곱을 반환한다. 그렇지 않으면 -1이다. 실수 제곱근의 반올림에 의존하지 않는다.

정수 제곱근을 한 번 계산한다. 내부 비용은 정수 비트 수에 따르며 문제의 고정 정수 범위에서 보조 공간 O(1).

## 공식 예제

입력 인수: `[121]`

반환값: `144`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
from math import isqrt

def solution(n):
    x = isqrt(n)
    if x * x == n:
        return (x + 1) ** 2
    return -1

# 전체 코드 줄별 설명
# from math import isqrt  # from math import는 math 모듈에서 이름을 가져옴. isqrt는 제곱근을 내림한 정수를 구하는 함수. math 모듈에서 정수 제곱근을 구하는 isqrt 함수 가져오기
# 
# def solution(n):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 자연수 n을 입력받는 함수
#     x = isqrt(n)  # isqrt는 내림한 정수 제곱근. =는 값 저장. n의 제곱근에서 소수 부분을 버린 정수 구하기
#     if x * x == n:  # if는 조건이 참일 때 실행. ==는 같음 비교. x의 제곱이 n과 같으면 완전제곱수
#         return (x + 1) ** 2  # return은 결과를 돌려주고 함수 종료. **는 거듭제곱. 제곱근에 1을 더한 뒤 제곱하여 반환
#     return -1  # return은 결과를 돌려주고 함수 종료. 완전제곱수가 아니라면 -1 반환

# 풀이 요약
# isqrt는 n의 제곱근을 내림한 정수를 돌려준다. 그 수의 제곱이 n과 같을 때만 완전제곱수이므로 다음 정수의 제곱을 반환한다. 그렇지 않으면 -1이다. 실수 제곱근의 반올림에 의존하지 않는다.
# 정수 제곱근을 한 번 계산한다. 내부 비용은 정수 비트 수에 따르며 문제의 고정 정수 범위에서 보조 공간 O(1).
```

## 확인한 범위

2026-10-16 02:52:37의 Python3 제출 내역에서 정답 100/100을 확인했다. 원본은 그대로 보관했다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
