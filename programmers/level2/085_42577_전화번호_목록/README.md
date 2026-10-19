# 전화번호 목록

[공식 문제 / Official problem](https://school.programmers.co.kr/learn/courses/30/lessons/42577) · Level 2 · Python3

## 문제와 조건 / Task and conditions

전화번호는 1~1000000개, 길이는 1~20이며 중복 번호는 없습니다. 어느 번호가 다른 번호의 접두사이면 False, 아니면 True입니다.

There are 1–1000000 distinct phone numbers of length 1–20. Return False if any number is a prefix of another, otherwise True.

## 풀이 흐름 / Approach

전화번호를 사전순으로 정렬합니다. 어떤 번호가 다른 번호의 접두사라면 그 바로 다음 번호와의 비교에서도 드러납니다. 그래서 인접한 두 번호만 검사합니다.

Sort phone numbers lexicographically. If a number prefixes any later number, it also prefixes its immediate successor, so adjacent comparisons suffice.

## 왜 맞는가 / Why it works

같은 접두사로 시작하는 문자열은 사전순 정렬에서 연속한 구간입니다. 짧은 접두사 번호가 존재하면 그 구간의 첫 번호와 바로 뒤 번호가 반드시 충돌합니다.

Strings sharing a prefix form a contiguous lexicographic interval. If the prefix itself occurs, it is followed immediately by a conflicting string in that interval.

## 비용 / Complexity

최대 길이 d에 시간 O(nd log n), 공간 O(n) 정렬 보조 / O(nd log n) time, O(n) sorting workspace

## 구현 / Implementation

이 구현은 입력 배열을 제자리에서 정렬하거나 힙으로 바꿉니다.

This implementation sorts or heapifies the input array in place.

[solution.py](solution.py)

```python
def solution(phone_book):
    # 접두어가 같은 번호들이 붙게 됨.
    phone_book.sort()
    for index in range(len(phone_book) - 1):
        # 바로 다음 번호가 앞 번호로 시작하는지 확인.
        if phone_book[index + 1].startswith(phone_book[index]):
            return False
    return True
```

## 다른 방법: 전화번호 집합과 모든 접두사 / Hash set and proper prefixes

전체 번호를 집합에 넣고 각 번호의 짧은 접두사가 집합에 있는지 확인합니다. 정렬이 필요 없지만 Python 문자열 자르기 비용까지 포함하면 O(nd²) 시간 상한입니다.

Put all full numbers in a set and check every proper prefix. No sorting is needed, but Python prefix slicing gives an O(nd²) time upper bound.

[alternative.py](alternative.py)

```python
def solution(phone_book):
    full = set(phone_book)
    for number in phone_book:
        for end in range(1, len(number)):
            if number[:end] in full:
                return False
    return True
```

## 예시 / Example

공식 예제의 입력 인자와 결과입니다.

Input arguments and result from an official example.

```json
{
  "input": [
    [
      "119",
      "97674223",
      "1195524421"
    ]
  ],
  "output": false
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

출처: [프로그래머스 문제 42577](https://school.programmers.co.kr/learn/courses/30/lessons/42577), 확인 2026-10-19. 문제 조건은 요약했으며 풀이와 비교 코드는 위 파일에 있습니다.

Source: [Programmers problem 42577](https://school.programmers.co.kr/learn/courses/30/lessons/42577), checked 2026-10-19. The conditions are summarized; implementations and comparisons are included above.

큰 입력 검사: 동일 길이의 서로 다른 번호 100만 개 / One million distinct equal-length numbers

```bash
python verify_stress.py
```
