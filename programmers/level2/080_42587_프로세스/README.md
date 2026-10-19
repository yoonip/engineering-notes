# 프로세스

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/42587) · Level 2 · Python3

## 문제와 조건 / Task and conditions

작업은 1~100개, 중요도는 1~9이고 location은 0기반입니다. 더 중요한 작업이 남으면 맨 앞 작업을 뒤로 보내며 목표 작업의 1기반 실행 순서를 반환합니다.

There are 1–100 jobs with priorities 1–9 and a zero-based location. Rotate the front job when a higher priority remains and return the target’s one-based execution rank.

## 풀이 흐름 / Approach

큐에는 원래 위치와 중요도를 저장합니다. 현재 중요도보다 높은 작업이 남아 있으면 뒤로 보내고, 없으면 실행합니다. 중요도별 남은 수로 최댓값을 관리하면 큐 전체를 매번 검사하지 않아도 됩니다.

Keep original indices and priorities in a queue. Rotate an item if a higher-priority one remains; otherwise execute it. Counts by priority avoid rescanning the full queue for its maximum.

## 왜 맞는가 / Why it works

중요도별 개수는 큐의 내용과 항상 같습니다. 최댓값보다 낮은 항목만 뒤로 보내므로 실행 순서는 문제 규칙과 같고, 원래 위치로 목표 항목을 구별할 수 있습니다.

Priority counts always match the queue. Rotating exactly the items below the current maximum reproduces the required order, while original indices identify the target.

## 비용 / Complexity

중요도 종류 p에 시간 O(np), 공간 O(n+p); 문제에서는 p≤9 / O(np) time, O(n+p) space; p≤9 here

## 구현 / Implementation

[solution.py](solution.py)

```python
from collections import Counter, deque

def solution(priorities, location):
    queue = deque(enumerate(priorities))
    remaining = Counter(priorities)
    maximum = max(remaining)
    executed = 0
    while queue:
        index, priority = queue.popleft()
        if priority < maximum:
            queue.append((index, priority))
            continue
        executed += 1
        remaining[priority] -= 1
        if index == location:
            return executed
        # 높은 중요도가 소진되면 다음으로 남은 중요도를 찾는다.
        while maximum and remaining[maximum] == 0:
            maximum -= 1
```

## 다른 방법: 큐 전체의 높은 중요도 검사 / Scan the queue for higher priorities

각 차례에 더 높은 중요도가 있는지 any로 확인하는 직접 시뮬레이션입니다. 구현은 짧지만 반복 순회가 추가돼 보수적 시간 상한은 O(n²p)입니다.

A direct simulation scans the queue with any at every turn. It is short but adds repeated traversal, with a conservative O(n²p) upper bound.

[alternative.py](alternative.py)

```python
from collections import deque

def solution(priorities, location):
    queue = deque(enumerate(priorities))
    executed = 0
    while queue:
        index, priority = queue.popleft()
        if any(other > priority for _, other in queue):
            queue.append((index, priority))
        else:
            executed += 1
            if index == location:
                return executed
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    [
      2,
      1,
      3,
      2
    ],
    2
  ],
  "output": 1
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 30개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 30 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 30개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 30 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 42587](https://school.programmers.co.kr/learn/courses/30/lessons/42587), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 42587](https://school.programmers.co.kr/learn/courses/30/lessons/42587), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
