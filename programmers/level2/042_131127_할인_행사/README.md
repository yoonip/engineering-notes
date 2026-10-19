# 할인 행사

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/131127) · Level 2 · Python3

연속 10일의 할인 상품이 원하는 품목과 수량에 정확히 맞는 시작일 수를 센다.

## 조건과 입출력

입력 매개변수: `want, number, discount`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과다.

- 1 ≤ want의 길이 = number의 길이 ≤ 10
- 1 ≤ number의 원소 ≤ 10
- 10 ≤ discount의 길이 ≤ 100,000
- 1 ≤ want의 원소의 길이, discount의 원소의 길이 ≤ 12

## 풀이를 따라가기

원하는 품목을 빈도 사전으로 만든다. 각 시작일부터 10일을 Counter로 세고 두 사전이 같은지 비교한다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
from collections import Counter

def solution(want, number, discount):
    needed = dict(zip(want, number))
    answer = 0
    for start in range(len(discount) - 9):
        # 열흘 구간의 상품별 수량을 센다.
        current = Counter(discount[start:start + 10])
        # 원하는 종류와 수량이 모두 같아야 한다.
        if current == needed:
            answer += 1
    return answer
```

## 왜 맞는가

원하는 수량 합은 10이다. 10일 구간의 품목별 빈도가 같다는 조건은 원하는 수량을 전부 사고 다른 품목은 사지 않는다는 조건과 같다.

시간 O(10N), 공간 O(10+U) / Time O(10N), space O(10+U)

주의할 점: 열흘이 남지 않은 시작일은 제외한다. 종류만 같고 수량이 다른 구간은 인정하지 않는다.

## 다른 방법: 빠지는 상품과 들어오는 상품만 갱신

기본 풀이와 같은 결과를 구하되 중간 상태와 계산 방식이 다르다.

```python
from collections import Counter

def solution(want,number,discount):
    need=dict(zip(want,number))
    current=Counter(discount[:10])
    answer=int(all(current[name]==count for name,count in need.items()))
    for end in range(10,len(discount)):
        current[discount[end-10]]-=1
        current[discount[end]]+=1
        answer+=all(current[name]==count for name,count in need.items())
    return answer
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 원하는 품목을 빈도 사전으로 만든다. 각 시작일부터 10일을 Counter로 세고 두 사전이 같은지 비교한다. | 빠지는 상품과 들어오는 상품만 갱신 |
| 비용 | 시간 O(10N), 공간 O(10+U) / Time O(10N), space O(10+U) | 시간 O(NU), 공간 O(U+10) / Time O(NU), space O(U+10); U≤10 |

## 검증

공식 예제 2개와 생성 입력 60개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Count starting days whose ten consecutive discounted products exactly match the desired quantities.

### Conditions and input/output

Input arguments: `want, number, discount`. The return value is an integer satisfying the task described below.

- 1 ≤ len(want)=len(number) ≤ 10; 1 ≤ number[i] ≤ 10; sum(number)=10
- 10 ≤ len(discount) ≤ 100000; product-name lengths 1 … 12, lowercase letters

### Approach

Build a frequency dictionary of the wanted products. Count each ten-day window with Counter and compare dictionaries.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Wanted quantities sum to ten. Equality of ten-day frequencies means all requested quantities are present with no unwanted replacements.

시간 O(10N), 공간 O(10+U) / Time O(10N), space O(10+U)

Boundary cases: Skip starts with fewer than ten days remaining. Matching product names without matching quantities is insufficient.

### Alternative: Incremental sliding-window frequencies

It computes the same result using different intermediate states or evaluation steps. 시간 O(NU), 공간 O(U+10) / Time O(NU), space O(U+10); U≤10

The main approach follows the steps described above. The alternative uses incremental sliding-window frequencies; compare its intermediate state and cost with the main implementation before choosing it.

### Verification

Local checks covered 2 official examples and 60 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 할인 행사](https://school.programmers.co.kr/learn/courses/30/lessons/131127) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
