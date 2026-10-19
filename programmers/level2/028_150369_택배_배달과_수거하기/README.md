# 택배 배달과 수거하기

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/150369) · Level 2 · Python3

용량이 제한된 트럭으로 배달과 수거를 모두 마치는 최소 왕복 거리를 구합니다.

## 조건과 입출력

입력 매개변수: `cap, n, deliveries, pickups`. 반환값은 정수이며 아래 풀이의 조건을 만족하는 결과입니다.

- 1 ≤ cap ≤ 50
- 1 ≤ n ≤ 100,000
- 0 ≤ deliveries의 원소 ≤ 50
- 0 ≤ pickups의 원소 ≤ 50

## 풀이를 따라가기

먼 집부터 배달·수거의 누적 부족량을 더합니다. 둘 중 더 많은 왕복을 요구하는 쪽만큼 운행하고 두 누적량에서 용량을 뺍니다. 음수 누적량은 그 운행의 남은 여유입니다.

[기본 풀이 / Main](solution.py) · [다른 풀이 / Alternative](alternative.py) · [제출 원본 / Archived submission](submitted_original.py)

```python
def solution(cap, n, deliveries, pickups):
    delivery = pickup = answer = 0
    # 가장 먼 집부터 처리하면 필수 운행의 여유를 가까운 집에 쓸 수 있다.
    for index in range(n - 1, -1, -1):
        delivery += deliveries[index]
        pickup += pickups[index]
        # 배달과 수거 중 더 많은 왕복을 요구하는 쪽에 맞춘다.
        trips = max(0, (delivery + cap - 1) // cap, (pickup + cap - 1) // cap)
        answer += trips * (index + 1) * 2
        # 음수는 이 운행에 남은 용량이므로 그대로 유지한다.
        delivery -= trips * cap
        pickup -= trips * cap
    return answer
```

## 정답이 되는 이유

먼 집의 물량을 처리하려면 그 거리까지 필요한 왕복을 반드시 해야 합니다. 같은 왕복의 빈 용량을 가까운 집에 쓰면 추가 거리를 들이지 않으므로 먼 곳 우선이 최적입니다.

시간 O(n), 공간 O(1) / Time O(n), space O(1)

주의할 점: 배달 용량과 수거 용량은 같은 왕복 안에서 각각 이용합니다. 음수 여유를 0으로 지우면 재사용 기회를 잃습니다.

## 다른 방법: 왕복마다 먼 물량을 실제로 소진

```python
def solution(cap,n,deliveries,pickups):
    delivery,pickup=list(deliveries),list(pickups)
    di=pi=n-1
    answer=0
    while True:
        while di>=0 and delivery[di]==0: di-=1
        while pi>=0 and pickup[pi]==0: pi-=1
        if di<0 and pi<0: return answer
        answer+=2*(max(di,pi)+1)
        for values,index in ((delivery,di),(pickup,pi)):
            room=cap
            while index>=0 and room:
                used=min(values[index],room)
                values[index]-=used
                room-=used
                if values[index]==0: index-=1
```

| 비교 | 기본 풀이 | 다른 풀이 |
|---|---|---|
| 계산 방식 | 먼 집부터 배달·수거의 누적 부족량을 더합니다. 둘 중 더 많은 왕복을 요구하는 쪽만큼 운행하고 두 누적량에서 용량을 뺍니다. 음수 누적량은 그 운행의 남은 여유입니다. | 왕복마다 먼 물량을 실제로 소진 |
| 비용 | 시간 O(n), 공간 O(1) / Time O(n), space O(1) | 시간 O(n+총 운행 수), 공간 O(n) / Time O(n+number of trips), space O(n) |

## 검증

공식 예제 2개와 생성 입력 70개를 로컬에서 확인했습니다. 생성 입력은 기본 풀이와 대안 풀이를 비교했습니다. 저장된 테스트는 공식 예제와 경계·소형 입력을 포함합니다. 제한 상한에 해당하는 크기·수치의 경계 검사도 저장된 테스트에 포함했습니다.

문제 폴더에서 `python test_solution.py`로 저장된 검사를 실행합니다. 로컬 기록의 원본 코드는 채점 100점으로 보관되어 있으며, 주석 정리와 대안 코드는 이 로컬 검증 결과로 구분합니다.

## English

Minimize round-trip distance while completing deliveries and pickups with a capacity-limited truck.

### Conditions and input/output

Input arguments: `cap, n, deliveries, pickups`. The return value is an integer satisfying the task described below.

- 1 ≤ cap ≤ 50; 1 ≤ n ≤ 100000; both arrays have length n
- 0 ≤ deliveries[i],pickups[i] ≤ 50

### Approach

Scan houses from farthest to nearest, accumulating delivery and pickup deficits. Add enough trips for the larger requirement, then subtract their capacity from both totals. Negative totals represent spare capacity.

The runnable code is linked above; its comments are in Korean.

### Correctness and cost

Trips required for the farthest remaining house are unavoidable. Filling their spare capacity at nearer houses adds no distance, making the farthest-first strategy optimal.

시간 O(n), 공간 O(1) / Time O(n), space O(1)

Boundary cases: Delivery and pickup capacities are usable separately within a trip. Do not erase negative spare capacity by clamping it to zero.

### Alternative: Explicitly consume farthest loads on each trip

시간 O(n+총 운행 수), 공간 O(n) / Time O(n+number of trips), space O(n)

### Verification

Local checks covered 2 official examples and 70 generated inputs. Generated inputs were compared between the main and alternative implementations. Saved tests include official examples and small/boundary cases. Saved tests also include a size or numeric boundary at the stated upper limit.

Run `python test_solution.py` in this problem directory. The local archive records the original submission as accepted with a score of 100. Comment cleanup and alternative implementations are covered by the local checks described here.

## 출처 / Source

- [프로그래머스: 택배 배달과 수거하기](https://school.programmers.co.kr/learn/courses/30/lessons/150369) — 조건·입출력·예제 확인 / conditions, inputs, outputs and examples; 2026-10-19.
