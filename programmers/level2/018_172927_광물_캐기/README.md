# 광물 캐기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/172927) · Level 2 · Python3

곡괭이별 피로도를 고려해 주어진 광물을 순서대로 캐는 최소 피로도를 구합니다.

## 조건과 입출력

입력 매개변수: `picks, minerals`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과입니다.

- 0 ≤ dia, iron, stone ≤ 5
- 곡괭이는 최소 1개 이상 가지고 있습니다.
- 5 ≤ minerals의 길이 ≤ 50

## 풀이를 따라가기

광물을 다섯 개씩 묶고 각 곡괭이로 묶음을 캘 때 비용을 미리 구합니다. 묶음 위치와 남은 세 곡괭이 수를 상태로 메모이제이션합니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
from functools import lru_cache

def solution(picks, minerals):
    fatigue = {'diamond': (1, 5, 25), 'iron': (1, 1, 5), 'stone': (1, 1, 1)}
    blocks = []
    # 곡괭이 하나가 처리하는 최대 다섯 광물을 묶는다.
    for start in range(0, len(minerals), 5):
        chunk = minerals[start:start + 5]
        blocks.append(tuple(sum(fatigue[name][pick] for name in chunk) for pick in range(3)))
    # 같은 위치와 남은 곡괭이 상태의 결과를 재사용한다.
    @lru_cache(None)
    def dfs(index, remaining):
        if index == len(blocks) or sum(remaining) == 0:
            return 0
        best = float('inf')
        for pick, count in enumerate(remaining):
            if count > 0:
                next_remaining = list(remaining)
                next_remaining[pick] -= 1
                # 현재 묶음 비용과 이후 최솟값을 합한다.
                cost = blocks[index][pick] + dfs(index + 1, tuple(next_remaining))
                best = min(best, cost)
        return best
    return dfs(0, tuple(picks))
```

## 정답이 되는 이유

곡괭이를 하나 고르면 최대 다섯 광물을 연속으로 캐므로 묶음 경계에서만 다음 선택이 생깁니다. 같은 위치·잔여 곡괭이의 이후 최솟값은 이전 선택과 무관합니다.

시간 O(B(p0+1)(p1+1)(p2+1)), 공간 같은 차수 / Time and space O(B(p0+1)(p1+1)(p2+1)); B=묶음 수 / block count

주의할 점: 곡괭이가 모자라면 뒤쪽 광물은 캐지 않습니다. 마지막 묶음은 다섯 개보다 작을 수 있습니다.

## 다른 방법: 어려운 묶음부터 좋은 곡괭이 배정

```python
def solution(picks,minerals):
    usable = minerals[:sum(picks)*5]
    blocks=[]
    for i in range(0,len(usable),5):
        block=usable[i:i+5]
        d,f,s=(block.count(name) for name in ('diamond','iron','stone'))
        blocks.append((d,f,s))
    blocks.sort(reverse=True)
    left=list(picks)
    answer=0
    for d,f,s in blocks:
        pick=next(i for i,count in enumerate(left) if count)
        left[pick]-=1
        # 다이아 수, 철 수가 큰 묶음부터 배정하면 좋은 곡괭이의 절감 효과가 크다.
        answer += (d+f+s,5*d+f+s,25*d+5*f+s)[pick]
    return answer
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 광물을 다섯 개씩 묶고 각 곡괭이로 묶음을 캘 때 비용을 미리 구합니다. 묶음 위치와 남은 세 곡괭이 수를 상태로 메모이제이션합니다. | 어려운 묶음부터 좋은 곡괭이 배정 |
| 비용 | 시간 O(B(p0+1)(p1+1)(p2+1)), 공간 같은 차수 / Time and space O(B(p0+1)(p1+1)(p2+1)); B=묶음 수 / block count | 시간 O(N+B log B), 공간 O(B) / Time O(N+B log B), space O(B) |

## 검증

공식 예제 2개와 생성 입력 80개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Minimize fatigue while mining minerals in order with the available pickaxes.

### Conditions and input/output

Input arguments: `picks, minerals`. The return value is an integer satisfying the task described below.

- 0 ≤ each pick count ≤ 5; at least one pick; 5 ≤ len(minerals) ≤ 50
- a pick mines at most 5 consecutive minerals; diamond/iron/stone types

### Approach

Group minerals into blocks of five and precompute each pick’s block cost. Memoize by block index and the remaining counts of all three picks.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

A chosen pick mines the next five minerals or the final partial block. Future optimal cost depends only on the block index and remaining picks.

시간 O(B(p0+1)(p1+1)(p2+1)), 공간 같은 차수 / Time and space O(B(p0+1)(p1+1)(p2+1)); B=묶음 수 / block count

Boundary cases: Stop when no picks remain. The last mineral block may contain fewer than five items.

### Alternative: Greedy assignment of better picks to harder blocks

시간 O(N+B log B), 공간 O(B) / Time O(N+B log B), space O(B)

### Verification

Local checks covered 2 official examples and 80 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 광물 캐기](https://school.programmers.co.kr/learn/courses/30/lessons/172927) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
