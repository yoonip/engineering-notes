# 봉인된 주문

[Level 3 목록 / Level 3 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/389481) · Level 3 · Python3

## 문제와 조건 / Task and conditions

목표 순번 n은 1~10¹⁵, 삭제 주문은 1~300000개로 중복이 없습니다. 주문은 길이 1~11의 소문자이며 짧은 길이부터 같은 길이 안에서는 사전순입니다. 삭제 후 n번째 주문을 반환합니다.

n is 1–10¹⁵ and there are 1–300000 distinct banned lowercase words of length 1–11. Order words by length then lexicographically. Return the n-th surviving word.

## 풀이 흐름 / Approach

문자열을 자릿수에 0이 없는 26진법 번호로 바꾸면 짧은 길이 우선·사전순 순서와 일치합니다. 삭제 번호를 정렬하고 목표 n 이하의 삭제를 만날 때마다 n을 하나 늘린 뒤 다시 문자로 바꿉니다.

Encode words as bijective base-26 numbers, matching length-first then lexicographic order. Sort banned ranks and increment the target for every banned rank not exceeding it, then decode the result.

## 정답이 되는 이유 / Why it works

정렬된 삭제 번호를 앞에서 처리할 때 현재 n은 이미 처리한 삭제만 반영한 정답 순위입니다. 그 이하의 삭제 한 개는 목표를 한 칸 밀고, 더 큰 삭제는 영향을 주지 않아 불변식이 유지됩니다.

After each sorted banned rank, n is the answer rank accounting for all processed deletions. A deletion at or before n shifts it once; a larger deletion cannot affect it, preserving the invariant.

## 비용 / Complexity

금지 b개, 최대 길이 d에 시간 O(bd+b log b), 공간 O(b+d) / O(bd+b log b) time, O(b+d) space

## 구현 / Implementation

[solution.py](solution.py)

```python
def solution(n, bans):
    removed = []
    # 삭제 주문 하나씩 순회.
    for word in bans:
        value = 0
        for letter in word:
            # a=1~z=26인 26진수처럼 앞자리 값을 26배 해 더함.
            value = value * 26 + ord(letter) - ord('a') + 1
        removed.append(value)
    # sort는 원본 리스트를 오름차순으로 정렬.
    removed.sort()
    for value in removed:
        # 찾으려는 원래 위치 앞의 삭제인지 검사.
        if value <= n:
            n += 1
        else:
            break
    letters = []
    while n:
        n, digit = divmod(n - 1, 26)
        # 나머지를 a~z로 바꿔 추가.
        letters.append(chr(ord('a') + digit))
    return ''.join(reversed(letters))
```

## 다른 방법: 남은 주문 개수의 이진 탐색 / Binary search by remaining-rank count

어떤 원래 순위 x까지 남은 주문은 x−삭제개수(x)개입니다. bisect로 삭제 수를 세며 최초로 n개 이상이 되는 x를 이진 탐색합니다.

Up to an original rank x, the number of surviving words is x minus banned ranks at most x. Use bisect for that count and binary-search the first x reaching n survivors.

[alternative.py](alternative.py)

```python
from bisect import bisect_right

def solution(n, bans):
    def rank(word):
        value = 0
        for ch in word:
            value = value * 26 + ord(ch) - 96
        return value
    removed = sorted(map(rank, bans))
    left, right = n, n + len(removed)
    while left < right:
        middle = (left + right) // 2
        if middle - bisect_right(removed, middle) >= n:
            right = middle
        else:
            left = middle + 1
    result = []
    while left:
        left, digit = divmod(left - 1, 26)
        result.append(chr(97 + digit))
    return ''.join(reversed(result))
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    30,
    [
      "d",
      "e",
      "bb",
      "aa",
      "ae"
    ]
  ],
  "output": "ah"
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

출처: [프로그래머스 문제 389481](https://school.programmers.co.kr/learn/courses/30/lessons/389481), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 389481](https://school.programmers.co.kr/learn/courses/30/lessons/389481), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.
