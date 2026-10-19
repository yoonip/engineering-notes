# 양궁대회

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/92342) · Level 2 · Python3

가장 큰 점수 차이로 양궁에서 이기는 화살 배분을 찾고 동률이면 낮은 점수를 우선한다.

## 조건과 입출력

입력 매개변수: `n, info`. 반환값은 수치 배열이며 아래 풀이의 조건을 만족하는 결과다.

- 1 ≤ n ≤ 10
- 0 ≤ info의 원소 ≤ n
- 0 ≤ return할 정수 배열의 원소 ≤ n

## 풀이를 따라가기

10점부터 1점까지 각 점수를 이길지 포기할지 비트마스크로 정한다. 이기는 점수에는 상대보다 한 발만 더 쏘고 나머지는 0점에 둔다. 점수 차이와 뒤집은 배분을 함께 비교한다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(n, info):
    # 뒤집은 배열로 낮은 점수 화살부터 동률을 비교한다.
    best_key = (0, [])
    answer = [-1]
    # 각 득점 과녁을 이길지 포기할지 선택한다.
    for mask in range(1 << 10):
        shots = [0] * 11
        remaining = n
        for index in range(10):
            if mask & (1 << index):
                shots[index] = info[index] + 1
                remaining -= shots[index]
        if remaining < 0:
            continue
        # 득점에 도움이 되지 않는 남은 화살은 0점에 몰아 동률 우선순위를 높인다.
        shots[10] = remaining
        difference = 0
        for index in range(10):
            if shots[index] > info[index]:
                difference += 10 - index
            elif info[index] > 0:
                difference -= 10 - index
        key = (difference, shots[::-1])
        if difference > 0 and key > best_key:
            best_key, answer = key, shots
    return answer
```

## 왜 맞는가

점수를 얻으려면 상대보다 한 발 많으면 충분하고 그 이상은 점수 이득이 없다. 남은 화살을 0점에 두면 점수 차이를 보존하면서 낮은 점수 우선 조건을 만족한다.

시간 O(2^10·11), 공간 O(11) / Time O(2^10·11), space O(11)

주의할 점: 화살 n발을 모두 써야 한다. 점수 차이가 0이면 승리가 아니므로 [-1]이다.

## 다른 방법: 모든 화살 분배 완전 탐색 · 작은 n

이 대안은 작은 입력에서 원리를 비교하는 검증용이다. 최대 제한에 제출할 기본 풀이와 구분한다.

```python
def solution(n,info):
    best=(0,[])
    answer=[-1]
    shots=[0]*11
    def assign(index,left):
        nonlocal best,answer
        if index==10:
            shots[index]=left
            difference=sum((10-i) if shots[i]>info[i] else -(10-i) if info[i]>0 else 0 for i in range(10))
            key=(difference,shots[::-1])
            if difference>0 and key>best: best,answer=key,shots[:]
            return
        for used in range(left+1):
            shots[index]=used
            assign(index+1,left-used)
    assign(0,n)
    return answer
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 10점부터 1점까지 각 점수를 이길지 포기할지 비트마스크로 정한다. 이기는 점수에는 상대보다 한 발만 더 쏘고 나머지는 0점에 둔다. 점수 차이와 뒤집은 배분을 함께 비교한다. | 모든 화살 분배 완전 탐색 · 작은 n |
| 비용 | 시간 O(2^10·11), 공간 O(11) / Time O(2^10·11), space O(11) | 시간 O(C(n+10,10)·11), 공간 O(11) / Time O(C(n+10,10)·11), space O(11) |

## 검증

공식 예제 4개와 생성 입력 25개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Find the winning arrow allocation with maximum score difference, preferring more low-score arrows on ties.

### Conditions and input/output

Input arguments: `n, info`. The return value is a numeric list satisfying the task described below.

- 1 ≤ n ≤ 10; len(info)=11; sum(info)=n
- a returned allocation must use all n arrows; ties prefer more arrows at lower scores

### Approach

Use a bitmask to win or concede each score from ten to one. Spend exactly one more arrow than the opponent on won scores and place leftovers at zero. Compare score difference and reversed allocation.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Extra arrows beyond a winning margin do not improve score. Putting leftovers at zero preserves the margin and optimizes the low-score tie break.

시간 O(2^10·11), 공간 O(11) / Time O(2^10·11), space O(11)

Boundary cases: Use all n arrows. A zero score difference is not a win and yields [-1].

### Alternative: Enumerate all arrow allocations for small n

This alternative is for understanding and checking small inputs; use the main implementation for the full constraints. 시간 O(C(n+10,10)·11), 공간 O(11) / Time O(C(n+10,10)·11), space O(11)

### Verification

Local checks covered 4 official examples and 25 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 양궁대회](https://school.programmers.co.kr/learn/courses/30/lessons/92342) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
