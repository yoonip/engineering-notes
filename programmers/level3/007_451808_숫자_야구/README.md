# 숫자 야구

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/451808) · Level 3 · Python3

## 문제와 조건 / Task and conditions

비밀번호는 서로 다른 1~9 숫자 네 개입니다. 허용 질문 n은 6~3024이고 submit은 xS yB 단서를 반환합니다. 허용 횟수 안에서 비밀번호를 추론해 정수로 반환합니다.

The secret uses four distinct digits from 1–9. The query budget n is 6–3024 and submit returns xS yB clues. Infer and return the secret integer within the allowed calls.

## 풀이 흐름 / Approach

서로 다른 1~9 숫자 네 개의 순열 3024개를 후보로 둡니다. 단서마다 모순되는 후보를 지웁니다. 다음 질문은 가능한 응답으로 나눈 후보 그룹 중 가장 큰 그룹이 작아지는 수를 골라 최악의 남는 후보 수를 줄입니다.

Begin with 3024 permutations of four distinct digits from 1–9. Filter inconsistent candidates after each clue. Choose a next guess minimizing the largest response bucket, reducing the worst-case number of survivors.

## 정답이 되는 이유 / Why it works

관측 단서와 같은 응답을 내는 후보만 남기므로 정답은 삭제되지 않습니다. 후보가 하나면 그 수가 답입니다. 전체 응답 트리 검사에서 3024개 비밀번호를 모두 구분하며 최악 질문 수가 6회임을 확인했습니다. 단순 평균 분할만으로는 이 최악 횟수가 보장되지 않습니다.

Filtering retains exactly candidates producing the observed clue, so the secret is never removed. A singleton is therefore the answer. The full response-tree check distinguished all 3024 secrets with at most six queries. Average split quality alone does not guarantee this worst-case bound.

## 비용 / Complexity

후보 c≤3024, 호출 q에 보수적 O(qc²), 응답 캐시 공간 O(c²) / Conservative O(qc²) time, O(c²) cached response space

## 구현 / Implementation

[solution.py](solution.py)

```python
from itertools import permutations

def solution(n, submit):
    # 1~9 중 서로 다른 4개를 고른 순열 3024개를 list로 저장.
    digits = list(permutations(range(1, 10), 4))
    masks = [sum(1 << digit for digit in pattern) for pattern in digits]
    # 리스트 내포와 튜플 언패킹으로 네 자릿수를 실제 정수로 변환.
    numbers = [a * 1000 + b * 100 + c * 10 + d for a, b, c, d in digits]
    cache = {}

    def feedback_row(index):
        if index not in cache:
            # 질문의 네 숫자를 언패킹.
            a, b, c, d = digits[index]
            mask = masks[index]
            # 단서를 공통 수*5+스트라이크로 인코딩.
            cache[index] = bytes((mask & masks[i]).bit_count() * 5 + (a == w) + (b == x) + (c == y) + (d == z) for i, (w, x, y, z) in enumerate(digits))
        return cache[index]

    candidates = list(range(len(digits)))
    # turn은 현재 질문 회차.
    for turn in range(n):
        if len(candidates) == 1:
            return numbers[candidates[0]]
        # 질문 후보의 기본값.
        selected = candidates[0]
        if turn > 0:
            best = len(candidates) + 1
            # 남아 있는 비밀번호 각각을 다음 질문으로 가정.
            for guess in candidates:
                row = feedback_row(guess)
                # 응답 인코딩 0~24별 후보 수를 셀 리스트 초기화.
                counts = [0] * 25
                worst = 0
                for hidden in candidates:
                    # 이 질문·비밀번호 조합의 예상 단서 번호.
                    clue = row[hidden]
                    counts[clue] += 1
                    # 현재 최악 그룹 크기 갱신.
                    worst = max(worst, counts[clue])
                    if worst >= best:
                        break
                # 최악의 후보 수를 더 줄이는 질문인지 검사.
                if worst < best:
                    best, selected = worst, guess
                    # 어떤 응답이든 후보가 하나이면 더 좋은 질문은 없음.
                    if best == 1:
                        break
        clue = submit(numbers[selected])
        # 'xS yB'의 두 숫자를 추출.
        strikes, balls = int(clue[0]), int(clue[3])
        observed = (strikes + balls) * 5 + strikes
        # 방금 질문의 예상 응답 행.
        row = feedback_row(selected)
        candidates = [hidden for hidden in candidates if row[hidden] == observed]
    return numbers[candidates[0]]
```

## 다른 방법: 첫 후보 질문과 단서 필터 / First-candidate querying with clue filtering

가장 앞 후보를 질문하고 맞지 않는 후보를 지우는 직접 전략입니다. 충분한 질문 예산에서는 정답을 찾지만 6회 제한을 보장하지 않으므로 제출용 최소최대 전략과 구별한 검증 코드입니다.

Query the first remaining candidate and filter by its clue. This finds the secret with a sufficiently large budget but does not guarantee six queries, so it is a verification comparison rather than a replacement for the budgeted minimax submission.

[alternative_reference.py](alternative_reference.py)

```python
from itertools import permutations

def solution(n, submit):
    candidates = [''.join(map(str, p)) for p in permutations(range(1, 10), 4)]
    for _ in range(n):
        if len(candidates) == 1:
            return int(candidates[0])
        guess = candidates[0]
        clue = submit(int(guess))
        strikes, balls = int(clue[0]), int(clue[3])
        next_candidates = []
        for secret in candidates:
            same_position = sum(a == b for a, b in zip(guess, secret))
            common_digits = len(set(guess) & set(secret))
            if (same_position, common_digits - same_position) == (strikes, balls):
                next_candidates.append(secret)
        candidates = next_candidates
    if len(candidates) != 1:
        raise ValueError('이 비교 전략의 질문 예산이 부족합니다.')
    return int(candidates[0])
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    3024
  ],
  "output": 1357
}
```

## 검증 / Verification

```bash
python verify.py
```

원본 채점 기록과 별도로 로컬 검증 6개를 통과했습니다. 검증 입력·예상 결과는 [cases.json](cases.json), 재현 코드는 [verify.py](verify.py), 실행 기록은 [verification.json](verification.json)에 있습니다.

Separately from the original grading record, 6 local cases passed. Inputs and expected results are in [cases.json](cases.json), the reproducer is [verify.py](verify.py), and the run record is [verification.json](verification.json).

비교 구현은 작은 입력 6개에서 함께 통과했습니다. 큰 입력용 제출 풀이와 전수 탐색 기준 코드는 파일명과 설명으로 구분합니다.

The comparison also passed 6 small-input cases. Exhaustive reference implementations are distinguished from the submission solution in their filenames and descriptions.

원본 채점 기록: 100점. [submitted_original.py](submitted_original.py)는 당시 원본 파일을 그대로 보존하며, `solution.py`는 설명을 정리한 구현입니다.

Original recorded grade: 100/100. [submitted_original.py](submitted_original.py) preserves the original file bytes; `solution.py` contains the documented implementation.

출처: [프로그래머스 문제 451808](https://school.programmers.co.kr/learn/courses/30/lessons/451808), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 451808](https://school.programmers.co.kr/learn/courses/30/lessons/451808), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

전체 응답 트리도 검사했습니다. 가능한 비밀번호 3024개가 모두 유일한 후보로 좁혀졌고 최악 질문 수는 6회입니다. [verify_strategy.py](verify_strategy.py)로 재현합니다.

The full response tree was checked as well: all 3024 possible secrets reached singleton candidates, with at most six queries. Reproduce it with [verify_strategy.py](verify_strategy.py).
