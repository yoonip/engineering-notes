# 순위 검색

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/72412) · Level 2 · Python3

네 조건의 일부가 생략될 수 있는 질의마다 점수 기준 이상인 지원자 수를 센다.

## 조건과 입출력

입력 매개변수: `info, query`. 반환값은 수치 배열이며 아래 풀이의 조건을 만족하는 결과다.

- info 배열의 크기는 1 이상 50,000 이하입니다.
- 점수는 코딩테스트 점수를 의미하며, 1 이상 100,000 이하인 자연수입니다.
- query 배열의 크기는 1 이상 100,000 이하입니다.
- X는 코딩테스트 점수를 의미하며 조건을 만족하는 사람 중 X점 이상 받은 사람은 모두 몇 명인 지를 의미합니다.
- 예를 들면, "cpp and - and senior and pizza 500"은 "cpp로 코딩테스트를 봤으며, 경력은 senior 이면서 소울푸드로 pizza를 선택한 지원자 중 코딩테스트 점수를 500점 이상 받은 사람은 모두 몇 명인가?"를 의미합니다.

## 풀이를 따라가기

지원자마다 네 조건을 실제 값 또는 -로 바꾼 16개 키에 점수를 저장한다. 키별 점수를 정렬한다. 질의 키를 찾아 bisect_left로 기준 미만 개수를 빼면 된다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
from collections import defaultdict
from itertools import product
from bisect import bisect_left

def solution(info, query):
    table = defaultdict(list)
    for record in info:
        parts = record.split()
        score = int(parts.pop())
        # 네 조건의 유지·무시 조합 16개를 미리 준비한다.
        for key in product(*[(value, '-') for value in parts]):
            table[key].append(score)
    for scores in table.values():
        scores.sort()
    answer = []
    for request in query:
        parts = request.replace(' and ', ' ').split()
        minimum = int(parts.pop())
        scores = table.get(tuple(parts), [])
        # 기준 이상 점수는 정렬된 목록의 뒤쪽 연속 구간이다.
        answer.append(len(scores) - bisect_left(scores, minimum))
    return answer
```

## 왜 맞는가

한 지원자는 자신을 포함하는 모든 조건 조합의 키에 정확히 한 번 들어간다. 정렬된 점수에서 lower_bound는 기준 이상 구간의 시작을 주므로 개수가 정확하다.

시간 O(16N log N+Q log N), 공간 O(16N+Q) / Time O(16N log N+Q log N), space O(16N+Q)

주의할 점: 점수는 기준 이상이다. -는 해당 조건을 무시한다는 의미이며 실제 값과 문자 연결 충돌이 없게 튜플 키를 쓴다.

## 다른 방법: 질의마다 전체 지원자 필터 · 작은 입력

이 대안은 작은 입력에서 원리를 비교하는 검증용이다. 최대 제한에 제출할 기본 풀이와 구분한다.

```python
def solution(info,query):
    applicants=[record.split() for record in info]
    answer=[]
    for text in query:
        parts=text.replace(' and ',' ').split()
        total=0
        for row in applicants:
            if all(wanted=='-' or wanted==actual for wanted,actual in zip(parts[:4],row[:4])) and int(row[4])>=int(parts[4]): total+=1
        answer.append(total)
    return answer
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 지원자마다 네 조건을 실제 값 또는 -로 바꾼 16개 키에 점수를 저장한다. 키별 점수를 정렬한다. 질의 키를 찾아 bisect_left로 기준 미만 개수를 빼면 된다. | 질의마다 전체 지원자 필터 · 작은 입력 |
| 비용 | 시간 O(16N log N+Q log N), 공간 O(16N+Q) / Time O(16N log N+Q log N), space O(16N+Q) | 시간 O(NQ), 공간 O(N+Q) / Time O(NQ), space O(N+Q) |

## 검증

공식 예제 1개와 생성 입력 40개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Count applicants meeting wildcard attribute filters and a minimum score for each query.

### Conditions and input/output

Input arguments: `info, query`. The return value is a numeric list satisfying the task described below.

- 1 ≤ len(info) ≤ 50000; 1 ≤ len(query) ≤ 100000
- score and minimum score: 1 … 100000; four attributes; '-' is a wildcard

### Approach

Store each applicant’s score under all sixteen combinations of actual attributes and wildcards. Sort each score list, then use bisect_left to locate qualifying query scores.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Each applicant appears exactly once under every filter combination that includes them. Lower_bound identifies the start of the qualifying sorted suffix.

시간 O(16N log N+Q log N), 공간 O(16N+Q) / Time O(16N log N+Q log N), space O(16N+Q)

Boundary cases: Scores equal to the threshold qualify. A wildcard ignores that attribute; tuple keys avoid ambiguous concatenations.

### Alternative: Full applicant scan per query for small inputs

This alternative is for understanding and checking small inputs; use the main implementation for the full constraints. 시간 O(NQ), 공간 O(N+Q) / Time O(NQ), space O(N+Q)

### Verification

Local checks covered 1 official examples and 40 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 순위 검색](https://school.programmers.co.kr/learn/courses/30/lessons/72412) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
