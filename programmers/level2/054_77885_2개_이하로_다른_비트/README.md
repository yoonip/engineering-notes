# 2개 이하로 다른 비트

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/77885) · Level 2 · Python3

각 수보다 크고 이진 표현이 두 비트 이하로 다른 가장 작은 수를 구한다.

## 조건과 입출력

입력 매개변수: `numbers`. 반환값은 수치 배열이며 아래 풀이의 조건을 만족하는 결과다.

- 1 ≤ numbers의 길이 ≤ 100,000
- 0 ≤ numbers의 모든 수 ≤ 10^15

## 풀이를 따라가기

가장 낮은 0비트 위치를 (~number)&(number+1)로 구한다. 그 비트를 켜고 바로 아래 비트를 끄는 값을 계산한다. 짝수이면 가장 낮은 비트만 0→1로 바뀐다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(numbers):
    answer = []
    for number in numbers:
        # 가장 오른쪽 0비트만 켜진 값을 만든다.
        zero = (~number) & (number + 1)
        # 그 0을 1로, 바로 아래 1을 0으로 바꿔 증가량을 최소화한다.
        answer.append(number + zero - (zero >> 1))
    return answer
```

## 왜 맞는가

더 큰 수로 바꾸려면 어떤 0비트를 1로 해야 한다. 가장 낮은 0을 바꾸는 것이 증가량을 최소화하고, 두 번째 변화로 그 아래 가장 큰 1을 끄면 증가량이 더 줄어든다.

워드 모델 시간 O(N), 출력 공간 O(N); 큰 정수 비트 비용 O(log V) / O(N) word operations and output space; big-integer bit cost O(log V)

주의할 점: 전부 1인 이진수는 앞에 0이 있다고 생각한다. XOR 비트 수가 1개나 2개인 경우 모두 허용된다.

## 다른 방법: 이진 문자열에서 가장 오른쪽 0 찾기

기본 풀이와 같은 결과를 구하되 중간 상태와 계산 방식이 다르다.

```python
def solution(numbers):
    answer=[]
    for number in numbers:
        bits=list('0'+bin(number)[2:])
        index=''.join(bits).rfind('0')
        bits[index]='1'
        if index+1<len(bits): bits[index+1]='0'
        answer.append(int(''.join(bits),2))
    return answer
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 가장 낮은 0비트 위치를 (~number)&(number+1)로 구한다. 그 비트를 켜고 바로 아래 비트를 끄는 값을 계산한다. 짝수이면 가장 낮은 비트만 0→1로 바뀐다. | 이진 문자열에서 가장 오른쪽 0 찾기 |
| 비용 | 워드 모델 시간 O(N), 출력 공간 O(N); 큰 정수 비트 비용 O(log V) / O(N) word operations and output space; big-integer bit cost O(log V) | 시간 O(N log V), 공간 O(log V)+출력 / Time O(N log V), space O(log V) plus output |

## 검증

공식 예제 1개와 생성 입력 31개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

For each integer, find the smallest larger integer differing in at most two bits.

### Conditions and input/output

Input arguments: `numbers`. The return value is a numeric list satisfying the task described below.

- 1 ≤ len(numbers) ≤ 100000; 0 ≤ number ≤ 10^15

### Approach

Find the lowest zero bit with (~number)&(number+1). Set it and clear the bit immediately below; for even numbers only the lowest bit changes.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Any larger value must set a zero bit. Choosing the lowest such bit minimizes the increase, and clearing the largest lower one further minimizes it within two changes.

워드 모델 시간 O(N), 출력 공간 O(N); 큰 정수 비트 비용 O(log V) / O(N) word operations and output space; big-integer bit cost O(log V)

Boundary cases: Treat an all-one bit string as having a leading zero. Both one-bit and two-bit differences qualify.

### Alternative: Locate the rightmost zero in a binary string

It computes the same result using different intermediate states or evaluation steps. 시간 O(N log V), 공간 O(log V)+출력 / Time O(N log V), space O(log V) plus output

The main approach follows the steps described above. The alternative uses locate the rightmost zero in a binary string; compare its intermediate state and cost with the main implementation before choosing it.

### Verification

Local checks covered 1 official examples and 31 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 2개 이하로 다른 비트](https://school.programmers.co.kr/learn/courses/30/lessons/77885) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
