# 요격 시스템

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/181188) · Level 2 · Python3

열린 구간으로 표현한 표적들을 모두 관통하는 최소 요격 수를 구합니다.

## 조건과 입출력

입력 매개변수: `targets`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과입니다.

- 1 ≤ targets의 길이 ≤ 500,000
- 0 ≤ s < e ≤ 100,000,000

## 풀이를 따라가기

끝점이 빠른 순서로 정렬합니다. 아직 맞지 않은 구간을 만나면 그 끝점 바로 왼쪽에서 요격한다고 생각하고 끝점을 경계로 저장합니다. 다음 시작점이 경계 이상이면 새 요격이 필요합니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(targets):
    # 가장 먼저 끝나는 아직 미처리 구간부터 맞힌다.
    targets.sort(key=lambda target: target[1])
    answer = 0
    end = -1
    for start, stop in targets:
        # 끝점은 제외되므로 시작이 이전 끝점과 같아도 새 요격이 필요하다.
        if start >= end:
            answer += 1
            end = stop
    return answer
```

## 정답이 되는 이유

가장 먼저 끝나는 구간은 어떤 해에서도 한 번 맞혀야 합니다. 그 안의 요격점을 끝점 쪽으로 미뤄도 이후 끝나는 구간을 덜 맞히지 않으므로 탐욕 선택이 안전합니다.

시간 O(N log N), 추가 공간 O(N) 이하 / Time O(N log N), additional space at most O(N)

주의할 점: 구간 끝은 포함하지 않습니다. 실제로 end 위치를 쏘는 것이 아니라 end 바로 왼쪽이라는 의미입니다.

## 다른 방법: 시작점 정렬 + 교집합 유지

```python
def solution(targets):
    end = None
    answer = 0
    for start, stop in sorted(targets):
        if end is None or start >= end:
            answer += 1
            end = stop
        else:
            end = min(end,stop)
    return answer
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 끝점이 빠른 순서로 정렬합니다. 아직 맞지 않은 구간을 만나면 그 끝점 바로 왼쪽에서 요격한다고 생각하고 끝점을 경계로 저장합니다. 다음 시작점이 경계 이상이면 새 요격이 필요합니다. | 시작점 정렬 + 교집합 유지 |
| 비용 | 시간 O(N log N), 추가 공간 O(N) 이하 / Time O(N log N), additional space at most O(N) | 시간 O(N log N), 공간 O(N) / Time O(N log N), space O(N) |

## 검증

공식 예제 1개와 생성 입력 70개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다. 제한 상한에 해당하는 크기·수치의 경계 검사도 저장된 테스트에 포함했습니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Find the fewest intercept positions piercing every open target interval.

### Conditions and input/output

Input arguments: `targets`. The return value is an integer satisfying the task described below.

- 1 ≤ len(targets) ≤ 500000; 0 ≤ start < end ≤ 100000000
- target intervals are open: (start,end)

### Approach

Sort by ending position. For each uncovered interval, conceptually intercept just before its end and store that boundary. A following start at or beyond the boundary needs a new shot.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Every solution must hit the earliest-ending uncovered interval. Moving its shot toward that end cannot lose any later-ending interval that was also hit.

시간 O(N log N), 추가 공간 O(N) 이하 / Time O(N log N), additional space at most O(N)

Boundary cases: Endpoints are excluded. The stored end represents a shot just before end, not at end itself.

### Alternative: Sort by starts and maintain the common intersection

시간 O(N log N), 공간 O(N) / Time O(N log N), space O(N)

### Verification

Local checks covered 1 official examples and 70 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases. Saved tests also include a size or numeric boundary at the stated upper limit.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 요격 시스템](https://school.programmers.co.kr/learn/courses/30/lessons/181188) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
