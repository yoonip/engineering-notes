# 점프와 순간 이동

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12980) · Level 2 · Python3

## 문제와 조건 / Task and conditions

도착점 n은 1~1000000000입니다. k칸 점프는 k 비용, 현재 위치의 두 배로 이동은 무료입니다. 0에서 n까지 최소 배터리를 반환합니다.

The target n is 1–1000000000. A jump of k costs k, while doubling the current position is free. Return minimum battery cost from zero to n.

## 풀이 흐름 / Approach

도착점에서 거꾸로 생각합니다. 짝수이면 비용 없이 절반으로 돌아가고, 홀수이면 배터리 1을 써서 1을 뺀 뒤 절반으로 돌아갑니다. 이 과정은 이진수의 1 개수를 세는 것과 같습니다.

Work backwards from the destination: halve an even position for free, or spend one unit to subtract one from an odd position and then halve. This counts one bits in binary.

## 정답이 되는 이유 / Why it works

짝수 위치는 순간이동의 역연산으로 비용 없이 줄일 수 있습니다. 홀수는 순간이동만으로 만들 수 없어 최소 한 번의 단위 점프가 필요합니다. 이 최적 선택을 반복하면 1비트 수가 최소 비용입니다.

An even position can be reduced by reversing a free teleport. An odd position requires at least one unit jump. Repeating these optimal reductions gives the population count.

## 비용 / Complexity

시간 O(log n), 공간 O(1) / O(log n) time, O(1) space

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(n):
    answer = 0
    while n:
        # 홀수 위치는 1칸 점프 비용이 필요하고 짝수는 비용 0.
        answer += n % 2
        n //= 2
    return answer
```

## 다른 방법: 작은 거리의 최단 비용 DP / Minimum-cost DP for small distances

각 위치에 점프로 오는 비용과 짝수 위치에 순간이동으로 오는 비용을 비교합니다. 시간·공간 O(n)이어서 큰 n용 제출보다 작은 입력 검증에 씁니다.

Compare arriving by a paid unit jump with arriving by a free teleport at even positions. O(n) time and space make it a small-distance verification reference.

[alternative_reference.py](alternative_reference.py)

```python
def solution(n):
    cost = [0] * (n + 1)
    for position in range(1, n + 1):
        cost[position] = cost[position - 1] + 1
        if position % 2 == 0:
            cost[position] = min(cost[position], cost[position // 2])
    return cost[n]
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    5
  ],
  "output": 2
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

출처: [프로그래머스 문제 12980](https://school.programmers.co.kr/learn/courses/30/lessons/12980), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 12980](https://school.programmers.co.kr/learn/courses/30/lessons/12980), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
