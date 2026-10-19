# 다리를 지나는 트럭

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/42583) · Level 2 · Python3

## 문제와 조건 / Task and conditions

다리 길이·무게 한도·트럭 수는 각각 1~10000입니다. 트럭은 입력 순서대로 초당 최대 한 대 진입하고 각 트럭은 한도 이하입니다. 마지막 트럭이 완전히 나온 시각을 반환합니다.

Bridge length, capacity and truck count are each 1–10000. At most one truck enters per second in input order, and each truck fits individually. Return when the last truck fully exits.

## 풀이 흐름 / Approach

다리에 올라간 트럭의 무게와 나가는 시각을 큐에 저장합니다. 다음 트럭을 넣을 수 없으면 가장 빠른 퇴장 시각으로 바로 이동합니다. 매초 빈 다리를 만들며 기다릴 필요가 없습니다.

Store each truck’s weight and exit time in a queue. If the next truck cannot enter, jump directly to the earliest exit event instead of simulating empty waiting seconds.

## 왜 맞는가 / Why it works

진입 순서는 고정이고 다음 상태가 바뀌는 시점은 트럭 퇴장뿐입니다. 필요한 퇴장까지 시간을 건너뛰어도 중간에 가능한 진입을 놓치지 않으므로 초 단위 시뮬레이션과 같은 결과입니다.

Entry order is fixed, and only an exit can change feasibility during a wait. Jumping to the next necessary exit therefore skips no possible entry and matches second-by-second simulation.

## 비용 / Complexity

시간 O(n), 공간 O(n) / Time O(n), space O(n)

## 구현 / Implementation

[solution.py](solution.py)

```python
from collections import deque

def solution(bridge_length, weight, truck_weights):
    # 다리 위 (무게,퇴장 시각) 튜플을 저장할 빈 큐.
    bridge = deque()
    time = load = 0
    # 대기 트럭을 순서대로 처리.
    for truck in truck_weights:
        time += 1
        while bridge and (bridge[0][1] <= time or load + truck > weight):
            # 두 값 언패킹.
            leaving, exit_time = bridge.popleft()
            time = max(time, exit_time)
            # 떠난 트럭 무게 차감.
            load -= leaving
        bridge.append((truck, time + bridge_length))
        # 진입한 트럭의 무게 추가.
        load += truck
    return bridge[-1][1]
```

## 다른 방법: 다리 칸 큐의 초 단위 시뮬레이션 / Second-by-second bridge slots

길이만큼 0을 넣은 큐를 한 초마다 움직입니다. 다리 길이에 따른 빈 시간도 계산하므로 큰 길이에서는 이벤트 방식보다 느립니다.

Move a length-sized queue one slot each second. It is straightforward but also processes empty waiting time and becomes slower for long bridges.

[alternative_reference.py](alternative_reference.py)

```python
from collections import deque

def solution(bridge_length, weight, truck_weights):
    waiting = deque(truck_weights)
    bridge = deque([0] * bridge_length)
    time = load = 0
    while waiting or load:
        time += 1
        load -= bridge.popleft()
        if waiting and load + waiting[0] <= weight:
            truck = waiting.popleft()
            bridge.append(truck)
            load += truck
        else:
            bridge.append(0)
    return time
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    2,
    10,
    [
      7,
      4,
      5,
      6
    ]
  ],
  "output": 8
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 31개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 31 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 31개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 31 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 42583](https://school.programmers.co.kr/learn/courses/30/lessons/42583), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 42583](https://school.programmers.co.kr/learn/courses/30/lessons/42583), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
