# 디펜스 게임

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/142085) · Level 2 · Python3

병사와 무적권을 최적으로 사용해 막을 수 있는 최대 라운드 수를 구한다.

## 조건과 입출력

입력 매개변수: `n, k, enemy`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과다.

- 1 ≤ n ≤ 1,000,000,000
- 1 ≤ k ≤ 500,000
- 1 ≤ enemy의 길이 ≤ 1,000,000
- 1 ≤ enemy[i] ≤ 1,000,000

## 풀이를 따라가기

현재까지 가장 큰 k개 적을 무적권 대상으로 최소 힙에 남긴다. 새 적을 넣고 k개를 넘으면 가장 작은 적을 꺼내 병사로 막는다. 병사가 음수가 되면 그 라운드는 불가능하다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
from heapq import heappush, heappop

def solution(n, k, enemy):
    shielded = []
    for index, count in enumerate(enemy):
        # 현재까지 가장 큰 k개 공격에 무적권을 배정한다.
        heappush(shielded, count)
        if len(shielded) > k:
            # k개를 넘으면 가장 작은 공격을 병사로 막는 편이 유리하다.
            n -= heappop(shielded)
        if n < 0:
            return index
    return len(enemy)
```

## 왜 맞는가

어떤 접두 구간에서든 무적권을 가장 큰 k개에 쓰는 것이 병사 비용을 최소화한다. 작은 적에 쓴 무적권을 큰 적과 바꾸는 교환 논증으로 확인할 수 있다.

시간 O(N log(k+1)), 공간 O(min(N,k+1)) / Time O(N log(k+1)), space O(min(N,k+1))

주의할 점: 적 수를 정렬하면 라운드 순서를 잃는다. 무적권보다 라운드가 적으면 모두 통과할 수 있다.

## 다른 방법: 접두 구간 정렬을 이용한 통과 라운드 이진 탐색

기본 풀이와 같은 결과를 구하되 중간 상태와 계산 방식이 다르다.

```python
def solution(n,k,enemy):
    def possible(count):
        ordered=sorted(enemy[:count])
        return sum(ordered[:max(0,count-k)])<=n
    low,high=0,len(enemy)
    while low<high:
        mid=(low+high+1)//2
        if possible(mid): low=mid
        else: high=mid-1
    return low
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 현재까지 가장 큰 k개 적을 무적권 대상으로 최소 힙에 남긴다. 새 적을 넣고 k개를 넘으면 가장 작은 적을 꺼내 병사로 막는다. 병사가 음수가 되면 그 라운드는 불가능하다. | 접두 구간 정렬을 이용한 통과 라운드 이진 탐색 |
| 비용 | 시간 O(N log(k+1)), 공간 O(min(N,k+1)) / Time O(N log(k+1)), space O(min(N,k+1)) | 시간 O(N(log N)^2), 공간 O(N) / Time O(N(log N)^2), space O(N) |

## 검증

공식 예제 2개와 생성 입력 80개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다. 제한 상한에 해당하는 크기·수치의 경계 검사도 저장된 테스트에 포함했다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Maximize survived rounds by optimally assigning soldiers and invincibility uses.

### Conditions and input/output

Input arguments: `n, k, enemy`. The return value is an integer satisfying the task described below.

- 1 ≤ n ≤ 10^9; 1 ≤ k ≤ 500000
- 1 ≤ len(enemy) ≤ 1000000; 1 ≤ enemy[i] ≤ 1000000

### Approach

Keep the largest k attacks seen so far in a min-heap. Insert each attack; if the heap exceeds k, pay soldiers for its smallest entry. A negative balance marks failure.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

For any prefix, shielding its largest k attacks minimizes soldier cost. Swapping a shield from a smaller attack to a larger one never increases that cost.

시간 O(N log(k+1)), 공간 O(min(N,k+1)) / Time O(N log(k+1)), space O(min(N,k+1))

Boundary cases: Sorting the entire enemy list destroys round order. If there are at most k rounds, all can be shielded.

### Alternative: Binary-search survived prefixes using sorted attack costs

It computes the same result using different intermediate states or evaluation steps. 시간 O(N(log N)^2), 공간 O(N) / Time O(N(log N)^2), space O(N)

The main approach follows the steps described above. The alternative uses binary-search survived prefixes using sorted attack costs; compare its intermediate state and cost with the main implementation before choosing it.

### Verification

Local checks covered 2 official examples and 80 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases. Saved tests also include a size or numeric boundary at the stated upper limit.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 디펜스 게임](https://school.programmers.co.kr/learn/courses/30/lessons/142085) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
