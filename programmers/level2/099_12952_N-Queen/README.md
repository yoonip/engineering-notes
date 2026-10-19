# N-Queen

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12952) · Level 2 · Python3

## 문제와 조건 / Task and conditions

1≤n≤12인 n×n 체스판입니다. n개 퀸이 가로·세로·대각선으로 서로 공격하지 않는 배치 수를 반환합니다.

The board is n×n with 1≤n≤12. Count placements of n queens with no shared row, column or diagonal.

## 풀이 흐름 / Approach

한 행에 퀸 하나를 놓습니다. 이미 쓰인 열과 두 대각선을 비트마스크로 표시하고, 충돌하지 않는 열만 다음 행으로 탐색합니다.

Place one queen per row. Bitmasks track occupied columns and the two diagonal attack directions; recurse only into unattacked columns.

## 정답이 되는 이유 / Why it works

각 행에서 금지된 열의 합집합을 뺀 자리만 선택하므로 모든 배치는 안전합니다. 안전한 모든 선택을 빠짐없이 탐색하며 각 배치는 행별 선택으로 유일하게 생성됩니다.

Removing the union of occupied and attacked columns ensures every placement is safe. Exhausting all remaining choices enumerates every valid board exactly once.

## 비용 / Complexity

탐색 시간 O(n!) 상한, 호출 공간 O(n) / O(n!) search upper bound, O(n) recursion space

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(n):
    # 아래 n비트가 모두 1인 마스크로 유효 열 표시.
    full = (1 << n) - 1
    def search(columns, left, right):
        if columns == full:
            return 1
        # 현재 행에서 열·대각선 공격을 안 받는 열만 선택.
        available = full & ~(columns | left | right)
        count = 0
        while available:
            # 음수와 비트 AND를 취해 가장 오른쪽 1비트 하나 추출.
            position = available & -available
            available -= position
            # 다음 행의 대각선은 <<1·>>1로 한 열씩 옮겨 재귀 호출, +=로 경우의 수 누적.
            count += search(columns | position, (left | position) << 1, (right | position) >> 1)
        return count
    return search(0, 0, 0)
```

## 다른 방법: 열·대각선 집합 / Column and diagonal sets

열, 행−열, 행+열을 집합으로 관리합니다. 비트 이동을 이해하지 않아도 제약을 직접 읽을 수 있지만 집합 조작 비용이 추가됩니다.

Store columns, row−column diagonals and row+column diagonals in sets. The constraints are explicit without bit shifts, at the cost of set-operation overhead.

[alternative.py](alternative.py)

```python
def solution(n):
    columns, descending, ascending = set(), set(), set()
    def place(row):
        if row == n:
            return 1
        count = 0
        for col in range(n):
            if col in columns or row - col in descending or row + col in ascending:
                continue
            columns.add(col)
            descending.add(row - col)
            ascending.add(row + col)
            count += place(row + 1)
            columns.remove(col)
            descending.remove(row - col)
            ascending.remove(row + col)
        return count
    return place(0)
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    4
  ],
  "output": 2
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 10개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 10 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 10개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 10 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 12952](https://school.programmers.co.kr/learn/courses/30/lessons/12952), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 12952](https://school.programmers.co.kr/learn/courses/30/lessons/12952), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
