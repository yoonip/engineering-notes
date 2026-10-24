# 쿼리의 모음의 개수 — Python 재풀이

[문제 원문](<https://school.programmers.co.kr/learn/courses/30/lessons/87394>) · [재풀이 목록](<../README.md>)

정답률 1%와 풀이 인원 105명은 이번 목록 확인 시점의 값입니다. 전체 10순위로 진행했습니다.

## 사이트 채점

사이트 채점 합계 100점과 이번 재풀이 이후의 Python3 정답 100점 제출 내역을 확인했습니다. 정답은 실제 1번째 제출이며, 총 1회 제출했습니다.

| 제출 | 결과 | 합계 점수 | 입력 코드 | 채점 기록 |
| --- | --- | ---: | --- | --- |
| 1 | 정답 | 100 | [코드](<solution.py>) | [채점 결과 발췌](<attempts/attempt1_grading.txt>) |

[채점·제출 내역 JSON](<grading.json>)에는 실제 제출 시각, 합계, 테스트별 결과와 시간, 메모리, 입력 SHA256 및 새 제출 내역을 기록합니다. 제출한 입력 파일은 원본 바이트를 보관하며, 화면에 넣을 때의 LF 정규화 해시를 별도 기록합니다.

## 로컬 검증

[제출 전 후보 검증 원본](<local_checks.json>)은 사이트 채점과 별도인 로컬 비교·성능 기록입니다. 로컬 검증에 기록한 코드 해시는 정답 제출 입력과 같습니다.

## 풀이 요약

목표 높이를 넘는 쿼리는 쓸 수 없음. 각 위치 i를 높이 a[i]인 쿼리가 한 번 이상 덮으면 목표 배열 완성.
구간의 최솟값 위치에서 필수 덮기 조건을 세고, 그 사이 더 높은 구간으로 나누기. 높이별 쿼리 종류는 서로 독립이라 지수생성함수를 곱함.
필수 위치를 못 덮는 사건을 포함배제로 계산. 선택한 미덮임 위치 사이 길이가 L이면 쓸 수 있는 부분구간은 L(L+1)/2개.
Python의 큰 정수 곱으로 다항식 곱을 계산. 계수를 80비트 간격으로 넣으면 가장 큰 중간 계수도 51²(mod−1)²보다 작아 다음 자리로 넘치지 않음.
음수 부호는 자리 분리 뒤에 적용. 음수 정수를 그대로 비트 묶음에 더하면 자리 빌림 때문에 다른 계수가 바뀌므로 피하기.
최종 q차 계수에 q!를 곱하면 순서를 구분한 쿼리 수. 큰 정수 연산을 제외한 Python 반복은 O(N²Q), 계수 저장은 O(NQ).

## 정답 제출 코드

실제 1번째 정답 제출 입력의 전체 내용입니다. 원본 파일의 줄바꿈 바이트는 그대로 두며, 아래 표시는 LF로 정규화합니다.

```python
from math import factorial

def solution(q, a):
    mod = 998244353
    width = 80
    mask = (1 << width) - 1
    degree_count = q + 1
    def pack(coefficients):
        value = 0
        for coefficient in reversed(coefficients):
            value = (value << width) | coefficient
        return value
    def reduce(value, sign=1):
        coefficients = []
        for _ in range(degree_count):
            coefficients.append(sign * (value & mask) % mod)
            value >>= width
        return pack(coefficients)
    inverse = [0, 1] + [0] * max(0, q - 1)
    for j in range(2, degree_count):
        inverse[j] = mod - (mod // j) * inverse[mod % j] % mod
    def exponential(kinds):
        coefficients = [1]
        for j in range(1, degree_count):
            coefficients.append(coefficients[-1] * kinds % mod * inverse[j] % mod)
        return pack(coefficients)
    n = len(a)
    gaps = [exponential(length * (length + 1) // 2) for length in range(n + 1)]
    product = 1
    unrestricted = 0
    stack = [(0, n - 1, 0)]
    while stack:
        left, right, floor = stack.pop()
        minimum = min(a[left:right + 1])
        length = right - left + 1
        unrestricted += (minimum - floor - 1) * length * (length + 1) // 2
        positions = [left - 1] + [i for i in range(left, right + 1) if a[i] == minimum] + [right + 1]
        paths = [1]
        for boundary in range(1, len(positions)):
            combined = 0
            for previous in range(boundary):
                gap = positions[boundary] - positions[previous] - 1
                combined += paths[previous] * gaps[gap]
            sign = 1 if boundary == len(positions) - 1 else -1
            paths.append(reduce(combined, sign))
        product = reduce(product * paths[-1])
        for first, last in zip(positions, positions[1:]):
            if first + 1 < last:
                stack.append((first + 1, last - 1, minimum))
    result = product * exponential(unrestricted)
    coefficient = (result >> (q * width)) & mask
    return coefficient % mod * factorial(q) % mod

# 전체 코드 줄별 설명
# from math import factorial  # 순서 있는 쿼리 수를 복원할 q! 계산
#
# def solution(q, a):  # q개의 최댓값 갱신으로 목표 배열을 만드는 방법 수 반환
#     mod = 998244353  # 모든 경우의 수에 사용할 소수 나머지
#     width = 80  # 다항식 계수 하나를 저장할 비트 간격
#     mask = (1 << width) - 1  # 한 계수만 꺼낼 때 쓸 비트 마스크
#     degree_count = q + 1  # 0차부터 q차까지만 저장
#     def pack(coefficients):  # 작은 계수 배열을 큰 정수 하나로 묶는 내부 함수
#         value = 0  # 아직 담긴 계수가 없는 상태
#         for coefficient in reversed(coefficients):  # 높은 차수부터 차례로 밀어 넣기
#             value = (value << width) | coefficient  # 80비트 공간을 비우고 다음 계수 저장
#         return value  # 정수 곱셈으로 다항식 곱을 계산할 표현
#     def reduce(value, sign=1):  # 잘린 다항식의 각 계수에 나머지와 부호 적용
#         coefficients = []  # q차 이하의 새 계수 목록
#         for _ in range(degree_count):  # 낮은 차수부터 하나씩 분리
#             coefficients.append(sign * (value & mask) % mod)  # 자리끼리 섞이지 않은 원래 계수에 모듈러 연산
#             value >>= width  # 처리한 계수 80비트를 버리고 다음 자리로 이동
#         return pack(coefficients)  # 나머지 범위의 계수들을 다시 정수로 묶기
#     inverse = [0, 1] + [0] * max(0, q - 1)  # 1부터 q까지 곱셈 역원을 담을 배열
#     for j in range(2, degree_count):  # 작은 수의 모듈러 역원을 순서대로 계산
#         inverse[j] = mod - (mod // j) * inverse[mod % j] % mod  # 앞서 구한 역원으로 현재 역원 계산
#     def exponential(kinds):  # kinds개 종류를 원하는 횟수만큼 쓰는 지수생성함수
#         coefficients = [1]  # 아무 쿼리도 고르지 않는 0차 계수는 1
#         for j in range(1, degree_count):  # kinds^j/j!를 q차까지 계산
#             coefficients.append(coefficients[-1] * kinds % mod * inverse[j] % mod)  # 이전 차수에 종류 수와 1/j를 곱하기
#         return pack(coefficients)  # 이후 곱셈을 위한 압축 정수
#     n = len(a)  # 목표 배열 길이
#     gaps = [exponential(length * (length + 1) // 2) for length in range(n + 1)]  # 빈 구간 길이별로 가능한 부분구간 쿼리의 생성함수
#     product = 1  # 지금까지의 독립된 높이 조건을 합친 생성함수
#     unrestricted = 0  # 필수 위치를 덮을 필요가 없는 쿼리 종류 수
#     stack = [(0, n - 1, 0)]  # 연속 구간과 부모의 최솟값 높이를 스택에 저장
#     while stack:  # 최솟값으로 갈라지는 구간들을 차례로 처리
#         left, right, floor = stack.pop()  # 이번 구간의 양끝과 이전 높이 경계
#         minimum = min(a[left:right + 1])  # 구간 전체를 넘지 않는 현재 필수 높이
#         length = right - left + 1  # 현재 구간 길이
#         unrestricted += (minimum - floor - 1) * length * (length + 1) // 2  # 빠진 높이들은 모든 부분구간에서 무제약으로 선택 가능
#         positions = [left - 1] + [i for i in range(left, right + 1) if a[i] == minimum] + [right + 1]  # 필수 위치들과 양쪽 가상 경계
#         paths = [1]  # 왼쪽 가상 경계까지의 포함배제 계수
#         for boundary in range(1, len(positions)):  # 다음 미덮임 위치 또는 마지막 가상 경계 선택
#             combined = 0  # 직전 경계별 생성함수 곱을 나머지 처리 전 합산
#             for previous in range(boundary):  # 직전에 골랐던 미덮임 위치 후보
#                 gap = positions[boundary] - positions[previous] - 1  # 두 경계 사이에서만 쿼리를 고를 수 있음
#                 combined += paths[previous] * gaps[gap]  # 압축 정수 곱으로 두 생성함수의 모든 차수 조합 합산
#             sign = 1 if boundary == len(positions) - 1 else -1  # 실제 미덮임 조건을 하나 고를 때만 포함배제 부호 반전
#             paths.append(reduce(combined, sign))  # 현재 경계까지의 계수를 q차로 자르고 저장
#         product = reduce(product * paths[-1])  # 이 높이의 필수 덮기 조건을 누적 생성함수에 곱하기
#         for first, last in zip(positions, positions[1:]):  # 최솟값 위치 사이의 더 높은 구간 확인
#             if first + 1 < last:  # 두 경계 사이에 실제 원소가 있는 경우
#                 stack.append((first + 1, last - 1, minimum))  # 더 높은 구간을 다음 작업으로 등록
#     result = product * exponential(unrestricted)  # 무제약 종류의 쿼리도 순서열에 섞기
#     coefficient = (result >> (q * width)) & mask  # 최종 곱의 q차 계수만 분리
#     return coefficient % mod * factorial(q) % mod  # q!로 순서를 복원하고 답의 나머지 반환

# 풀이 요약
# 목표 높이를 넘는 쿼리는 쓸 수 없음. 각 위치 i를 높이 a[i]인 쿼리가 한 번 이상 덮으면 목표 배열 완성.
# 구간의 최솟값 위치에서 필수 덮기 조건을 세고, 그 사이 더 높은 구간으로 나누기. 높이별 쿼리 종류는 서로 독립이라 지수생성함수를 곱함.
# 필수 위치를 못 덮는 사건을 포함배제로 계산. 선택한 미덮임 위치 사이 길이가 L이면 쓸 수 있는 부분구간은 L(L+1)/2개.
# Python의 큰 정수 곱으로 다항식 곱을 계산. 계수를 80비트 간격으로 넣으면 가장 큰 중간 계수도 51²(mod−1)²보다 작아 다음 자리로 넘치지 않음.
# 음수 부호는 자리 분리 뒤에 적용. 음수 정수를 그대로 비트 묶음에 더하면 자리 빌림 때문에 다른 계수가 바뀌므로 피하기.
# 최종 q차 계수에 q!를 곱하면 순서를 구분한 쿼리 수. 큰 정수 연산을 제외한 Python 반복은 O(N²Q), 계수 저장은 O(NQ).
```
