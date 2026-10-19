# [PCCP 기출문제] 3번 / 충돌위험 찾기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/340211) · Level 2 · Python3

정해진 경로를 움직이는 로봇이 같은 시각·좌표에 두 대 이상 모이는 횟수를 센다.

## 조건과 입출력

입력 매개변수: `points, routes`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과다.

- 2 ≤ points의 길이 = n ≤ 100
- 1 ≤ r ≤ 100
- 1 ≤ c ≤ 100
- 2 ≤ routes의 길이 = 로봇의 수 = x ≤ 100
- 2 ≤ routes[i]의 길이 = m ≤ 100
- 1 ≤ routes[i][j] ≤ n

## 풀이를 따라가기

매 초 현재 위치를 센다. 행부터 목적지와 같게 맞춘 다음 열을 이동한다. 마지막 도착 위치는 세고 다음 초부터 로봇을 제외한다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(points, routes):
    robots = []
    for route in routes:
        r, c = points[route[0] - 1]
        robots.append((r, c, 1, route))
    answer = 0
    while robots:
        counts = {}
        next_robots = []
        for r, c, index, route in robots:
            position = (r, c)
            # 같은 시각 같은 좌표에 있는 로봇 수를 센다.
            counts[position] = counts.get(position, 0) + 1
            if index == len(route):
                continue
            target_r, target_c = points[route[index] - 1]
            # 행을 먼저 맞춘 뒤 열을 움직인다.
            if r != target_r:
                r += 1 if r < target_r else -1
            elif c != target_c:
                c += 1 if c < target_c else -1
            if r == target_r and c == target_c:
                index += 1
            next_robots.append((r, c, index, route))
        for count in counts.values():
            # 여러 대가 모여도 좌표 하나의 위험은 한 번만 센다.
            if count >= 2:
                answer += 1
        robots = next_robots
    return answer
```

## 왜 맞는가

현재 로봇 목록이 그 시각에 센터 안에 있는 로봇을 정확히 나타내도록 갱신한다. 좌표별 빈도가 2 이상인지 검사하면 로봇 쌍 수가 아니라 위험 상황 수를 센다.

시간 O(A·T), 공간 O(A) / Time O(A·T), space O(A); A=로봇 수 / robot count, T=최대 이동 시간 / longest route duration

주의할 점: 0초와 마지막 도착 시각을 포함한다. 네 대가 한 좌표에 모여도 그 좌표의 위험은 한 번이다.

## 다른 방법: 로봇별 경로 전개 + 시공간 해시

기본 풀이와 같은 결과를 구하되 중간 상태와 계산 방식이 다르다.

```python
from collections import Counter

def solution(points, routes):
    occupied = Counter()
    for route in routes:
        row, col = points[route[0]-1]
        time = 0
        occupied[(time,row,col)] += 1
        for point in route[1:]:
            r, c = points[point-1]
            while row != r or col != c:
                if row != r:
                    row += 1 if row < r else -1
                else:
                    col += 1 if col < c else -1
                time += 1
                occupied[(time,row,col)] += 1
    return sum(count >= 2 for count in occupied.values())
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 매 초 현재 위치를 센다. 행부터 목적지와 같게 맞춘 다음 열을 이동한다. 마지막 도착 위치는 세고 다음 초부터 로봇을 제외한다. | 로봇별 경로 전개 + 시공간 해시 |
| 비용 | 시간 O(A·T), 공간 O(A) / Time O(A·T), space O(A); A=로봇 수 / robot count, T=최대 이동 시간 / longest route duration | 시간 O(총 이동량), 공간 O(총 이동량) / Time and space O(total trajectory length) |

## 검증

공식 예제 3개와 생성 입력 40개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Count time-position pairs occupied by at least two robots following their prescribed routes.

### Conditions and input/output

Input arguments: `points, routes`. The return value is an integer satisfying the task described below.

- 2 ≤ len(points) ≤ 100; 1 ≤ row,column ≤ 100; unique points
- 2 ≤ number of robots ≤ 100; 2 ≤ route length ≤ 100
- all route lengths equal; consecutive waypoints differ

### Approach

Count current positions each second. Move along rows before columns toward the next waypoint. Count a final arrival position, then remove that robot from the following second.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

The active list represents exactly the robots still present at that time. Testing whether each coordinate count is at least two counts danger events rather than robot pairs.

시간 O(A·T), 공간 O(A) / Time O(A·T), space O(A); A=로봇 수 / robot count, T=최대 이동 시간 / longest route duration

Boundary cases: Include time zero and the final arrival instant. Four robots at one coordinate still form one danger event.

### Alternative: Expand each trajectory into a time-position hash table

It computes the same result using different intermediate states or evaluation steps. 시간 O(총 이동량), 공간 O(총 이동량) / Time and space O(total trajectory length)

The main approach follows the steps described above. The alternative uses expand each trajectory into a time-position hash table; compare its intermediate state and cost with the main implementation before choosing it.

### Verification

Local checks covered 3 official examples and 40 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: [PCCP 기출문제] 3번 / 충돌위험 찾기](https://school.programmers.co.kr/learn/courses/30/lessons/340211) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
