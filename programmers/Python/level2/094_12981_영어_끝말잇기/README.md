# 영어 끝말잇기

[Level 2 목록 / Level 2 index](../README.md) · [풀이 전체 목차 / Solution index](../../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/12981) · Level 2 · Python3

## 문제와 조건 / Task and conditions

사람은 2~10명, 단어는 n~100개이고 각 길이는 2~50자 소문자입니다. 중복 또는 연결 실패가 처음 나온 [사람,차례]를 반환하며 없으면 [0,0]입니다.

There are 2–10 players and n–100 lowercase words of length 2–50. Return [player,turn] for the first repetition or link failure, or [0,0] if none occurs.

## 풀이 흐름 / Approach

이미 나온 단어는 집합으로 확인하고, 직전 단어의 마지막 글자와 현재 단어의 첫 글자를 비교합니다. 처음 틀린 위치를 사람 번호와 차례로 바꿉니다.

Use a set to detect repeated words and compare the previous word’s last letter with the current first letter. Convert the first failing index into player number and turn.

## 정답이 되는 이유 / Why it works

정방향으로 검사하므로 처음 발견한 위반이 최초 탈락입니다. 0기반 인덱스 i에서 사람은 i%n+1, 그 사람의 차례는 i//n+1입니다.

A forward scan finds the earliest violation. At zero-based index i, the player is i%n+1 and that player’s turn is i//n+1.

## 비용 / Complexity

문자 합 L에 평균 시간 O(L), 공간 O(L) / Average O(L) time and space for total word characters

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(n, words):
    seen = set()
    # 발언 순서·단어를 언패킹.
    for index, word in enumerate(words):
        if word in seen or (index > 0 and words[index - 1][-1] != word[0]):
            return [index % n + 1, index // n + 1]
        # add로 이번 단어를 사용 목록에 추가.
        seen.add(word)
    return [0, 0]
```

## 다른 방법: 앞부분 목록과 직접 비교 / Compare with all previous words

집합 대신 앞서 나온 목록에서 중복을 찾습니다. 시간 O(w²d) 상한이므로 짧은 입력의 기준 구현이며 결과를 직접 따라가기 쉽습니다.

Search the list of previous words instead of using a set. The O(w²d) upper bound makes this a short-input reference whose behavior is easy to inspect.

[alternative_reference.py](alternative_reference.py)

```python
def solution(n, words):
    for i, word in enumerate(words):
        repeated = word in words[:i]
        disconnected = i > 0 and words[i - 1][-1] != word[0]
        if repeated or disconnected:
            return [i % n + 1, i // n + 1]
    return [0, 0]
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    3,
    [
      "tank",
      "kick",
      "know",
      "wheel",
      "land",
      "dream",
      "mother",
      "robot",
      "tank"
    ]
  ],
  "output": [
    3,
    3
  ]
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

출처: [프로그래머스 문제 12981](https://school.programmers.co.kr/learn/courses/30/lessons/12981), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 12981](https://school.programmers.co.kr/learn/courses/30/lessons/12981), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
