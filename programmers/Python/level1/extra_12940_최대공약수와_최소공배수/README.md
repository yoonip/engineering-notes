# 최대공약수와 최소공배수

[Level 1 목록 / Level 1 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12940) · Level 1 · Python3

유형: 정수론 · 최대공약수·최소공배수

## 풀이 원리

gcd가 두 수의 최대공약수 g를 구합니다. 두 수의 곱은 최대공약수×최소공배수이므로 n×m/g가 최소공배수입니다. 나누어떨어지는 정수 계산에 //를 씁니다.

입력 정수 범위에서 gcd의 나눗셈 횟수 O(log min(n,m)), 보조 공간 O(1).

## 공식 예제

입력 인수: `[3, 12]`

반환값: `[3, 12]`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
from math import gcd

def solution(n, m):
    g = gcd(n, m)
    l = n * m // g
    return [g, l]

# 전체 코드 줄별 설명
# from math import gcd  # from math import는 math 모듈에서 이름을 가져옴. gcd는 최대공약수를 구하는 함수. math 모듈에서 최대공약수를 구하는 gcd 함수를 가져옴
# 
# def solution(n, m):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 두 자연수 n과 m을 입력받는 함수
#     g = gcd(n, m)  # gcd는 최대공약수. =는 값 저장. gcd()로 n과 m의 최대공약수를 계산
#     l = n * m // g  # //는 내림한 정수 몫. =는 값 저장. 두 수를 곱한 뒤 최대공약수로 나누어 최소공배수 계산
#     return [g, l]  # return은 결과를 돌려주고 함수 종료. []는 리스트. 최대공약수와 최소공배수를 리스트로 반환

# 풀이 요약
# gcd가 두 수의 최대공약수 g를 구한다. 두 수의 곱은 최대공약수×최소공배수이므로 n×m/g가 최소공배수다. 나누어떨어지는 정수 계산에 //를 쓴다.
# 입력 정수 범위에서 gcd의 나눗셈 횟수 O(log min(n,m)), 보조 공간 O(1).
```

## 확인한 범위

2026-10-16 02:37:50의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
