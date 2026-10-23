# 연속된 부분 수열의 합

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/178870) · Level 2 · Python3

합이 k인 연속 부분 수열 중 가장 짧고 가장 앞선 구간을 찾습니다.

## 조건과 입출력

입력 매개변수: `sequence, k`. 반환값은 수치 배열이며 아래 풀이의 조건을 만족하는 결과입니다.

- 5 ≤ sequence의 길이 ≤ 1,000,000
- 1 ≤ sequence의 원소 ≤ 1,000
- sequence는 비내림차순으로 정렬되어 있습니다.
- 5 ≤ k ≤ 1,000,000,000

## 풀이를 따라가기

오른쪽 포인터를 늘리며 합을 더합니다. 합이 k를 넘으면 왼쪽 값을 빼며 구간을 줄입니다. 합이 같을 때 길이가 더 짧은 경우만 답을 갱신합니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(sequence, k):
    left = total = 0
    answer = [0, len(sequence)]
    for right, value in enumerate(sequence):
        total += value
        # 양수 수열이므로 왼쪽을 빼야 큰 합을 줄일 수 있다.
        while total > k:
            total -= sequence[left]
            left += 1
        # 길이가 더 짧을 때만 바꿔 같은 길이의 앞선 시작점을 보존한다.
        if total == k and right - left < answer[1] - answer[0]:
            answer = [left, right]
    return answer
```

## 정답이 되는 이유

모든 값이 양수라 오른쪽을 늘리면 합이 증가하고 왼쪽을 빼면 감소합니다. 버린 왼쪽 끝은 이후 더 긴 구간만 만들므로 다시 볼 필요가 없습니다.

시간 O(N), 공간 O(1) / Time O(N), space O(1)

주의할 점: 동률 때 갱신하지 않아 먼저 찾은 시작점을 유지합니다. 음수가 있는 수열에는 이 투 포인터 근거를 그대로 적용할 수 없습니다.

## 다른 방법: 누적합과 해시 맵

```python
def solution(sequence,k):
    latest = {0:-1}
    prefix = 0
    answer = None
    for right,value in enumerate(sequence):
        prefix += value
        if prefix-k in latest:
            left = latest[prefix-k]+1
            key = (right-left,left,right)
            if answer is None or key < answer:
                answer = key
        latest[prefix] = right
    return [answer[1],answer[2]]
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 오른쪽 포인터를 늘리며 합을 더합니다. 합이 k를 넘으면 왼쪽 값을 빼며 구간을 줄입니다. 합이 같을 때 길이가 더 짧은 경우만 답을 갱신합니다. | 누적합과 해시 맵 |
| 비용 | 시간 O(N), 공간 O(1) / Time O(N), space O(1) | 평균 시간 O(N), 공간 O(N) / Expected time O(N), space O(N) |

## 검증

공식 예제 3개와 생성 입력 60개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다. 제한 상한에 해당하는 크기·수치의 경계 검사도 저장된 테스트에 포함했습니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Find the shortest contiguous subsequence summing to k, breaking ties by earliest start.

### Conditions and input/output

Input arguments: `sequence, k`. The return value is a numeric list satisfying the task described below.

- 5 ≤ len(sequence) ≤ 1000000; 1 ≤ sequence[i] ≤ 1000
- sequence is nondecreasing; 5 ≤ k ≤ 10^9; a matching interval exists

### Approach

Extend the right endpoint and add its value. While the sum exceeds k, remove values from the left. Update only for a strictly shorter matching interval.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

All values are positive: extending increases the sum and shrinking decreases it. A discarded left endpoint cannot later yield a better interval.

시간 O(N), 공간 O(1) / Time O(N), space O(1)

Boundary cases: Keeping equal-length ties preserves the earlier start. This two-pointer argument does not apply unchanged to negative values.

### Alternative: Prefix sums with a hash map

평균 시간 O(N), 공간 O(N) / Expected time O(N), space O(N)

### Verification

Local checks covered 3 official examples and 60 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases. Saved tests also include a size or numeric boundary at the stated upper limit.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 연속된 부분 수열의 합](https://school.programmers.co.kr/learn/courses/30/lessons/178870) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
