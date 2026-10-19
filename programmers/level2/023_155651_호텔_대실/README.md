# 호텔 대실

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/155651) · Level 2 · Python3

각 대실 종료 후 청소 10분을 포함해 필요한 최소 객실 수를 구한다.

## 조건과 입출력

입력 매개변수: `book_time`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과다.

- 1 ≤ book_time의 길이 ≤ 1,000

## 풀이를 따라가기

시작 시각에 +1, 종료+10분에 −1을 기록한다. 분 단위 변화량을 누적해 동시에 점유한 객실의 최댓값을 구한다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(book_time):
    changes = [0] * 1450
    for start, end in book_time:
        sh, sm = map(int, start.split(':'))
        eh, em = map(int, end.split(':'))
        changes[sh * 60 + sm] += 1
        # 방을 다시 쓸 수 있는 시각은 종료 10분 뒤다.
        changes[eh * 60 + em + 10] -= 1
    active = answer = 0
    # 시간 변화량을 누적하면 동시에 점유 중인 방 수가 된다.
    for change in changes:
        active += change
        answer = max(answer, active)
    return answer
```

## 왜 맞는가

방이 점유되는 반열린 구간의 겹침 수가 필요한 객실 수의 하한이다. 끝난 방을 다시 쓰는 배정으로 그 최댓값만큼의 방이면 모든 예약을 처리할 수 있다.

시간 O(N+1440), 공간 O(1440) / Time O(N+1440), space O(1440)

주의할 점: 종료+10분과 다음 시작이 같으면 재사용할 수 있다. 23:59 종료 뒤 청소까지 배열에 들어가야 한다.

## 다른 방법: 시작순 정렬 + 종료 시각 최소 힙

기본 풀이와 같은 결과를 구하되 중간 상태와 계산 방식이 다르다.

```python
from heapq import heappush,heappop

def solution(book_time):
    def minutes(text):
        h,m=map(int,text.split(':'))
        return h*60+m
    heap=[]
    rooms=0
    for start,end in sorted((minutes(a),minutes(b)+10) for a,b in book_time):
        while heap and heap[0]<=start: heappop(heap)
        heappush(heap,end)
        rooms=max(rooms,len(heap))
    return rooms
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 시작 시각에 +1, 종료+10분에 −1을 기록한다. 분 단위 변화량을 누적해 동시에 점유한 객실의 최댓값을 구한다. | 시작순 정렬 + 종료 시각 최소 힙 |
| 비용 | 시간 O(N+1440), 공간 O(1440) / Time O(N+1440), space O(1440) | 시간 O(N log N), 공간 O(N) / Time O(N log N), space O(N) |

## 검증

공식 예제 3개와 생성 입력 70개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Find the minimum room count including ten minutes of cleaning after each booking.

### Conditions and input/output

Input arguments: `book_time`. The return value is an integer satisfying the task described below.

- 1 ≤ len(book_time) ≤ 1000; 00:00 … 23:59 timestamps
- start < end; no booking crosses midnight; cleaning adds 10 minutes

### Approach

Record +1 at arrival and −1 ten minutes after departure. Prefix-sum the minute changes and take the maximum occupancy.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

The maximum overlap of half-open occupied intervals is a lower bound. Reusing completed rooms achieves that bound.

시간 O(N+1440), 공간 O(1440) / Time O(N+1440), space O(1440)

Boundary cases: A room is reusable exactly at end+10. Allow the cleanup interval after a 23:59 departure.

### Alternative: Start-order scheduling with a min-heap of availability times

It computes the same result using different intermediate states or evaluation steps. 시간 O(N log N), 공간 O(N) / Time O(N log N), space O(N)

The main approach follows the steps described above. The alternative uses start-order scheduling with a min-heap of availability times; compare its intermediate state and cost with the main implementation before choosing it.

### Verification

Local checks covered 3 official examples and 70 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 호텔 대실](https://school.programmers.co.kr/learn/courses/30/lessons/155651) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
