# 튜플

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/64065) · Level 2 · Python3

원소가 하나씩 늘어나는 집합 표현에서 원래 튜플의 순서를 복원합니다.

## 조건과 입출력

입력 매개변수: `s`. 반환값은 수치 배열이며 아래 풀이의 조건을 만족하는 결과입니다.

- s의 길이는 5 이상 1,000,000 이하입니다.
- s가 표현하는 튜플의 원소는 1 이상 100,000 이하인 자연수입니다.
- return 하는 배열의 길이가 1 이상 500 이하인 경우만 입력으로 주어집니다.

## 풀이를 따라가기

정규식으로 숫자 토큰을 추출하고 빈도를 셉니다. 가장 많이 나오는 숫자부터 나열합니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
from collections import Counter
from re import findall

def solution(s):
    # 앞선 튜플 원소일수록 더 많은 집합에 등장한다.
    counts = Counter(findall(r'\d+', s))
    return [int(value) for value, count in counts.most_common()]
```

## 정답이 되는 이유

첫 튜플 원소는 모든 집합에, 두 번째는 첫 집합을 제외한 모두에 나옵니다. 따라서 빈도가 엄격히 감소하는 순서가 원래 튜플 순서입니다.

시간 O(L+U log U), 공간 O(L+U) / Time O(L+U log U), space O(L+U)

주의할 점: 집합 표현의 나열 순서는 임의입니다. 문자열 정렬이 아니라 출현 빈도 또는 집합 크기 순서로 복원합니다.

## 다른 방법: 집합 크기순 정렬 후 차집합

```python
def solution(s):
    groups=[set(map(int,chunk.split(','))) for chunk in s[2:-2].split('},{')]
    groups.sort(key=len)
    seen=set()
    answer=[]
    for group in groups:
        fresh=group-seen
        answer.append(fresh.pop())
        seen=group
    return answer
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 정규식으로 숫자 토큰을 추출하고 빈도를 셉니다. 가장 많이 나오는 숫자부터 나열합니다. | 집합 크기순 정렬 후 차집합 |
| 비용 | 시간 O(L+U log U), 공간 O(L+U) / Time O(L+U log U), space O(L+U) | 시간 O(L+U log U), 공간 O(L) / Time O(L+U log U), space O(L) |

## 검증

공식 예제 5개와 생성 입력 60개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Recover tuple order from nested set representations that add one element at a time.

### Conditions and input/output

Input arguments: `s`. The return value is a numeric list satisfying the task described below.

- 5 ≤ len(s) ≤ 1000000; element values 1 … 100000
- reconstructed tuple length 1 … 500; valid nested-set representation

### Approach

Extract numeric tokens and count frequencies. Return numbers from most frequent to least frequent.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

The first tuple element appears in every set, the second in all but the smallest, and so on. Strictly decreasing frequencies recover the tuple order.

시간 O(L+U log U), 공간 O(L+U) / Time O(L+U log U), space O(L+U)

Boundary cases: The sets may appear in any order. Recover by frequency or set size, not lexicographic token order.

### Alternative: Sort sets by size and extract newly added elements

시간 O(L+U log U), 공간 O(L) / Time O(L+U log U), space O(L)

### Verification

Local checks covered 5 official examples and 60 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 튜플](https://school.programmers.co.kr/learn/courses/30/lessons/64065) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
