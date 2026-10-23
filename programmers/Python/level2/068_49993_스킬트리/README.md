# 스킬트리

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/49993) · Level 2 · Python3

## 문제와 조건 / Task and conditions

선행 순서는 1~26자, 트리는 1~20개이고 각 길이는 2~26자입니다. 모두 중복 없는 대문자 스킬이며 조건에 맞는 트리 수를 반환합니다.

The prerequisite chain has 1–26 characters; there are 1–20 trees of length 2–26. Each uses distinct uppercase skills. Return the number satisfying the prerequisites.

## 풀이 흐름 / Approach

선행 조건이 있는 스킬만 남깁니다. 남은 문자열이 주어진 선행 순서의 접두부이면 가능한 스킬트리입니다. 선행 조건이 없는 스킬은 어느 위치에 있어도 괜찮습니다.

Keep only skills that appear in the prerequisite chain. The remaining sequence must be a prefix of that chain; unrelated skills may occur anywhere.

## 정답이 되는 이유 / Why it works

배울 수 있는 선행 스킬은 항상 chain의 첫 k개뿐입니다. 따라서 조건 대상만 추출한 결과가 접두부라는 조건은 필요충분합니다.

The learned prerequisite skills must be exactly the first k elements of the chain. Thus the filtered-prefix condition is both necessary and sufficient.

## 비용 / Complexity

전체 문자 수 L에 시간 O(L), 공간 O(가장 긴 트리 길이) / O(L) time, O(maximum tree length) space

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(skill, skill_trees):
    # 선행 조건이 있는 스킬들을 빠르게 찾도록 저장.
    required = set(skill)
    answer = 0
    for tree in skill_trees:
        # 생성식의 if·in으로 선행 대상만 남기고 join으로 문자열 연결.
        filtered = ''.join(character for character in tree if character in required)
        if skill.startswith(filtered):
            answer += 1
    return answer
```

## 다른 방법: 다음에 배울 위치 추적 / Track the next required skill

필터 문자열을 만들지 않고 다음 차례의 스킬만 확인합니다. 스킬 순서 표를 쓰면 보조 공간은 선행 스킬 수만큼이며 잘못된 순서를 발견하는 즉시 종료합니다.

Track the next expected prerequisite without constructing a filtered string. A position map uses space proportional to the chain and allows early rejection.

[alternative.py](alternative.py)

```python
def solution(skill, skill_trees):
    order = {ch: i for i, ch in enumerate(skill)}
    answer = 0
    for tree in skill_trees:
        needed = 0
        for ch in tree:
            if ch in order:
                if order[ch] != needed:
                    break
                needed += 1
        else:
            answer += 1
    return answer
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    "CBD",
    [
      "BACDE",
      "CBADF",
      "AECB",
      "BDA"
    ]
  ],
  "output": 2
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

출처: [프로그래머스 문제 49993](https://school.programmers.co.kr/learn/courses/30/lessons/49993), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 49993](https://school.programmers.co.kr/learn/courses/30/lessons/49993), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
