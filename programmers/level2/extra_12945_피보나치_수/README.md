# 피보나치 수

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12945) · Level 2 · Python3

## 문제와 조건 / Task and conditions

2≤n≤100000입니다. F(0)=0,F(1)=1이며 F(n)을 1234567로 나눈 나머지를 반환합니다.

2≤n≤100000, with F(0)=0 and F(1)=1. Return F(n) modulo 1234567.

## 풀이 흐름 / Approach

이전 두 피보나치 수만 보관합니다. 다음 값은 두 수의 합이며 매 단계에서 1234567로 나눈 나머지만 남깁니다.

Keep only the previous two Fibonacci numbers. Their sum gives the next one, reduced modulo 1234567 at every step.

## 왜 맞는가 / Why it works

F(n)=F(n−1)+F(n−2)이고 덧셈의 나머지는 각 항의 나머지로 계산해도 같습니다. 두 변수의 의미를 한 칸씩 이동하면 목표 항에 도달합니다.

F(n)=F(n−1)+F(n−2), and modular addition preserves the recurrence. Shifting the two stored terms forward reaches the requested value.

## 비용 / Complexity

시간 O(n), 공간 O(1) / O(n) time, O(1) space

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(n):
    # 두 변수만 사용하는 동적 계획법(DP).
    previous, current = 0, 1
    for _ in range(n):
        # 연속 두 피보나치 값을 다음으로 이동.
        previous, current = current, (previous + current) % 1234567
    return previous
```

## 다른 방법: 빠른 배가법 / Fast doubling

F(2k)=F(k)(2F(k+1)−F(k)), F(2k+1)=F(k)²+F(k+1)²를 사용합니다. 재귀 깊이와 시간 모두 O(log n)입니다.

Use F(2k)=F(k)(2F(k+1)−F(k)) and F(2k+1)=F(k)²+F(k+1)². Both time and recursion depth are O(log n).

[alternative.py](alternative.py)

```python
def solution(n):
    modulus = 1234567
    def pair(k):
        if k == 0:
            return 0, 1
        a, b = pair(k // 2)
        even = a * (2 * b - a) % modulus
        odd = (a * a + b * b) % modulus
        return (odd, (even + odd) % modulus) if k % 2 else (even, odd)
    return pair(n)[0]
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    3
  ],
  "output": 2
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

출처: [프로그래머스 문제 12945](https://school.programmers.co.kr/learn/courses/30/lessons/12945), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 12945](https://school.programmers.co.kr/learn/courses/30/lessons/12945), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
