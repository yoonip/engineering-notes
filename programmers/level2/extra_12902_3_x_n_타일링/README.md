# 3 x n 타일링

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12902) · Level 2 · Python3

## 문제와 조건 / Task and conditions

1≤n≤5000입니다. 3×n 판을 1×2 또는 2×1 도미노로 채우는 경우 수를 1000000007로 나눈 나머지로 반환합니다.

1≤n≤5000. Count domino tilings of a 3×n board modulo 1000000007.

## 풀이 흐름 / Approach

3×n 보드는 넓이가 짝수여야 하므로 n이 홀수면 불가능합니다. 짝수 폭의 기본 배치와 좌우로 이어지는 특수 배치를 묶으면 f(n)=4f(n−2)−f(n−4)로 줄어듭니다.

A 3×n board must have even area, so odd n is impossible. Grouping ordinary width-two tilings and the longer special boundary patterns simplifies the recurrence to f(n)=4f(n−2)−f(n−4).

## 왜 맞는가 / Why it works

먼저 f(n)=3f(n−2)+2Σf(n−4),f(n−6),…를 얻습니다. n−2에 대한 같은 식을 빼면 합이 소거되어 4f(n−2)−f(n−4)가 됩니다. f(0)=1,f(2)=3입니다.

Start with f(n)=3f(n−2)+2 times the sum f(n−4)+f(n−6)+…. Subtract the corresponding recurrence for n−2 to eliminate the sum, leaving 4f(n−2)−f(n−4). Bases are f(0)=1 and f(2)=3.

## 비용 / Complexity

시간 O(n), 공간 O(1) / O(n) time, O(1) space

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(n):
    if n % 2:
        return 0
    # 너비 0은 빈 배치 한 가지, 너비 2는 세 가지.
    previous, current = 1, 3
    for _ in range(4, n + 1, 2):
        # 점화식 f(n)=4f(n-2)-f(n-4), %는 나머지.
        previous, current = current, (4 * current - previous) % 1000000007
    return current
```

## 다른 방법: 열별 프로파일 DP / Column-profile DP

현재 열에서 이미 채워진 세 칸을 비트마스크로 표시하고 실제 도미노를 놓습니다. 점화식을 외우지 않아도 전이를 만들 수 있으며 고정 높이에서 시간 O(n), 공간 O(1)입니다.

Represent the three occupied cells of a column by a bitmask and place actual dominoes. This derives transitions without relying on the closed recurrence and remains O(n) time and constant space for fixed height.

[alternative.py](alternative.py)

```python
def solution(n):
    dp = {0: 1}
    for _ in range(n):
        next_dp = {}
        def fill(mask, following, count):
            if mask == 7:
                next_dp[following] = (next_dp.get(following, 0) + count) % 1000000007
                return
            row = next(i for i in range(3) if not (mask >> i & 1))
            # 가로 도미노는 다음 열의 같은 칸을 예약한다.
            fill(mask | (1 << row), following | (1 << row), count)
            if row + 1 < 3 and not (mask >> (row + 1) & 1):
                fill(mask | (3 << row), following, count)
        for mask, count in dp.items():
            fill(mask, 0, count)
        dp = next_dp
    return dp.get(0, 0)
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    4
  ],
  "output": 11
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 29개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 29 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 29개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 29 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 12902](https://school.programmers.co.kr/learn/courses/30/lessons/12902), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 12902](https://school.programmers.co.kr/learn/courses/30/lessons/12902), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
