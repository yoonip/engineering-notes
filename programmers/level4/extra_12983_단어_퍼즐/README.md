# 단어 퍼즐

[Level 4 목록 / Level 4 index](../README.md) · [풀이 전체 목차 / Solution index](../../README.md)

Level 4 · `12983` · Python3 · [공식 문제](https://school.programmers.co.kr/learn/courses/30/lessons/12983)

[기본 풀이](solution.py) · [다른 풀이](alternative.py) · [예제 입력과 정답](examples.json) · [검증 코드](test_solution.py)

## 문제와 조건

길이 1~5의 단어 조각을 반복 사용해 목표 문자열을 만들 때 최소 조각 수를 구합니다.

입력 범위와 상수는 다음과 같습니다. 기호는 코드의 매개변수에 맞췄습니다.

`1≤pieces≤100; distinct lowercase pieces of length1..5; 1≤len(t)≤20000; reuse pieces; return −1 if impossible.`

## 풀이를 따라가기

목표의 앞 i글자를 만드는 최솟값을 저장합니다. 끝에서 1~5글자를 떼어 보며 유효한 조각이면 이전 접두사 답에 1을 더합니다. 불가능한 접두사는 무한대로 둡니다.

어떤 완성도 마지막 조각 하나와 그 앞 접두사로 유일하게 나뉩니다. 가능한 마지막 조각을 전부 비교하므로 최소를 놓치지 않습니다. Python 슬라이스·해시 비용까지 길이 제곱으로 적었지만 조각 길이 5는 고정 상수입니다.

## 다른 방법과 비교

대안은 접두사 길이를 정점으로 보고 조각 하나를 붙이는 이동을 BFS로 탐색합니다. 모든 이동 비용이 1이므로 처음 도달한 목표가 최소 조각 수입니다.

| 구분 | 시간 | 추가 공간 |
|---|---|---|
| 기본 풀이 | `O(len(t)·5² + total piece characters)` | `O(len(t)+total piece characters)` |
| 대안 풀이 | `O(len(t)·5² + total piece characters)` | `O(len(t)+total piece characters)` |

## 코드와 검증

`solution.py`에는 상태의 뜻과 경계조건을 한국어 주석으로 적었습니다. `alternative.py`는 별도의 풀이이며, `test_solution.py`에서 공식 예제와 생성 입력을 비교합니다. 실행 기록은 [validation.json](validation.json)에 있습니다. 원본 제출 파일은 [submitted_original.py](submitted_original.py)에 그대로 보관했습니다.

```bash
python test_solution.py
```

## English

### Problem and constraints

Reuse pieces of length one to five to construct a target string with as few pieces as possible.

Input limits and constants, using the parameter names in the code:

`1≤pieces≤100; distinct lowercase pieces of length1..5; 1≤len(t)≤20000; reuse pieces; return −1 if impossible.`

### Following the solution

Store the optimum for every target prefix. Try each possible last piece of length one to five and extend the preceding feasible prefix by one.

Every construction decomposes into its final piece and preceding prefix. Exhausting those final pieces proves the recurrence. The complexity includes Python slicing/hashing, with maximum piece length five remaining constant.

### Alternative and comparison

The alternative treats prefix lengths as graph vertices and appending a piece as a unit-cost edge. BFS reaches the goal with the minimum piece count.

The primary solution takes `O(len(t)·5² + total piece characters)` time and `O(len(t)+total piece characters)` additional space. The alternative takes `O(len(t)·5² + total piece characters)` time. Its additional space is `O(len(t)+total piece characters)`.

### Code and verification

Read `solution.py` for the primary implementation and `alternative.py` for the comparison. Comments explain states and boundary cases in Korean. Run `python test_solution.py` for the official examples and generated comparisons; [validation.json](validation.json) records the execution. The submitted source is preserved byte for byte in [submitted_original.py](submitted_original.py).

## 출처 / Source

- [Programmers — 단어 퍼즐](https://school.programmers.co.kr/learn/courses/30/lessons/12983): 문제 조건·입출력 예 확인 / problem constraints and examples checked on 2026-10-19.
