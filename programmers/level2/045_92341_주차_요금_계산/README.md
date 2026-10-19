# 주차 요금 계산

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/92341) · Level 2 · Python3

차량별 하루 누적 주차 시간으로 요금을 계산해 차량번호순으로 반환합니다.

## 조건과 입출력

입력 매개변수: `fees, records`. 반환값은 수치 배열이며 아래 풀이의 조건을 만족하는 결과입니다.

- 1 ≤ fees[0] ≤ 1,439
- 0 ≤ fees[1] ≤ 100,000
- 1 ≤ fees[2] ≤ 1,439
- 1 ≤ fees[3] ≤ 10,000
- 1 ≤ records의 길이 ≤ 1,000
- records의 원소들은 시각을 기준으로 오름차순으로 정렬되어 주어집니다.
- 같은 시각에, 같은 차량번호의 내역이 2번 이상 나타내지 않습니다.

## 풀이를 따라가기

입차 시각을 저장하고 출차 때 차이를 누적합니다. 미출차 차량은 23:59에 출차한 것으로 더합니다. 기본 시간을 넘은 부분만 단위 시간으로 올림해 요금을 계산합니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(fees, records):
    entered, totals = {}, {}
    for record in records:
        time, car, action = record.split()
        hour, minute = map(int, time.split(':'))
        now = hour * 60 + minute
        if action == 'IN':
            entered[car] = now
        else:
            totals[car] = totals.get(car, 0) + now - entered.pop(car)
    for car, time in entered.items():
        # 출차 기록이 없으면 23:59에 나간 것으로 본다.
        totals[car] = totals.get(car, 0) + 1439 - time
    base_time, base_fee, unit_time, unit_fee = fees
    answer = []
    for car in sorted(totals):
        # 기본 시간을 넘은 부분에만 추가 요금을 부과한다.
        extra = max(0, totals[car] - base_time)
        answer.append(base_fee + (extra + unit_time - 1) // unit_time * unit_fee)
    return answer
```

## 정답이 되는 이유

정상 입출차는 차량별로 짝을 이루므로 각 차이의 합이 총 체류 시간입니다. 요금은 체류 구간마다가 아니라 하루 합계에 한 번 적용합니다.

시간 O(R+V log V), 공간 O(V) / Time O(R+V log V), space O(V)

주의할 점: 23:59 기준은 1439분입니다. 단위 시간이 정확히 나누어지면 추가 올림하지 않습니다.

## 다른 방법: 차량별 기록 그룹 후 시간 쌍 계산

```python
from collections import defaultdict

def solution(fees,records):
    logs=defaultdict(list)
    for record in records:
        time,car,_=record.split()
        h,m=map(int,time.split(':'))
        logs[car].append(h*60+m)
    answer=[]
    base,price,unit,extra=fees
    for car in sorted(logs):
        times=logs[car]
        if len(times)%2: times.append(1439)
        total=sum(times[i+1]-times[i] for i in range(0,len(times),2))
        answer.append(price+(max(0,total-base)+unit-1)//unit*extra)
    return answer
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 입차 시각을 저장하고 출차 때 차이를 누적합니다. 미출차 차량은 23:59에 출차한 것으로 더합니다. 기본 시간을 넘은 부분만 단위 시간으로 올림해 요금을 계산합니다. | 차량별 기록 그룹 후 시간 쌍 계산 |
| 비용 | 시간 O(R+V log V), 공간 O(V) / Time O(R+V log V), space O(V) | 시간 O(R+V log V), 공간 O(R) / Time O(R+V log V), space O(R) |

## 검증

공식 예제 3개와 생성 입력 40개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Compute fees from each vehicle’s total daily parking time and return them in vehicle-number order.

### Conditions and input/output

Input arguments: `fees, records`. The return value is a numeric list satisfying the task described below.

- len(fees)=4; base time 1 … 1439; base fee 0 … 100000
- unit time 1 … 1439; unit fee 1 … 10000; 1 ≤ len(records) ≤ 1000
- valid chronological daily records; unmatched entries exit at 23:59

### Approach

Store entry times and accumulate durations on exits. Close unmatched entries at 23:59, then ceil only the duration exceeding the base time into billing units.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Valid entry/exit pairs partition each vehicle’s stay. Apply the tariff once to the daily total, not separately to every visit.

시간 O(R+V log V), 공간 O(V) / Time O(R+V log V), space O(V)

Boundary cases: 23:59 is minute 1439. Do not add another unit when the extra time divides exactly.

### Alternative: Group records per vehicle and pair timestamps

시간 O(R+V log V), 공간 O(R) / Time O(R+V log V), space O(R)

### Verification

Local checks covered 3 official examples and 40 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 주차 요금 계산](https://school.programmers.co.kr/learn/courses/30/lessons/92341) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
