# 서버 증설 횟수

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/389479) · Level 2 · Python3

시간대별 이용자를 감당하도록 필요한 서버를 k시간씩 증설하고 총 증설 수를 구한다.

## 조건과 입출력

입력 매개변수: `players, m, k`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과다.

- 0 ≤ players의 원소 ≤ 1,000
- 1 ≤ m ≤ 1,000
- 1 ≤ k ≤ 24

## 풀이를 따라가기

시간이 시작되면 만료된 서버를 뺀다. 이용자 수를 m으로 나눈 몫만큼 서버가 필요하므로 부족한 수만 증설한다. 만료 시각에 그 수를 기록한다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(players, m, k):
    expires = [0] * (len(players) + k)
    active = 0
    answer = 0
    for hour, people in enumerate(players):
        # 이번 시간에 수명이 끝난 서버를 제외한다.
        active -= expires[hour]
        # 이용자 수를 감당하는 데 부족한 서버만 설치한다.
        added = max(0, people // m - active)
        active += added
        answer += added
        # 정확히 k시간 뒤에 설치 수만큼 만료시킨다.
        expires[hour + k] += added
    return answer
```

## 왜 맞는가

현재 부족한 서버는 반드시 지금 설치해야 한다. 더 미리 설치하면 수명이 빨리 끝나고, 필요한 수보다 더 설치해도 지금 설치하는 최소 계획보다 유리할 수 없다.

시간 O(H+k), 공간 O(H+k) / Time O(H+k), space O(H+k); H=len(players)

주의할 점: 한 대의 기간은 설치 시각부터 k개 시간대다. 수요가 m보다 작으면 추가 서버는 0대다.

## 다른 방법: 만료 시각을 저장하는 최소 힙

```python
from heapq import heappush, heappop

def solution(players, m, k):
    expires = []
    active = answer = 0
    for hour, people in enumerate(players):
        while expires and expires[0][0] <= hour:
            _, count = heappop(expires)
            active -= count
        added = max(0, people//m-active)
        if added:
            heappush(expires, (hour+k, added))
            active += added
            answer += added
    return answer
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 시간이 시작되면 만료된 서버를 뺀다. 이용자 수를 m으로 나눈 몫만큼 서버가 필요하므로 부족한 수만 증설한다. 만료 시각에 그 수를 기록한다. | 만료 시각을 저장하는 최소 힙 |
| 비용 | 시간 O(H+k), 공간 O(H+k) / Time O(H+k), space O(H+k); H=len(players) | 시간 O(H log H), 공간 O(H) / Time O(H log H), space O(H) |

## 검증

공식 예제 3개와 생성 입력 70개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Add servers lasting k hours to meet each hour’s demand, and minimize the total number added.

### Conditions and input/output

Input arguments: `players, m, k`. The return value is an integer satisfying the task described below.

- len(players)=24; 0 ≤ players[i] ≤ 1000
- 1 ≤ m ≤ 1000; 1 ≤ k ≤ 24

### Approach

At each hour, remove expired servers. Demand requires players//m servers; add only the shortfall and schedule their expiration.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

A current shortage must be filled now. Installing earlier only shortens useful remaining lifetime, and installing more than the shortfall cannot outperform delaying those extra servers until needed.

시간 O(H+k), 공간 O(H+k) / Time O(H+k), space O(H+k); H=len(players)

Boundary cases: A server covers exactly k hourly slots starting at installation. Demand below m needs no added server.

### Alternative: Min-heap of expiration events

시간 O(H log H), 공간 O(H) / Time O(H log H), space O(H)

### Verification

Local checks covered 3 official examples and 70 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 서버 증설 횟수](https://school.programmers.co.kr/learn/courses/30/lessons/389479) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
