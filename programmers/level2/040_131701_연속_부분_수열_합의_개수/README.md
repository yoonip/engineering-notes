# 연속 부분 수열 합의 개수

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/131701) · Level 2 · Python3

원형 수열의 모든 비어 있지 않은 연속 구간 합 중 서로 다른 값 수를 셉니다.

## 조건과 입출력

입력 매개변수: `elements`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과입니다.

- 3 ≤ elements의 길이 ≤ 1,000
- 1 ≤ elements의 원소 ≤ 1,000

## 풀이를 따라가기

수열을 두 번 이어 원형 경계를 직선으로 폅니다. 각 시작점에서 길이 1부터 n까지 누적합을 늘려 집합에 넣습니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(elements):
    n = len(elements)
    # 두 번 이어 붙이면 원형 경계를 넘는 구간도 그대로 읽을 수 있다.
    doubled = elements * 2
    sums = set()
    for start in range(n):
        total = 0
        # 시작마다 길이 1부터 전체 길이까지의 합을 모은다.
        for end in range(start, start + n):
            total += doubled[end]
            sums.add(total)
    return len(sums)
```

## 정답이 되는 이유

모든 원형 연속 구간은 시작점 n가지와 길이 n가지 중 하나입니다. 두 번 이어 붙이면 이 구간들을 빠짐없이 만들고 집합은 같은 합을 하나로 합칩니다.

시간 O(N²), 공간 O(N²) / Time and worst-case space O(N²)

주의할 점: 길이가 n인 전체 합도 포함합니다. 시작점이 달라도 합이 같으면 하나만 셉니다.

## 다른 방법: 길이별 슬라이딩 윈도

```python
def solution(elements):
    n=len(elements)
    totals=set()
    for length in range(1,n+1):
        current=sum(elements[:length])
        totals.add(current)
        for start in range(1,n):
            current-=elements[start-1]
            current+=elements[(start+length-1)%n]
            totals.add(current)
    return len(totals)
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 수열을 두 번 이어 원형 경계를 직선으로 폅니다. 각 시작점에서 길이 1부터 n까지 누적합을 늘려 집합에 넣습니다. | 길이별 슬라이딩 윈도 |
| 비용 | 시간 O(N²), 공간 O(N²) / Time and worst-case space O(N²) | 시간 O(N²), 공간 O(N²) / Time and worst-case space O(N²) |

## 검증

공식 예제 1개와 생성 입력 60개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Count distinct sums of all nonempty contiguous segments in a circular sequence.

### Conditions and input/output

Input arguments: `elements`. The return value is an integer satisfying the task described below.

- 3 ≤ len(elements) ≤ 1000; 1 ≤ elements[i] ≤ 1000

### Approach

Duplicate the sequence to linearize wraparound. For each start, accumulate lengths one through n into a set.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Every circular segment is determined by one of n starts and n lengths. Duplication represents all of them; the set deduplicates equal sums.

시간 O(N²), 공간 O(N²) / Time and worst-case space O(N²)

Boundary cases: Include length-n segments. Equal sums count once even when starts differ.

### Alternative: Slide a window separately for each length

시간 O(N²), 공간 O(N²) / Time and worst-case space O(N²)

### Verification

Local checks covered 1 official examples and 60 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 연속 부분 수열 합의 개수](https://school.programmers.co.kr/learn/courses/30/lessons/131701) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
