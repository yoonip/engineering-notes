# 예상 대진표

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12985) · Level 2 · Python3

## 문제와 조건 / Task and conditions

n은 2¹~2²⁰의 2 거듭제곱이며 a,b는 서로 다른 1~n 번호입니다. 두 선수가 계속 이긴다고 할 때 처음 만나는 라운드를 반환합니다.

n is a power of two from 2¹ through 2²⁰; a,b are distinct indices in [1,n]. Assuming both keep winning, return their first meeting round.

## 풀이 흐름 / Approach

한 라운드 뒤 번호는 (번호+1)//2입니다. 두 참가자 번호가 같아질 때까지 이를 반복하며 라운드 수를 셉니다.

After one round, a player’s next bracket number is (number+1)//2. Repeat until both numbers coincide and count the rounds.

## 정답이 되는 이유 / Why it works

같은 다음 라운드 번호를 가진 두 선수는 바로 그 라운드에서 만납니다. 번호를 반복해서 부모 대진으로 바꾸면 처음 같아지는 깊이가 만나는 라운드입니다.

Two players with the same next-round number meet in that round. Repeatedly mapping to parent brackets identifies the first common level.

## 비용 / Complexity

시간 O(log n), 공간 O(1) / O(log n) time, O(1) space

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(n, a, b):
    rounds = 0
    # 다음 라운드 번호가 같아질 때까지 진행.
    while a != b:
        a = (a + 1) // 2
        # 상대의 다음 라운드 번호도 같은 방식으로 계산.
        b = (b + 1) // 2
        rounds += 1
    return rounds
```

## 다른 방법: 0기반 번호 XOR의 비트 길이 / XOR bit length of zero-based indices

0부터 센 번호가 처음 달라지는 최상위 비트가 서로 다른 대진 구간을 나타냅니다. XOR의 비트 길이가 만나기까지 올라가야 할 라운드 수입니다.

The highest differing bit in zero-based indices marks their largest distinct bracket subdivision. The XOR bit length equals the rounds to their common bracket.

[alternative.py](alternative.py)

```python
def solution(n, a, b):
    return ((a - 1) ^ (b - 1)).bit_length()
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    8,
    4,
    7
  ],
  "output": 3
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

출처: [프로그래머스 문제 12985](https://school.programmers.co.kr/learn/courses/30/lessons/12985), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 12985](https://school.programmers.co.kr/learn/courses/30/lessons/12985), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
