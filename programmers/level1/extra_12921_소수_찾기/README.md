# 소수 찾기

[공식 문제 / Problem](https://school.programmers.co.kr/learn/courses/30/lessons/12921) · Level 1 · Python3

유형: 정수론 · 에라토스테네스의 체

## 풀이 원리

처음에는 모두 소수 후보로 두고 0과 1을 제외합니다. 아직 소수인 수의 배수들을 지우면 합성수만 제거됩니다. number보다 작은 인수의 배수는 이미 처리했으므로 number²부터 시작하고, number²>n이면 끝냅니다.

입력 N: 시간 O(N log log N), 공간 O(N).

## 공식 예제

입력 인수: `[10]`

반환값: `4`

전체 공개 예제의 입력과 결과는 [examples.json](examples.json)에 있습니다.

## 코드와 줄별 설명

[코드 파일](solution.py) · [100점 제출 원본](submitted_original.py) · [제출 기록](grading.json)

```python
def solution(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = False
    is_prime[1] = False
    number = 2
    while number * number <= n:
        if is_prime[number]:
            for multiple in range(number * number, n + 1, number):
                is_prime[multiple] = False
        number += 1
    return sum(is_prime)

# 전체 코드 줄별 설명
# def solution(n):  # def는 함수 정의, () 안은 입력 매개변수, : 뒤 들여쓰기는 함수 본문. 1부터 n까지에 있는 소수의 개수를 반환하는 함수
#     is_prime = [True] * (n + 1)  # []는 리스트. =는 값 저장. True·False는 참·거짓. 0~n번 위치를 만들고, 우선 모두 소수 후보인 True로 표시
#     is_prime[0] = False  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. True·False는 참·거짓. 0은 소수가 아니므로 제외
#     is_prime[1] = False  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. True·False는 참·거짓. 1도 소수가 아니므로 제외
#     number = 2  # =는 값 저장. 가장 작은 소수인 2부터 확인 시작
#     while number * number <= n:  # while은 조건이 참인 동안 반복. <=는 이하 비교. number의 제곱이 n 이하인 동안 반복
#         if is_prime[number]:  # if는 조건이 참일 때 실행. []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. 현재 숫자가 아직 제외되지 않았다면 소수이므로
#             for multiple in range(number * number, n + 1, number):  # for·in은 원소를 차례로 꺼내는 반복문. range는 끝값 직전까지 정수 순서 생성. 제곱부터 n까지 배수를 확인
#                 is_prime[multiple] = False  # []는 0부터 시작하는 인덱스 접근, 음수는 뒤에서 셈. =는 값 저장. True·False는 참·거짓. 현재 소수의 배수는 소수가 아니므로 제외
#         number += 1  # +=는 더하거나 연결한 값을 저장. 다음 숫자를 확인하기 위해 1 증가. number = number + 1
#     return sum(is_prime)  # return은 결과를 돌려주고 함수 종료. sum은 원소 합. True는 1, False는 0으로 더해지므로 남아 있는 소수의 개수를 반환

# 풀이 요약
# 처음에는 모두 소수 후보로 두고 0과 1을 제외한다. 아직 소수인 수의 배수들을 지우면 합성수만 제거된다. number보다 작은 인수의 배수는 이미 처리했으므로 number²부터 시작하고, number²>n이면 끝낸다.
# 입력 N: 시간 O(N log log N), 공간 O(N).
```

## 확인한 범위

2026-10-16 02:10:49의 Python3 제출 내역에서 정답 100/100을 확인했습니다. 원본은 그대로 보관했습니다. 학습용 코드에서는 기존 설명 주석과 빈 줄을 정리했으며 실행 구문의 AST는 원본과 같습니다. 새 줄별 설명을 붙인 파일은 사이트에 다시 제출하지 않았습니다. 공개 예제 비교 결과는 [검증 기록](validation.json)에 있습니다.

## English

The accepted Python3 submission was read from the website history with a score of 100/100. [The original](submitted_original.py) is preserved. [The study file](solution.py) keeps the same executable AST, followed by an exact commented copy with Korean syntax and purpose notes. The Korean method section explains the approach and its costs. The annotated file was not resubmitted. [Public examples](examples.json) and [local validation](validation.json) record the checked inputs and outputs.
