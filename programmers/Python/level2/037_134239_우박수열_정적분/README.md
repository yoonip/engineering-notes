# 우박수열 정적분

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/134239) · Level 2 · Python3

우박수열 점들을 직선으로 잇는 그래프의 지정 구간 넓이를 계산합니다.

## 조건과 입출력

입력 매개변수: `k, ranges`. 반환값은 수치 배열이며 아래 풀이의 조건을 만족하는 결과입니다.

- 2 ≤ k ≤ 10,000
- 1 ≤ ranges의 길이 ≤ 10,000
- ranges의 원소는 [a, b] 형식이며 0 ≤ a < 200, -200 < b ≤ 0 입니다.

## 풀이를 따라가기

문제의 규칙으로 k가 1이 될 때까지 다음 수를 구합니다. 폭 1인 사다리꼴 넓이를 누적합니다. [a,b]의 오른쪽 끝은 전체 단계 수+b이므로 누적합 차이로 답합니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(k, ranges):
    prefix = [0.0]
    while k > 1:
        next_value = k // 2 if k % 2 == 0 else 3 * k + 1
        # 폭이 1인 사다리꼴의 넓이를 누적한다.
        prefix.append(prefix[-1] + (k + next_value) / 2)
        k = next_value
    n = len(prefix) - 1
    answer = []
    for start, offset in ranges:
        # 음수 끝점은 전체 단계 수를 기준으로 해석한다.
        end = n + offset
        answer.append(prefix[end] - prefix[start] if start <= end else -1.0)
    return answer
```

## 정답이 되는 이유

각 선분 아래 넓이는 양 끝 높이의 평균입니다. 겹치지 않는 단위 구간 넓이를 누적하면 임의 구간 넓이를 두 누적값의 차이로 정확히 얻습니다.

시간 O(L+Q), 공간 O(L) / Time O(L+Q), space O(L); L=해당 입력의 수열 길이 / sequence length for this input

주의할 점: 시작이 끝보다 크면 −1, 같으면 0입니다. 이 구현은 주어진 입력에서의 계산이며 콜라츠 추측의 일반 증명이 아닙니다.

## 다른 방법: 유리수 사다리꼴을 구간마다 직접 합산

```python
from fractions import Fraction

def solution(k,ranges):
    values=[k]
    while k>1:
        k=k//2 if k%2==0 else 3*k+1
        values.append(k)
    n=len(values)-1
    answer=[]
    for start,offset in ranges:
        end=n+offset
        area=sum((Fraction(values[i]+values[i+1],2) for i in range(start,end)),Fraction(0))
        answer.append(float(area) if start<=end else -1.0)
    return answer
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 문제의 규칙으로 k가 1이 될 때까지 다음 수를 구합니다. 폭 1인 사다리꼴 넓이를 누적합니다. [a,b]의 오른쪽 끝은 전체 단계 수+b이므로 누적합 차이로 답합니다. | 유리수 사다리꼴을 구간마다 직접 합산 |
| 비용 | 시간 O(L+Q), 공간 O(L) / Time O(L+Q), space O(L); L=해당 입력의 수열 길이 / sequence length for this input | 시간 O(LQ), 공간 O(L) / Time O(LQ), space O(L) |

## 검증

공식 예제 2개와 생성 입력 50개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Compute areas over specified ranges of the piecewise-linear hailstone-sequence graph.

### Conditions and input/output

Input arguments: `k, ranges`. The return value is a numeric list satisfying the task described below.

- 2 ≤ k ≤ 10000; 1 ≤ len(ranges) ≤ 10000
- ranges=[a,b]: 0 ≤ a < 200; −200 < b ≤ 0; area ≤ 2^27

### Approach

Generate the sequence until it reaches one, prefix-summing each unit-width trapezoid area. A query’s right endpoint is sequence_length+b; answer by subtracting prefixes.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Each segment’s area is the average of its endpoint heights. Disjoint unit intervals add, so prefix differences give exact requested areas.

시간 O(L+Q), 공간 O(L) / Time O(L+Q), space O(L); L=해당 입력의 수열 길이 / sequence length for this input

Boundary cases: Return −1 for reversed endpoints and zero for an empty-width range. Computing these inputs does not prove the Collatz conjecture in general.

### Alternative: Direct per-range summation with exact rational trapezoids

시간 O(LQ), 공간 O(L) / Time O(LQ), space O(L)

### Verification

Local checks covered 2 official examples and 50 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 우박수열 정적분](https://school.programmers.co.kr/learn/courses/30/lessons/134239) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
