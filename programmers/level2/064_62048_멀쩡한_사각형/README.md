# 멀쩡한 사각형

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/62048) · Level 2 · Python3

## 문제와 조건 / Task and conditions

w,h는 1~100000000의 정수입니다. 대각선에 걸리지 않는 1×1 칸 수를 반환합니다.

w and h are integers in [1,100000000]. Return the number of unit cells not cut by the diagonal.

## 풀이 흐름 / Approach

대각선이 잘라 놓은 칸만 세어 전체 칸 수에서 뺍니다. 가로 경계를 지날 때와 세로 경계를 지날 때 새 칸에 들어갑니다. 두 경계를 동시에 지나는 격자점은 최대공약수로 보정합니다.

Count the cells crossed by the diagonal and subtract them from the whole rectangle. Crossing a vertical or horizontal grid line enters another cell; the greatest common divisor corrects simultaneous crossings.

## 정답이 되는 이유 / Why it works

w와 h를 최대공약수 g로 나누면 같은 모양의 구간이 g개입니다. 각 구간에서 내부 격자점은 없으므로 잘린 칸은 w/g+h/g−1개이고, 전체는 w+h−g개입니다.

Splitting at the g=gcd(w,h) lattice intervals gives g copies without an interior lattice point. Each crosses w/g+h/g−1 cells, hence w+h−g in total.

## 비용 / Complexity

시간 O(log min(w,h)), 공간 O(1) / Time O(log min(w,h)), space O(1)

## 구현 / Implementation

[solution.py](solution.py)

```python
from math import gcd

def solution(w, h):
    # 대각선이 지나는 잘린 칸 수 계산.
    broken = w + h - gcd(w, h)
    return w * h - broken
```

## 다른 방법: 열별 정수 격자 계산 / Column-by-column integer counting

각 세로 띠에서 선 아래에 온전히 들어가는 칸을 정수 나눗셈으로 세고 두 배 합니다. 시간 O(w)라서 작은 입력 대조에 사용합니다. 부동소수점 기울기를 쓰지 않아 경계 오차가 없습니다.

Count complete cells below the line in each column using integer division and double the result. This O(w) implementation is a small-input reference and avoids floating-point boundary errors.

[alternative_reference.py](alternative_reference.py)

```python
def solution(w, h):
    # 선 아래의 완전한 칸을 세면 선 위에도 같은 수가 있다.
    return 2 * sum((h * column) // w for column in range(w))
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    8,
    12
  ],
  "output": 80
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

출처: [프로그래머스 문제 62048](https://school.programmers.co.kr/learn/courses/30/lessons/62048), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 62048](https://school.programmers.co.kr/learn/courses/30/lessons/62048), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
