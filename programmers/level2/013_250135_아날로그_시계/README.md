# [PCCP 기출문제] 3번 / 아날로그 시계

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/250135) · Level 2 · Python3

시작·종료 시각을 포함해 초침이 시침이나 분침과 겹치는 횟수를 센다.

## 조건과 입출력

입력 매개변수: `h1, m1, s1, h2, m2, s2`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과다.

- 0 ≤ h1, h2 ≤ 23
- 0 ≤ m1, m2 ≤ 59
- 0 ≤ s1, s2 ≤ 59
- 시간이 23시 59분 59초를 초과해서 0시 0분 0초로 돌아가는 경우는 주어지지 않습니다.

## 풀이를 따라가기

초침과 시침의 상대 회전 수는 t·719/43200, 초침과 분침은 t·59/3600이다. 각 정수 회전 교차를 바닥 나눗셈으로 세고 세 바늘이 동시에 만나는 중복을 뺀다. 누적 횟수의 차이에 시작 시각의 겹침을 보정한다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(h1, m1, s1, h2, m2, s2):
    start = h1 * 3600 + m1 * 60 + s1
    end = h2 * 3600 + m2 * 60 + s2
    def count(t):
        # 상대 각도의 정수 회전 수를 세고 삼중 겹침을 한 번 뺀다.
        return t * 719 // 43200 + t * 59 // 3600 - t // 43200 + 1
    # 누적 횟수 차이에서 빠진 시작 순간을 다시 포함한다.
    at_start = start * 719 % 43200 == 0 or start * 59 % 3600 == 0
    return count(end) - count(start) + int(at_start)
```

## 왜 맞는가

겹침은 상대 각도가 한 바퀴의 정수배가 되는 순간이다. 두 쌍이 동시에 겹치는 시각은 12시간 간격이므로 포함-배제로 한 번만 센다.

시간 O(1), 공간 O(1) / Time and space O(1)

주의할 점: 00:00:00과 12:00:00의 삼중 겹침은 한 번이다. 실수 각도 비교 대신 정수 산술을 쓴다.

## 다른 방법: 유리수로 겹침 시각 직접 열거

기본 풀이와 같은 결과를 구하되 중간 상태와 계산 방식이 다르다.

```python
from fractions import Fraction

def solution(h1,m1,s1,h2,m2,s2):
    start, end = h1*3600+m1*60+s1, h2*3600+m2*60+s2
    events = set()
    for period, speed in ((43200,719),(3600,59)):
        for turn in range(end*speed//period+1):
            instant = Fraction(turn*period,speed)
            if start <= instant <= end:
                events.add(instant)
    return len(events)
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 초침과 시침의 상대 회전 수는 t·719/43200, 초침과 분침은 t·59/3600이다. 각 정수 회전 교차를 바닥 나눗셈으로 세고 세 바늘이 동시에 만나는 중복을 뺀다. 누적 횟수의 차이에 시작 시각의 겹침을 보정한다. | 유리수로 겹침 시각 직접 열거 |
| 비용 | 시간 O(1), 공간 O(1) / Time and space O(1) | 시간 O(T/60), 공간 O(T/60) / Time and space O(T/60); T=종료 초 / ending second |

## 검증

공식 예제 7개와 생성 입력 45개를 로컬에서 확인했다. 생성 입력은 기본 풀이와 대안 풀이를 비교했다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함한다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행한다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분한다.

## English

Count instants when the second hand meets the hour or minute hand, including both interval endpoints.

### Conditions and input/output

Input arguments: `h1, m1, s1, h2, m2, s2`. The return value is an integer satisfying the task described below.

- 0 ≤ h1,h2 ≤ 23; 0 ≤ m1,m2,s1,s2 ≤ 59
- start < end; no midnight wraparound

### Approach

Relative revolutions are t·719/43200 against the hour hand and t·59/3600 against the minute hand. Count integer crossings with floor division, subtract simultaneous triple meetings, then correct the inclusive start.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

A meeting occurs exactly when the relative angle is an integer revolution. Triple meetings recur every twelve hours, so inclusion-exclusion counts them once.

시간 O(1), 공간 O(1) / Time and space O(1)

Boundary cases: Count triple meetings at midnight and noon once. Integer arithmetic avoids floating-point angle comparisons.

### Alternative: Enumerate meeting instants with exact fractions

It computes the same result using different intermediate states or evaluation steps. 시간 O(T/60), 공간 O(T/60) / Time and space O(T/60); T=종료 초 / ending second

The main approach follows the steps described above. The alternative uses enumerate meeting instants with exact fractions; compare its intermediate state and cost with the main implementation before choosing it.

### Verification

Local checks covered 7 official examples and 45 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: [PCCP 기출문제] 3번 / 아날로그 시계](https://school.programmers.co.kr/learn/courses/30/lessons/250135) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
