# 조이스틱

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/42860) · Level 2 · Python3

## 문제와 조건 / Task and conditions

name은 대문자 1~20자입니다. A로 채워진 이름과 맨 앞 커서에서 시작하며 알파벳·좌우 커서가 순환합니다. 최소 조작 수를 반환합니다.

name has 1–20 uppercase letters. Start with all A characters and the cursor at the first position; alphabet and horizontal movements wrap. Return the minimum operations.

## 풀이 흐름 / Approach

각 문자를 A에서 바꾸는 상하 이동은 서로 독립입니다. 좌우 이동에서는 연속한 A 구간을 지나지 않고 되돌아오는 경로를 비교합니다. 왼쪽 구간을 왕복하거나 오른쪽 구간을 왕복하는 두 방향을 모두 봅니다.

Vertical changes from A are independent per character. For horizontal movement, consider skipping a consecutive A run by turning around, checking both choices of which side is traversed twice.

## 정답이 되는 이유 / Why it works

필요한 위치를 방문하는 최단 경로는 불필요한 여러 번의 왕복을 지울 수 있어 최대 한 번 방향을 바꾸는 형태로 줄어듭니다. A 구간 앞 길이 i와 뒤 길이 t에 대해 2i+t, i+2t를 비교합니다.

Extra reversals can be removed from an optimal visit route, leaving a route with at most one turn. For prefix length i and remaining suffix length t, compare 2i+t and i+2t.

## 비용 / Complexity

주 풀이: 다음 비-A 위치 전처리로 시간 O(n), 공간 O(n) / Main: O(n) time and space with next-non-A preprocessing

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(name):
    vertical = sum(min(ord(ch) - ord('A'), ord('Z') - ord(ch) + 1) for ch in name)
    n = len(name)
    # 각 위치에서 다음으로 만나는 비-A 위치를 오른쪽부터 미리 구한다.
    next_needed = [n] * (n + 1)
    for i in range(n - 1, -1, -1):
        next_needed[i] = i if name[i] != 'A' else next_needed[i + 1]
    horizontal = n - 1
    for i in range(n):
        tail = n - next_needed[i + 1]
        # 앞쪽을 왕복하는 경로와 뒤쪽을 왕복하는 경로를 비교한다.
        horizontal = min(horizontal, 2 * i + tail, i + 2 * tail)
    return vertical + horizontal
```

## 다른 방법: 위치·방문 집합 BFS / Position-and-visited-mask BFS

수정이 필요한 위치를 모두 방문하는 최단 이동을 BFS로 구합니다. 그리디 경로식과 별개로 검증할 수 있지만 상태가 O(n2ⁿ)이므로 작은 이름에서만 사용합니다.

Run BFS over cursor positions and visited required positions. This independently checks the route formula but has O(n2ⁿ) states and is intended for short names.

[alternative_reference.py](alternative_reference.py)

```python
from collections import deque

def solution(name):
    n = len(name)
    required = sum(1 << i for i, ch in enumerate(name) if ch != 'A')
    vertical = sum(min(ord(ch) - 65, 91 - ord(ch)) for ch in name)
    start = (0, required & ~1)
    queue = deque([(start[0], start[1], 0)])
    seen = {start}
    while queue:
        pos, left, cost = queue.popleft()
        if not left:
            return vertical + cost
        for nxt in ((pos - 1) % n, (pos + 1) % n):
            state = (nxt, left & ~(1 << nxt))
            if state not in seen:
                seen.add(state)
                queue.append((state[0], state[1], cost + 1))
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    "JEROEN"
  ],
  "output": 56
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

출처: [프로그래머스 문제 42860](https://school.programmers.co.kr/learn/courses/30/lessons/42860), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 42860](https://school.programmers.co.kr/learn/courses/30/lessons/42860), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

큰 입력 검사: 최대 이름 길이의 전부 A / All-A at maximum name length

```bash
python verify_stress.py
```
